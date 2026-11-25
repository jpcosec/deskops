FILE:desk/tasks/task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas.md
---
sldb:
  by: agent
  at: '2026-11-23T04:37:25Z'
  authority: generated
  via: create_document
id: task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- deskops/integrate.py
depends_on: []
pills: []
files:
- deskops/integrate.py
- tests/test_integrate.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# integrate corre la suite con --basetemp dentro de su carpeta temporal y al empezar borra las carpetas deskops-integrate-* de corridas muertas

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de la sesión de Governance del 2026-11-23, registrado en ~/coordinacion/respuesta-deskops-2026-11-22-despacho-por-pr.md. En deskops/integrate.py, _steps (alrededor de la línea 303) crea `work` con tempfile.mkdtemp(prefix="deskops-integrate-") y el finally de integrate (alrededor de la línea 283) borra `temps`. Pero _run_suite (línea 195) corre cfg.suite sin basetemp: pytest usa su basetemp por defecto, /dev/shm/pytest-of-<usuario>, fuera de `work`, y conserva 3 corridas de unos 5 GB cada una. El 2026-11-23 eso dejó /dev/shm al 99 % (13 GB de pytest-of-robocop) y el intento 20261123T032514Z del integrate del modo pr falló con 6 ENOSPC en tests/test_view.py y tests/test_view_goldens.py. Además, un SIGKILL u OOM (dos el mismo día, 02:55 y 03:12 UTC) se salta el finally y la carpeta deskops-integrate-* queda para siempre.

## Goal

_Describe the concrete result this task must produce._

(1) _run_suite le da a la suite --basetemp=<work>/pytest: agrega `--basetemp=<work>/pytest` a PYTEST_ADDOPTS en el env del proceso (conservando lo que ya traiga PYTEST_ADDOPTS, separado por un espacio). Va por env y no por argv porque la suite configurada en desk/config.json es `sh -c "... pytest ..."` y agregar un argumento al final no llega a pytest. (2) Cada carpeta de trabajo deja un archivo owner.pid con el pid del proceso de integrate. Al empezar la suite, ya con el lock de la suite tomado (_suite_lock(cfg.tests_lock)), integrate borra las carpetas deskops-integrate-* de tempfile.gettempdir() que son de corridas muertas: las que tienen owner.pid con un pid que no vive (os.kill(pid, 0) da ProcessLookupError) y las que no tienen owner.pid y tienen mtime más viejo que cfg.suite_timeout. Nunca borra la carpeta propia ni la de un pid vivo. Cada carpeta borrada se imprime en una línea ("limpieza: <ruta>").

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/integrate.py (_run_suite, _steps, una función nueva de limpieza) y tests/test_integrate.py. No entra: cambiar la suite de desk/config.json, la limpieza de /dev/shm/pytest-of-scion de los testers (tarea aparte), la cola (deskops/queue.py).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests nuevos en tests/test_integrate.py (fallan antes del cambio): test_suite_gets_basetemp_inside_work: una suite falsa ["sh", "-c", "echo \"$PYTEST_ADDOPTS\" > <archivo>"] corrida por _run_suite recibe --basetemp=<work>/pytest y conserva un PYTEST_ADDOPTS previo (-p no:cacheprovider); test_stale_integrate_dirs_are_removed_under_the_lock: con TMPDIR apuntando a tmp_path, una carpeta deskops-integrate-a con owner.pid de un pid muerto y una deskops-integrate-b sin owner.pid y mtime viejo se borran; una deskops-integrate-c con owner.pid = os.getpid() y la carpeta propia quedan. p2: implementar en deskops/integrate.py. p3: correr los tests del archivo y la suite con -n 4. p4: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_integrate.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar; cada falla se compara contra un worktree limpio de origin/main)

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos de tests/test_integrate.py pasan, el resto de tests/test_integrate.py sigue verde, y una corrida real de integrate deja los temporales de pytest dentro de su carpeta deskops-integrate-* (y por lo tanto los borra el finally).

FILE:deskops/integrate.py
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
            return 0
        except StepFailed as exc:
            result = f"fallo:{exc.step}"
            print(f"fallo: {exc.step}: {exc.detail}")
            return 1
    finally:
        for temp in temps:
            shutil.rmtree(temp, ignore_errors=True)
        _append_event(root, task_id, result if not (dry_run and result == "ok") else "dry-run", tip)
    verb = "simulado" if dry_run else "integrado"
    where = f"en PR a {cfg.branch}" if cfg.mode == "pr" else f"en {cfg.branch}"
    print(f"{verb} {code[:SHORT]} {tip[:SHORT]} {where}")
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

FILE:tests/test_integrate.py
"""`deskops integrate` against real git, a real desk and a bare remote in tmp_path."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from tests.activation_receipts import accept_receipts

ROOT = Path(__file__).resolve().parents[1]
TASK = "task-foo"
BRANCH = "main"


def _git(cwd: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=cwd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _cli(root: Path, *argv: str, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    full_env = {k: v for k, v in os.environ.items() if not k.startswith("DESKOPS_")}
    full_env["PYTHONPATH"] = str(ROOT) + os.pathsep + full_env.get("PYTHONPATH", "")
    full_env.update(env or {})
    result = subprocess.run([sys.executable, "-m", "deskops", *argv], cwd=root, capture_output=True, text=True, env=full_env)
    if check:
        assert result.returncode == 0, result.stderr or result.stdout
    return result


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _configure(root: Path, suite: list[str] | None = None, **extra: object) -> None:
    config_path = root / "desk" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["queue_min_available_gb"] = 0
    config["queue_max_psi_avg60"] = 101
    config["integrate"] = {
        "remote_url": str(root.parent / "remote.git"),
        "branch": BRANCH,
        "suite": suite or ["sh", "-c", "exit 0"],
        **extra,
    }
    config_path.write_text(json.dumps(config), encoding="utf-8")


def _build(tmp_path: Path) -> tuple[Path, Path]:
    """Build once (slow: real `deskops init` and lifecycle): (unclosed snapshot, closed repo), each with its remote."""
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q", "-b", BRANCH)
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _write(root / "seed.txt", "seed\n")
    _git(root, "add", "seed.txt")
    _git(root, "commit", "-q", "-m", "seed")
    _cli(root, "init", str(root))
    _cli(
        root, "add", "atom", "--root", str(root), "--title", "Integrate evidence", "--five-wh-one-plus", "what",
        "--answer", "The integration is exercised against a bare remote.",
    )
    _cli(
        root, "add", "task", "--root", str(root),
        json.dumps({"id": TASK, "title": "Foo", "goal": "g", "scope": "s", "implementation_path": "i",
                    "done_when": "d", "validation": ["pytest"], "task_type": "task.code"}),
    )
    accept_receipts(root, TASK)
    _write(root / "tests" / "test_smoke.py", "def test_smoke():\n    assert True\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "base")
    remote = tmp_path / "remote.git"
    _git(tmp_path, "init", "-q", "--bare", "-b", BRANCH, str(remote))
    _git(root, "push", "-q", str(remote), f"HEAD:{BRANCH}")

    _cli(root, "advance", "task", TASK, "--root", str(root))
    _cli(root, "advance", "task", TASK, "--root", str(root))
    _write(root / "feature.py", "VALUE = 1\n")
    _git(root, "add", "feature.py")
    _git(root, "commit", "-q", "-m", "feature")
    code = _git(root, "rev-parse", "HEAD")
    _cli(
        root, "edit", "task", TASK, "references",
        json.dumps(["desk/atoms/atom-integrate-evidence.md", "pytest tests/test_smoke.py::test_smoke", code]),
        "--root", str(root),
    )
    _cli(root, "edit", "task", TASK, "files", json.dumps(["desk/atoms/atom-integrate-evidence.md"]), "--root", str(root))
    unclosed = tmp_path.parent / (tmp_path.name + "-unclosed")
    shutil.copytree(tmp_path, unclosed, symlinks=True)
    _cli(root, "closeout", "verify", "--root", str(root), "--task", TASK, check=False)
    _cli(
        root, "closeout", "commit", "--root", str(root), "--task", TASK, "--no-run",
        "--reason", "integrate test", "--paths", "desk", ".sldb",
    )
    return unclosed, tmp_path


@pytest.fixture(scope="module")
def _templates(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, Path]:
    return _build(tmp_path_factory.mktemp("integrate-template"))


def _copy(template: Path, tmp_path: Path) -> Path:
    for name in ("repo", "remote.git"):
        shutil.copytree(template / name, tmp_path / name, symlinks=True)
    root = tmp_path / "repo"
    _configure(root)
    return root


@pytest.fixture
def closed(_templates: tuple[Path, Path], tmp_path: Path) -> Path:
    return _copy(_templates[1], tmp_path)


@pytest.fixture
def unclosed(_templates: tuple[Path, Path], tmp_path: Path) -> Path:
    return _copy(_templates[0], tmp_path)


def _integrate(root: Path, *extra: str, tmpdir: Path | None = None) -> subprocess.CompletedProcess[str]:
    tmp = tmpdir or root.parent / "tmpdir"
    tmp.mkdir(exist_ok=True)
    return _cli(root, "integrate", "--task", TASK, "--root", ".", *extra, env={"TMPDIR": str(tmp)}, check=False)


def _remote_head(root: Path) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "-q", BRANCH], cwd=root.parent / "remote.git", capture_output=True, text=True
    )
    return result.stdout.strip() or None


def _find(root: Path, subject: str) -> str:
    return _git(root, "log", "-1", "--format=%H", "--fixed-strings", f"--grep={subject}")


def _leftovers(root: Path) -> list[str]:
    return sorted(p.name for p in (root.parent / "tmpdir").iterdir())


def _events(root: Path) -> list[str]:
    return (root / "runs" / "hooks" / "events.log").read_text(encoding="utf-8").splitlines()


def test_green_gates_push_code_and_tip(closed: Path, tmp_path: Path) -> None:
    root = closed
    tip = _git(root, "rev-parse", "HEAD")
    assert _git(root, "log", "-1", "--format=%s") == f"closeout: {TASK}"
    code = _find(root, "feature")
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == f"integrado {code[:12]} {tip[:12]} en {BRANCH}"
    assert _remote_head(root) == tip
    remote = root.parent / "remote.git"
    assert _git(remote, "merge-base", "--is-ancestor", code, tip) == ""
    assert _events(root)[-1].endswith(f" {TASK} integrate ok {tip[:12]}")
    assert (root / "runs" / "queue" / "logs" / f"integrate-{TASK}.log").exists()
    assert _leftovers(root) == []


def test_task_from_env_is_equivalent(closed: Path, tmp_path: Path) -> None:
    root = closed
    tmp = tmp_path / "tmpdir"
    tmp.mkdir()
    result = _cli(root, "integrate", "--task-from-env", "--root", ".", env={"DESKOPS_TASK_ID": TASK, "TMPDIR": str(tmp)}, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.startswith("integrado ")
    assert _remote_head(root) == _git(root, "rev-parse", "HEAD")


def test_dry_run_leaves_the_remote_and_prints_both_pushes(closed: Path, tmp_path: Path) -> None:
    root = closed
    before = _remote_head(root)
    tip = _git(root, "rev-parse", "HEAD")
    code = _find(root, "feature")
    tools = tmp_path / "tools"
    _git(tmp_path, "clone", "-q", str(root.parent / "remote.git"), str(tools))
    tools_before = _git(tools, "rev-parse", "HEAD")
    _configure(root, tools_checkout=str(tools))
    result = _integrate(root, "--dry-run")
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"git push origin {code}:{BRANCH}" in result.stdout
    assert f"git push origin {tip}:{BRANCH}" in result.stdout
    assert result.stdout.index(code) < result.stdout.index(tip)
    assert _remote_head(root) == before
    assert _git(tools, "rev-parse", "HEAD") == tools_before
    assert _leftovers(root) == []


def test_tools_checkout_follows_the_remote_after_push(closed: Path, tmp_path: Path) -> None:
    root = closed
    tools = tmp_path / "tools"
    _git(tmp_path, "clone", "-q", str(root.parent / "remote.git"), str(tools))
    _configure(root, tools_checkout=str(tools))
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(tools, "rev-parse", "HEAD") == _git(root, "rev-parse", "HEAD")


def test_failing_suite_stops_before_any_push(closed: Path, tmp_path: Path) -> None:
    root = closed
    before = _remote_head(root)
    _configure(root, suite=["sh", "-c", "echo roto; exit 1"])
    result = _integrate(root)
    assert result.returncode == 1
    assert "fallo: suite: " in result.stdout
    assert _remote_head(root) == before
    assert "roto" in (root / "runs" / "queue" / "logs" / f"integrate-{TASK}.log").read_text(encoding="utf-8")
    assert " integrate fallo:suite " in _events(root)[-1]
    assert _leftovers(root) == []


def test_suite_timeout_is_reported(closed: Path, tmp_path: Path) -> None:
    root = closed
    _configure(root, suite=["sh", "-c", "sleep 30"], suite_timeout=1)
    result = _integrate(root)
    assert result.returncode == 1
    assert "fallo: suite: timeout tras 1 s" in result.stdout


def test_suite_runs_under_the_declared_lock_with_pythonpath_of_the_copy(closed: Path, tmp_path: Path) -> None:
    root = closed
    probe = tmp_path / "probe.txt"
    lock = tmp_path / "locks" / "tests.lock"
    _configure(root, suite=["sh", "-c", f'echo "$PYTHONPATH" > {probe}'], tests_lock=str(lock))
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert lock.exists()
    assert probe.read_text(encoding="utf-8").strip().startswith(str(tmp_path / "tmpdir"))


def test_range_touching_only_desk_does_not_run_the_suite(closed: Path, tmp_path: Path) -> None:
    root = closed
    # The remote already has the code commit: what is left to publish is only the closeout (desk, .sldb, runs).
    code = _find(root, "feature")
    _git(root, "push", "-q", str(root.parent / "remote.git"), f"{code}:{BRANCH}")
    _configure(root, suite=["sh", "-c", "exit 1"])
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "integrado " in result.stdout
    assert not (root / "runs" / "queue" / "logs" / f"integrate-{TASK}.log").exists()


def test_code_already_behind_origin_main_is_not_pushed(closed: Path, tmp_path: Path) -> None:
    root = closed
    tip = _git(root, "rev-parse", "HEAD")
    code = _find(root, "feature")
    # origin/main is ahead of the code commit (it holds a descendant): pushing code:main would be non-fast-forward.
    # Rebuild the tip on top of an extra empty commit that the remote already has.
    extra = _git(root, "commit-tree", f"{code}^{{tree}}", "-p", code, "-m", "other task tip")
    tip = _git(root, "commit-tree", f"{tip}^{{tree}}", "-p", extra, "-m", f"closeout: {TASK}")
    _git(root, "reset", "-q", "--hard", tip)
    _configure(root)
    _git(root, "push", "-q", str(root.parent / "remote.git"), f"{extra}:{BRANCH}")
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"código ya en origin: {code[:12]}" in result.stdout
    assert result.stdout.strip().splitlines()[-1] == f"integrado {code[:12]} {tip[:12]} en {BRANCH}"
    assert _remote_head(root) == tip


def test_a_tip_that_is_not_fast_forward_fails(closed: Path, tmp_path: Path) -> None:
    root = closed
    side = tmp_path / "side"
    _git(tmp_path, "clone", "-q", str(root.parent / "remote.git"), str(side))
    _git(side, "config", "user.email", "o@example.com")
    _git(side, "config", "user.name", "Other")
    _git(side, "commit", "-q", "--allow-empty", "-m", "elsewhere")
    _git(side, "push", "-q", "origin", f"HEAD:{BRANCH}")
    before = _remote_head(root)
    result = _integrate(root)
    assert result.returncode == 1
    assert "fallo: fast-forward" in result.stdout
    assert _remote_head(root) == before
    assert _leftovers(root) == []


def test_a_store_path_missing_in_the_commit_fails(closed: Path, tmp_path: Path) -> None:
    root = closed
    store_path = root / ".sldb" / "store.yaml"
    store = yaml.safe_load(store_path.read_text(encoding="utf-8"))
    store["links"] = [*store.get("links", []), {"name": "ghost", "path": "ghost/absent.yaml"}]
    store_path.write_text(yaml.safe_dump(store, sort_keys=False), encoding="utf-8")
    _git(root, "add", ".sldb/store.yaml")
    _git(root, "commit", "-q", "--amend", "--no-edit")
    before = _remote_head(root)
    result = _integrate(root)
    assert result.returncode == 1
    assert "fallo: store: " in result.stdout and "ghost/absent.yaml" in result.stdout
    assert _remote_head(root) == before


def test_an_unclosed_task_exits_2(unclosed: Path, tmp_path: Path) -> None:
    root = unclosed
    result = _integrate(root)
    assert result.returncode == 2
    assert "no esta cerrada" in result.stdout
    assert not (root / "runs" / "hooks" / "events.log").exists()


def test_a_closed_task_without_code_commit_exits_2(unclosed: Path, tmp_path: Path) -> None:
    root = unclosed
    _cli(root, "edit", "task", TASK, "references", json.dumps(["desk/atoms/atom-integrate-evidence.md"]), "--root", str(root))
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "refs")
    _git(root, "commit", "-q", "--allow-empty", "-m", f"closeout: {TASK}")
    _git(root, "rm", "-q", "-f", f"desk/tasks/{TASK}.md")
    _git(root, "commit", "-q", "--amend", "--no-edit")
    result = _integrate(root)
    assert result.returncode == 2
    assert "falta el commit de codigo en references" in result.stdout


def test_missing_integrate_field_exits_2(closed: Path, tmp_path: Path) -> None:
    root = closed
    config_path = root / "desk" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    del config["integrate"]
    config_path.write_text(json.dumps(config), encoding="utf-8")
    result = _integrate(root)
    assert result.returncode == 2
    assert "falta el campo integrate en desk/config.json" in result.stdout


@pytest.mark.parametrize(
    "argv, env",
    [
        ([], {}),
        (["--task", TASK, "--task-from-env"], {"DESKOPS_TASK_ID": TASK}),
        (["--task-from-env"], {"DESKOPS_TASK_ID": ""}),
    ],
)
def test_task_selection_errors_exit_2(closed: Path, argv: list[str], env: dict[str, str]) -> None:
    root = closed
    result = _cli(root, "integrate", *argv, "--root", ".", env=env, check=False)
    assert result.returncode == 2, result.stdout + result.stderr


def test_memory_gate_fails_the_first_step(closed: Path, tmp_path: Path) -> None:
    root = closed
    config_path = root / "desk" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["queue_min_available_gb"] = 100000
    config_path.write_text(json.dumps(config), encoding="utf-8")
    result = _integrate(root)
    assert result.returncode == 1
    assert "fallo: memoria: " in result.stdout
    assert _remote_head(root) != _git(root, "rev-parse", "HEAD")
    assert _leftovers(root) == []


def test_push_env_reaches_the_push_commands(closed: Path, tmp_path: Path) -> None:
    root = closed
    hooks = tmp_path / "remote.git" / "hooks"
    marker = tmp_path / "marker.txt"
    hook = hooks / "pre-receive"
    hook.write_text(f'#!/bin/sh\necho "$INTEGRATE_MARK" >> {marker}\n', encoding="utf-8")
    hook.chmod(0o755)
    _configure(root, push_env={"INTEGRATE_MARK": "visible"})
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert marker.read_text(encoding="utf-8").split() == ["visible", "visible"]


def test_a_tip_already_on_the_remote_is_a_noop(closed: Path, tmp_path: Path) -> None:
    root = closed
    tip = _git(root, "rev-parse", "HEAD")
    first = _integrate(root)
    assert first.returncode == 0, first.stdout + first.stderr
    second = _integrate(root)
    assert second.returncode == 0, second.stdout + second.stderr
    assert second.stdout.strip() == f"ya integrado: {tip[:12]}"
    assert _remote_head(root) == tip
    assert _events(root)[-1].endswith(f" {TASK} integrate ya-integrado {tip[:12]}")
    assert _leftovers(root) == []


def _dangling_closeout(root: Path) -> str:
    """Amend the closeout commit so it carries a task with a dangling file reference; returns the tip."""
    other = {"id": "task-old", "title": "Old", "goal": "g", "scope": "s", "implementation_path": "i",
             "done_when": "d", "validation": ["pytest"], "task_type": "task.code"}
    _cli(root, "add", "task", "--root", str(root), json.dumps(other))
    _cli(root, "edit", "task", "task-old", "files", json.dumps(["desk/ghost-absent.md"]), "--root", str(root))
    _git(root, "add", "desk", ".sldb")
    _git(root, "commit", "-q", "--amend", "--no-edit")
    return _git(root, "rev-parse", "HEAD")


def test_tip_extends_over_later_desk_only_commits(closed: Path, tmp_path: Path) -> None:
    root = closed
    tip = _dangling_closeout(root)
    before = _remote_head(root)
    failed = _integrate(root)
    assert failed.returncode == 1 and "fallo: graph" in failed.stdout
    assert _remote_head(root) == before
    _cli(root, "edit", "task", "task-old", "files", json.dumps([]), "--root", str(root))
    _git(root, "add", "desk", ".sldb")
    _git(root, "commit", "-q", "-m", "desk: retire dangling reference")
    head = _git(root, "rev-parse", "HEAD")
    assert head != tip
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"tip extendido a {head[:12]}: solo commits de desk" in result.stdout
    assert _remote_head(root) == head


def _remote_code_commit(root: Path) -> None:
    """Another person pushes a code commit to the bare remote."""
    other = root.parent / "other"
    _git(root.parent, "clone", "-q", str(root.parent / "remote.git"), str(other))
    _write(other / "src" / "remote_code.py", "R = 1\n")
    _git(other, "add", "src/remote_code.py")
    _git(other, "commit", "-q", "-m", "remote code")
    _git(other, "push", "-q", "origin", f"HEAD:{BRANCH}")


def test_tip_extends_over_a_merge_of_the_remote_branch(closed: Path, tmp_path: Path) -> None:
    root = closed
    _dangling_closeout(root)
    _remote_code_commit(root)
    _git(root, "fetch", "-q", str(root.parent / "remote.git"), BRANCH)
    _git(root, "merge", "-q", "--no-ff", "-m", "merge remote", "FETCH_HEAD")
    _cli(root, "edit", "task", "task-old", "files", json.dumps([]), "--root", str(root))
    _git(root, "add", "desk", ".sldb")
    _git(root, "commit", "-q", "-m", "desk: retire dangling reference")
    head = _git(root, "rev-parse", "HEAD")
    result = _integrate(root, "--dry-run")
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"tip extendido a {head[:12]}: solo commits de desk" in result.stdout
    assert "fast-forward" not in result.stdout


def test_code_commit_that_is_not_fast_forward_rides_with_the_tip(closed: Path, tmp_path: Path) -> None:
    root = closed
    _dangling_closeout(root)
    code = _find(root, "feature")
    _remote_code_commit(root)
    _git(root, "fetch", "-q", str(root.parent / "remote.git"), BRANCH)
    _git(root, "merge", "-q", "--no-ff", "-m", "merge remote", "FETCH_HEAD")
    _cli(root, "edit", "task", "task-old", "files", json.dumps([]), "--root", str(root))
    _git(root, "add", "desk", ".sldb")
    _git(root, "commit", "-q", "-m", "desk: retire dangling reference")
    head = _git(root, "rev-parse", "HEAD")
    result = _integrate(root)
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"código va con el tip: {code[:12]}" in result.stdout
    assert _remote_head(root) == head
    assert _git(root.parent / "remote.git", "merge-base", "--is-ancestor", code, head) == ""


def test_tip_stays_when_a_local_code_commit_follows_a_remote_merge(closed: Path, tmp_path: Path) -> None:
    root = closed
    _dangling_closeout(root)
    _remote_code_commit(root)
    _git(root, "fetch", "-q", str(root.parent / "remote.git"), BRANCH)
    _git(root, "merge", "-q", "--no-ff", "-m", "merge remote", "FETCH_HEAD")
    _write(root / "src" / "local_code.py", "L = 1\n")
    _git(root, "add", "src/local_code.py")
    _git(root, "commit", "-q", "-m", "local code")
    result = _integrate(root, "--dry-run")
    assert "tip extendido" not in result.stdout


def test_tip_stays_at_closeout_when_a_later_commit_touches_code(closed: Path, tmp_path: Path) -> None:
    root = closed
    tip = _dangling_closeout(root)
    _write(root / "src" / "later.py", "X = 1\n")
    _git(root, "add", "src/later.py")
    _git(root, "commit", "-q", "-m", "later code")
    result = _integrate(root)
    assert "tip extendido" not in result.stdout
    assert result.returncode == 1 and "fallo: graph" in result.stdout
    assert _remote_head(root) != tip


# --- mode pr: remote with a protected dev and a fake gh -----------------------

FAKE_GH = """#!{python}
import json, os, sys
with open(os.environ["FAKE_GH_LOG"], "a") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
if sys.argv[1:3] == ["pr", "list"]:
    print(os.environ.get("FAKE_GH_EXISTING", ""))
elif sys.argv[1:3] == ["pr", "create"]:
    print("https://example.test/org/repo/pull/7")
"""


def _pr_setup(root: Path, tmp_path: Path) -> tuple[Path, Path, dict[str, str]]:
    remote = root.parent / "remote.git"
    base_commit = _find(root, "base")
    _git(remote, "update-ref", "refs/heads/dev", base_commit)
    hook = remote / "hooks" / "pre-receive"
    hook.write_text('#!/bin/sh\nwhile read old new ref; do [ "$ref" = refs/heads/dev ] && { echo protected >&2; exit 1; }; done\nexit 0\n')
    hook.chmod(0o755)
    _git(root, "branch", "dev", base_commit)
    _git(root, "checkout", "-q", "-B", f"task/{TASK}", BRANCH)
    _configure(root, mode="pr", branch="dev")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    gh = bin_dir / "gh"
    gh.write_text(FAKE_GH.format(python=sys.executable))
    gh.chmod(0o755)
    log = tmp_path / "gh.log"
    return remote, log, {"PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}", "FAKE_GH_LOG": str(log)}


def _integrate_env(root: Path, extra: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
    tmp = root.parent / "tmpdir"
    tmp.mkdir(exist_ok=True)
    return _cli(root, "integrate", "--task", TASK, "--root", ".", *args, env={"TMPDIR": str(tmp), **extra}, check=False)


def test_pr_mode_pushes_the_task_branch_and_opens_the_pr_leaving_dev_alone(closed: Path, tmp_path: Path) -> None:
    root = closed
    remote, log, env = _pr_setup(root, tmp_path)
    tip = _git(root, "rev-parse", "HEAD")
    dev_before = _git(remote, "rev-parse", "dev")
    local_dev = _git(root, "rev-parse", "dev")
    result = _integrate_env(root, env)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PR: https://example.test/org/repo/pull/7" in result.stdout
    assert _git(remote, "rev-parse", f"task/{TASK}") == tip
    assert _git(remote, "rev-parse", "dev") == dev_before
    assert _git(root, "rev-parse", "dev") == local_dev
    calls = [json.loads(line) for line in log.read_text().splitlines()]
    create = next(c for c in calls if c[:2] == ["pr", "create"])
    assert create[create.index("--base") + 1] == "dev"
    assert create[create.index("--head") + 1] == f"task/{TASK}"
    assert create[create.index("--title") + 1] == "Foo"
    assert TASK in create[create.index("--body") + 1]
    assert _leftovers(root) == []


def test_pr_mode_with_an_open_pr_only_pushes(closed: Path, tmp_path: Path) -> None:
    root = closed
    remote, log, env = _pr_setup(root, tmp_path)
    env["FAKE_GH_EXISTING"] = "https://example.test/org/repo/pull/3"
    result = _integrate_env(root, env)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PR: https://example.test/org/repo/pull/3" in result.stdout
    assert not any(json.loads(line)[:2] == ["pr", "create"] for line in log.read_text().splitlines())
    assert _git(remote, "rev-parse", f"task/{TASK}") == _git(root, "rev-parse", "HEAD")


def test_pr_mode_dry_run_pushes_nothing(closed: Path, tmp_path: Path) -> None:
    root = closed
    remote, log, env = _pr_setup(root, tmp_path)
    result = _integrate_env(root, env, "--dry-run")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "dry-run: gh pr create --base dev" in result.stdout
    assert _git(remote, "branch", "--list", "task/*") == ""
    assert not log.exists()

FILE:instruccion
Cold-bundle de la tarea task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_integrate.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar; cada falla se compara contra un worktree limpio de origin/main)

