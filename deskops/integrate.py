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
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

import yaml

from deskops.config import DeskConfig
from deskops.config import IntegrateConfig
from deskops.errors import UsageError
from deskops.models.task_lifecycle import CLOSEOUT_STATES
from deskops.queue import _read_job, queue_dir, wait_reason

SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
DESK_ONLY_PREFIXES = ("desk/", ".sldb/", "runs/")
SHORT = 12


class AlreadyIntegrated(Exception):
    """The tip is already an ancestor of the remote branch."""


class StepFailed(Exception):
    """A step of the integration failed; ``step`` and ``detail`` make the ``fallo:`` line."""

    def __init__(self, step: str, detail: str) -> None:
        super().__init__(f"{step}: {detail}")
        self.step = step
        self.detail = detail


def _run(argv: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    if argv and argv[0] == "git":
        # Parsed paths must not come back quoted with octal escapes (ids with accents).
        argv = ["git", "-c", "core.quotepath=false", *argv[1:]]
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


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _clean_stale_integrate_dirs(own: Path, max_age: float) -> None:
    """Remove ``deskops-integrate-*`` temp dirs left by dead runs (never ``own`` nor a live pid's)."""
    base = Path(tempfile.gettempdir())
    try:
        candidates = sorted(base.glob("deskops-integrate-*"))
    except OSError:
        return
    for path in candidates:
        try:
            if not path.is_dir() or path.resolve() == own.resolve():
                continue
            owner = path / "owner.pid"
            if owner.is_file():
                try:
                    pid = int(owner.read_text(encoding="utf-8").strip())
                except (ValueError, OSError):
                    continue
                if pid <= 0 or _pid_alive(pid):
                    continue
            elif time.time() - path.stat().st_mtime <= max_age:
                continue
            shutil.rmtree(path, ignore_errors=True)
            print(f"limpieza: {path}")
        except OSError:
            continue


def _run_suite(cfg: IntegrateConfig, copy: Path, log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    work = copy.parent
    env = dict(os.environ)
    env["PYTHONPATH"] = str(copy)
    basetemp = f"--basetemp={work / 'pytest'}"
    env["PYTEST_ADDOPTS"] = " ".join(filter(None, [env.get("PYTEST_ADDOPTS", "").strip(), basetemp]))
    with _suite_lock(cfg.tests_lock), log_path.open("wb") as log:
        _clean_stale_integrate_dirs(work, cfg.suite_timeout)
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


def extend_tip(root: Path, tip: str, remote: str | None = None, branch: str | None = None) -> str:
    """HEAD when only desk commits (``desk/``, ``.sldb/``, ``runs/``) follow the closeout commit, else ``tip``.

    When the configured remote branch is an ancestor of HEAD (a merge of it after the closeout), the
    code that merge brought from the remote is not counted: only the non-merge commits of
    ``tip..HEAD`` that the remote branch lacks are checked.
    """
    head = _run(["git", "rev-parse", "HEAD"], root)
    if head.returncode != 0 or head.stdout.strip() == tip:
        return tip
    head_sha = head.stdout.strip()
    remote_sha = None
    if remote and branch:
        fetched = _run(["git", "fetch", "-q", remote, branch], root)
        if fetched.returncode == 0:
            ref = _run(["git", "rev-parse", "FETCH_HEAD"], root)
            candidate = ref.stdout.strip() if ref.returncode == 0 else ""
            if candidate and _run(["git", "merge-base", "--is-ancestor", candidate, head_sha], root).returncode == 0:
                remote_sha = candidate
    if remote_sha is None:
        diff = _run(["git", "diff", "--name-only", f"{tip}..{head_sha}"], root)
    else:
        diff = _run(
            ["git", "log", "--no-merges", "--name-only", "--format=", head_sha, f"^{tip}", f"^{remote_sha}"], root
        )
    if diff.returncode != 0:
        return tip
    if any(not path.startswith(DESK_ONLY_PREFIXES) for path in diff.stdout.splitlines() if path):
        return tip
    return head_sha


def integrate(root: Path, task_id: str, dry_run: bool) -> int:
    config = DeskConfig.load(root / "desk")
    cfg = config.integrate
    if cfg is None:
        raise UsageError("falta el campo integrate en desk/config.json")
    tip, code = load_closed_task(root, task_id)
    extended = extend_tip(root, tip, cfg.remote_url, cfg.branch)
    if extended != tip:
        tip = extended
        print(f"tip extendido a {tip[:SHORT]}: solo commits de desk")

    temps: list[Path] = []
    result = "ok"
    try:
        try:
            _steps(root, config, cfg, task_id, tip, code, dry_run, temps)
        except AlreadyIntegrated:
            result = "ya-integrado"
            print(f"ya integrado: {tip[:SHORT]}")
            if not dry_run:
                _resolve_failed(root, cfg, task_id)
            return 0
        except StepFailed as exc:
            result = f"fallo:{exc.step}"
            print(f"fallo: {exc.step}: {exc.detail}")
            return 1
    finally:
        for temp in temps:
            shutil.rmtree(temp, ignore_errors=True)
        _append_event(root, task_id, result if not (dry_run and result == "ok") else "dry-run", tip)
    if not dry_run and cfg.mode != "pr":
        _resolve_failed(root, cfg, task_id)
    verb = "simulado" if dry_run else "integrado"
    where = f"en PR a {cfg.branch}" if cfg.mode == "pr" else f"en {cfg.branch}"
    print(f"{verb} {code[:SHORT]} {tip[:SHORT]} {where}")
    return 0


def _resolve_failed(root: Path, cfg: IntegrateConfig, current: str) -> None:
    """Move to ``done`` the failed integrate jobs whose closing commit is already in the remote branch."""
    failed = queue_dir(root) / "failed"
    if not failed.is_dir():
        return
    if _run(["git", "fetch", "-q", cfg.remote_url, cfg.branch], root).returncode != 0:
        return
    remote = _run(["git", "rev-parse", "FETCH_HEAD"], root).stdout.strip()
    if not remote:
        return
    for path in sorted(failed.glob("*.json")):
        try:
            job = _read_job(path)
            if job.get("kind") != "integrate" or not job.get("task_id"):
                continue
            found = _run(
                ["git", "log", "-1", "--format=%H", f"--grep=^Task-Id: {job['task_id']}$", cfg.branch], root
            )
            sha = found.stdout.strip() if found.returncode == 0 else ""
            if not sha or _run(["git", "merge-base", "--is-ancestor", sha, remote], root).returncode != 0:
                continue
            line = f"resuelto por integrate {current}: {sha} ya en origin/{cfg.branch}\n"
            if job.get("log"):
                log = Path(str(job["log"]))
                log.parent.mkdir(parents=True, exist_ok=True)
                existing = log.read_text(encoding="utf-8") if log.is_file() else ""
                with log.open("a", encoding="utf-8") as handle:
                    handle.write(("\n" if existing and not existing.endswith("\n") else "") + line)
            done = queue_dir(root) / "done"
            done.mkdir(parents=True, exist_ok=True)
            path.rename(done / path.name)
            print(f"integrate fallido resuelto: {job.get('id', path.stem)}")
        except (OSError, ValueError):
            continue


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
    (work / "owner.pid").write_text(f"{os.getpid()}\n", encoding="utf-8")
    copy = work / "copia"
    _git(root, "clone", "-q", "--no-hardlinks", str(root), str(copy), step="copia")
    _git(copy, "checkout", "-q", "--detach", tip, step="copia")
    _git(copy, "remote", "set-url", "origin", cfg.remote_url, step="copia")
    _git(copy, "fetch", "-q", "origin", branch, step="copia")

    if _run(["git", "merge-base", "--is-ancestor", "HEAD", remote_ref], copy).returncode == 0:
        raise AlreadyIntegrated()

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
    if cfg.mode == "pr":
        _open_pr(root, copy, cfg, task_id, tip, code, env, dry_run)
        return
    code_in_origin = _run(["git", "merge-base", "--is-ancestor", code, remote_ref], copy).returncode == 0
    if code_in_origin:
        print(f"código ya en origin: {code[:SHORT]}")
    code_ff = not code_in_origin and _run(["git", "merge-base", "--is-ancestor", remote_ref, code], copy).returncode == 0
    if not code_in_origin and not code_ff:
        print(f"código va con el tip: {code[:SHORT]}")
    pushes = [f"git push origin {code}:{branch}"] if code_ff else []
    pushes.append(f"git push origin {tip}:{branch}")
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


def _task_title(root: Path, tip: str, task_id: str) -> str:
    """First ``# `` heading of the last recorded version of the task document (task id when none)."""
    task_rel = f"desk/tasks/{task_id}.md"
    text = _show(root, "HEAD", task_rel)
    if text is None:
        before = _run(["git", "log", "-1", "--format=%H", f"{tip}^", "--", task_rel], root)
        revision = before.stdout.strip() if before.returncode == 0 else ""
        text = _show(root, revision, task_rel) if revision else None
    for line in (text or "").splitlines():
        if line.startswith("# "):
            return line[2:].strip() or task_id
    return task_id


def _open_pr(
    root: Path, copy: Path, cfg: IntegrateConfig, task_id: str, tip: str, code: str,
    env: dict[str, str], dry_run: bool,
) -> None:
    """pr mode: push the tip as ``task/<id>`` and open the PR to ``cfg.branch`` unless one is open already."""
    from deskops.dispatch import task_branch

    head = task_branch(task_id)
    title = _task_title(root, tip, task_id)
    closeout = _git(copy, "log", "-1", "--format=%B", tip, step="pr")
    body = f"Task-Id: {task_id}\n\nCodigo: {code}\nCierre: {tip}\n\n{closeout}\n"
    push = f"git push origin {tip}:refs/heads/{head}"
    create = f"gh pr create --base {cfg.branch} --head {head} --title {title!r}"
    if dry_run:
        print(f"dry-run: {push}")
        print(f"dry-run: {create}")
        return
    _git(copy, *push.split()[1:], step="push", env=env)
    listed = _run(
        ["gh", "pr", "list", "--head", head, "--base", cfg.branch, "--state", "open", "--json", "url", "--jq", ".[0].url"],
        copy, env,
    )
    if listed.returncode != 0:
        raise StepFailed("pr", f"gh pr list: {' '.join((listed.stderr or listed.stdout).split())}")
    url = listed.stdout.strip()
    if not url or url == "null":
        made = _run(
            ["gh", "pr", "create", "--base", cfg.branch, "--head", head, "--title", title, "--body", body], copy, env
        )
        if made.returncode != 0:
            raise StepFailed("pr", f"gh pr create: {' '.join((made.stderr or made.stdout).split())}")
        url = made.stdout.strip().splitlines()[-1] if made.stdout.strip() else ""
    print(f"PR: {url}")


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
