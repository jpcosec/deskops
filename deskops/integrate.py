"""`deskops integrate`: run the gates of a closed task in a clean copy and push code and tip.

The integration the operator did by hand, as one command a host queue job can run:
memory gates, clean clone at the closing commit, fast-forward check, full suite (only when
the range touches more than desk records), store and graph checks, then the two pushes and
the tools checkout. The first failing step stops everything: nothing is pushed, the copies
are removed and the command exits 1 with ``fallo: <paso>: <detalle>``.
"""

from __future__ import annotations

import contextlib
import fcntl
import os
import re
import shutil
import signal
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

import yaml

from deskops.config import DeskConfig
from deskops.config import IntegrateConfig
from deskops.errors import UsageError
from deskops.models.task_lifecycle import CLOSEOUT_STATES
from deskops.queue import wait_reason

SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
DESK_ONLY_PREFIXES = ("desk/", ".sldb/", "runs/")
SHORT = 12


class StepFailed(Exception):
    """A step of the integration failed; ``step`` and ``detail`` make the ``fallo:`` line."""

    def __init__(self, step: str, detail: str) -> None:
        super().__init__(f"{step}: {detail}")
        self.step = step
        self.detail = detail


def _run(argv: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, env=env, stdin=subprocess.DEVNULL)


def _git(cwd: Path, *argv: str, step: str, env: dict[str, str] | None = None) -> str:
    result = _run(["git", *argv], cwd, env)
    if result.returncode != 0:
        detail = " ".join((result.stderr.strip() or result.stdout.strip() or f"codigo {result.returncode}").split())
        raise StepFailed(step, f"git {' '.join(argv)}: {detail}")
    return result.stdout.strip()


def _split_frontmatter(text: str) -> dict[str, Any]:
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data = yaml.safe_load(parts[1])
    return data if isinstance(data, dict) else {}


def _show(root: Path, rev: str, path: str) -> str | None:
    result = _run(["git", "show", f"{rev}:{path}"], root)
    return result.stdout if result.returncode == 0 else None


def find_tip(root: Path, task_id: str) -> str | None:
    """Most recent commit of HEAD whose whole subject is ``closeout: <task_id>``."""
    subject = f"closeout: {task_id}"
    result = _run(
        ["git", "log", "HEAD", "--fixed-strings", f"--grep={subject}", "--format=%H %s"], root
    )
    if result.returncode != 0:
        return None
    for line in result.stdout.splitlines():
        sha, _, subj = line.partition(" ")
        if subj == subject:
            return sha
    return None


def code_commit(references: list[Any]) -> str | None:
    for item in references:
        if isinstance(item, str) and SHA_RE.match(item):
            return item.lower()
    return None


def _receipt_commit(root: Path, tip: str, task_id: str) -> str | None:
    """The commit an accepted ``evidence-commit`` receipt of the tip names (latest receipt first)."""
    folder = f"desk/reviews/{task_id}/"
    listing = _run(["git", "ls-tree", "--name-only", tip, folder], root)
    names = [line for line in listing.stdout.splitlines() if "/evidence-commit-" in line]

    def number(name: str) -> int:
        digits = re.findall(r"(\d+)\.md$", name)
        return int(digits[0]) if digits else 0

    for name in sorted(names, key=number, reverse=True):
        text = _show(root, tip, name)
        data = _split_frontmatter(text) if text else {}
        if data.get("verdict") != "accepted":
            continue
        for token in re.findall(r"[0-9a-fA-F]{40}(?![0-9a-fA-F])", str(data.get("value") or "")):
            return token.lower()
    return None


def load_closed_task(root: Path, task_id: str) -> tuple[str, str]:
    """(tip, code commit) of a closed task; UsageError (exit 2) when it is not closed or a commit is missing.

    ``closeout commit`` removes the task document in the closing commit, so a task closed that
    way has no document at HEAD. The code commit is then the first 40-hex entry of ``references``
    in the last recorded version of the task; when that version predates the references (the
    closeout drops what was never committed) it is the commit the accepted ``evidence-commit``
    receipt of the tip names. A document still at HEAD counts as closed only when its status and
    last history item are the pair ``CLOSEOUT_STATES`` declares for a normal closeout.
    """
    task_rel = f"desk/tasks/{task_id}.md"
    tip = find_tip(root, task_id)
    live = _show(root, "HEAD", task_rel)
    if live is not None:
        data = _split_frontmatter(live)
        history = [str(item) for item in data.get("history") or []]
        status, last = str(data.get("status")), (history[-1] if history else "")
        if (status, last) != ("closed", CLOSEOUT_STATES["closed"][0]):
            raise UsageError(
                f"la tarea {task_id} no esta cerrada (status '{status}', ultima entrada de history '{last}')"
            )
        references = list(data.get("references") or [])
    else:
        if tip is None:
            raise UsageError(f"la tarea {task_id} no esta cerrada: no hay commit 'closeout: {task_id}' en HEAD")
        before = _run(["git", "log", "-1", "--format=%H", f"{tip}^", "--", task_rel], root)
        revision = before.stdout.strip() if before.returncode == 0 else ""
        recorded = _show(root, revision, task_rel) if revision else None
        references = list(_split_frontmatter(recorded).get("references") or []) if recorded else []
    if tip is None:
        raise UsageError(f"falta el commit de cierre 'closeout: {task_id}' en HEAD")
    code = code_commit(references) or (_receipt_commit(root, tip, task_id) if live is None else None)
    if code is None:
        raise UsageError("falta el commit de codigo en references")
    return tip, code


def _collect_paths(node: Any) -> Iterator[str]:
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "path" and isinstance(value, str):
                yield value
            else:
                yield from _collect_paths(value)
    elif isinstance(node, list):
        for item in node:
            yield from _collect_paths(item)


def _missing_count(copy: Path) -> int:
    """Failing findings of ``deskops graph missing`` (the function the command calls)."""
    from deskops.graph.checks import GraphMissingCheckError, find_missing_graph_references

    try:
        findings = find_missing_graph_references(copy)
    except GraphMissingCheckError as exc:
        raise StepFailed("graph", str(exc)) from exc
    return len([finding for finding in findings if not finding.record])


@contextlib.contextmanager
def _suite_lock(path: str | None) -> Iterator[None]:
    if not path:
        yield
        return
    lock = Path(path)
    lock.parent.mkdir(parents=True, exist_ok=True)
    with lock.open("a+") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def _run_suite(cfg: IntegrateConfig, copy: Path, log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(copy)
    with _suite_lock(cfg.tests_lock), log_path.open("wb") as log:
        try:
            proc = subprocess.Popen(
                cfg.suite, cwd=copy, env=env, stdout=log, stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL, start_new_session=True,
            )
        except OSError as exc:
            raise StepFailed("suite", f"no arranca {cfg.suite}: {exc}") from exc
        try:
            code = proc.wait(timeout=cfg.suite_timeout)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            raise StepFailed("suite", f"timeout tras {cfg.suite_timeout} s") from None
    if code != 0:
        raise StepFailed("suite", f"codigo {code}, log {log_path}")


def _append_event(root: Path, task_id: str, result: str, tip: str | None) -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    log = root / "runs" / "hooks" / "events.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as handle:
        handle.write(f"{stamp} {task_id} integrate {result} {(tip or '')[:SHORT]}\n")


def integrate(root: Path, task_id: str, dry_run: bool) -> int:
    config = DeskConfig.load(root / "desk")
    cfg = config.integrate
    if cfg is None:
        raise UsageError("falta el campo integrate en desk/config.json")
    tip, code = load_closed_task(root, task_id)

    temps: list[Path] = []
    result = "ok"
    try:
        try:
            _steps(root, config, cfg, task_id, tip, code, dry_run, temps)
        except StepFailed as exc:
            result = f"fallo:{exc.step}"
            print(f"fallo: {exc.step}: {exc.detail}")
            return 1
    finally:
        for temp in temps:
            shutil.rmtree(temp, ignore_errors=True)
        _append_event(root, task_id, result if not (dry_run and result == "ok") else "dry-run", tip)
    verb = "simulado" if dry_run else "integrado"
    print(f"{verb} {code[:SHORT]} {tip[:SHORT]} en {cfg.branch}")
    return 0


def _steps(
    root: Path, config: DeskConfig, cfg: IntegrateConfig, task_id: str, tip: str, code: str,
    dry_run: bool, temps: list[Path],
) -> None:
    branch = cfg.branch
    remote_ref = f"origin/{branch}"

    reason = wait_reason(config)
    if reason:
        raise StepFailed("memoria", reason)

    work = Path(tempfile.mkdtemp(prefix="deskops-integrate-"))
    temps.append(work)
    copy = work / "copia"
    _git(root, "clone", "-q", "--no-hardlinks", str(root), str(copy), step="copia")
    _git(copy, "checkout", "-q", "--detach", tip, step="copia")
    _git(copy, "remote", "set-url", "origin", cfg.remote_url, step="copia")
    _git(copy, "fetch", "-q", "origin", branch, step="copia")

    if _run(["git", "merge-base", "--is-ancestor", remote_ref, "HEAD"], copy).returncode != 0:
        raise StepFailed("fast-forward", f"{remote_ref} no es ancestro de {tip[:SHORT]}")

    changed = _git(copy, "diff", "--name-only", remote_ref, "HEAD", step="suite").splitlines()
    if any(not path.startswith(DESK_ONLY_PREFIXES) for path in changed if path):
        _run_suite(cfg, copy, root / "runs" / "queue" / "logs" / f"integrate-{task_id}.log")

    store_text = _show(copy, "HEAD", ".sldb/store.yaml")
    if store_text is None:
        raise StepFailed("store", ".sldb/store.yaml ausente en el commit")
    try:
        store = yaml.safe_load(store_text)
    except yaml.YAMLError as exc:
        raise StepFailed("store", f".sldb/store.yaml no se lee: {exc}") from exc
    for path in _collect_paths(store):
        if path.startswith("../"):
            continue
        if _run(["git", "cat-file", "-e", f"HEAD:{path.rstrip('/') or '.'}"], copy).returncode != 0:
            raise StepFailed("store", f"ruta ausente en el commit: {path}")

    base = work / "base"
    _git(copy, "worktree", "add", "-q", "--detach", str(base), remote_ref, step="graph")
    try:
        tip_missing = _missing_count(copy)
        base_missing = _missing_count(base)
    except StepFailed:
        raise
    except Exception as exc:  # noqa: BLE001 - a graph that cannot be read is a failed gate
        raise StepFailed("graph", f"{type(exc).__name__}: {exc}") from exc
    if tip_missing > base_missing:
        raise StepFailed("graph", f"faltantes {tip_missing} en el tip > {base_missing} en {remote_ref}")

    env = dict(os.environ)
    env.update(cfg.push_env)
    pushes = [f"git push origin {code}:{branch}", f"git push origin {tip}:{branch}"]
    if dry_run:
        for line in pushes:
            print(f"dry-run: {line}")
    else:
        for line in pushes:
            _git(copy, *line.split()[1:], step="push", env=env)

    if cfg.tools_checkout and not dry_run:
        tools = Path(cfg.tools_checkout)
        _git(tools, "fetch", "origin", step="herramientas")
        _git(tools, "checkout", "--detach", remote_ref, step="herramientas")


class IntegrateCLI:
    """`deskops integrate --task <id> | --task-from-env [--dry-run] [--root .]`."""

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        task = getattr(args, "task", None)
        from_env = bool(getattr(args, "task_from_env", False))
        if task and from_env:
            raise UsageError("--task y --task-from-env son excluyentes.")
        if from_env:
            task = os.environ.get("DESKOPS_TASK_ID", "")
        task = (task or "").strip()
        if not task:
            raise UsageError("integrate necesita --task <id> o --task-from-env con DESKOPS_TASK_ID no vacia.")
        return integrate(root, task, bool(getattr(args, "dry_run", False)))
