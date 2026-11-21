"""Scion dispatch: `deskops dispatch {start|reap}`.

Chains the deterministic steps of launching the executor or tester of one task
(identity, template, prompt, `scion start`) and of collecting the finished ones
(`scion stop` + `scion delete`). Every call to scion goes through `_scion`.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import shlex
import subprocess
from pathlib import Path
from typing import Any

from deskops.config import DeskConfig, DispatchConfig
from deskops.errors import UsageError

EXIT_BUSY = 3
EXIT_ALIVE = 4
EXIT_NO_ATTEMPTS = 5
EXIT_SCION_ERROR = 6
EXIT_WORKTREE = 8
WORKTREES_DIR = ".worktrees"
DONE_ACTIVITIES = ("completed", "blocked", "limits_exceeded")


def _scion(argv: list[str]) -> subprocess.CompletedProcess[str]:
    """The only place that runs scion."""
    return subprocess.run(argv, capture_output=True, text=True)


def _dispatch_config(root: Path) -> DispatchConfig:
    config = DeskConfig.load(root / "desk")
    if config.dispatch is None:
        raise UsageError("falta el campo dispatch en desk/config.json")
    return config.dispatch


def _roles_root(root: Path, cfg: DispatchConfig) -> Path:
    """Repo whose desk/roles holds the RoleDocs (default: the task root), absolute."""
    if not cfg.roles_root:
        return root
    path = Path(cfg.roles_root).expanduser()
    if not path.is_absolute():
        path = root / path
    return path.resolve()


def _task_repo(root: Path) -> str:
    config = DeskConfig.load(root / "desk")
    if "project_identity" in config.model_fields_set:
        return config.project_identity
    return root.name


def _task_path(root: Path, task_id: str) -> Path:
    path = root / "desk" / "tasks" / f"{task_id}.md"
    if not path.is_file():
        raise UsageError(f"tarea no encontrada: {task_id}")
    return path


def _list_agents(cfg: DispatchConfig) -> list[dict[str, Any]]:
    result = _scion(["scion", "list", "--project", cfg.project, "--format", "json"])
    if result.returncode != 0:
        raise UsageError(f"scion list fallo ({result.returncode}): {result.stderr.strip()}")
    try:
        data = json.loads(result.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise UsageError(f"scion list no devolvio JSON: {exc}") from exc
    if isinstance(data, dict):
        data = data.get("agents") or []
    return [item for item in data if isinstance(item, dict)]


def _git(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    # Messages are parsed (e.g. "would be overwritten"), so git must not localize them.
    env = {**os.environ, "LC_ALL": "C", "LANGUAGE": ""}
    return subprocess.run(
        ["git", "-c", "core.quotepath=false", *argv], cwd=root, capture_output=True, text=True,
        stdin=subprocess.DEVNULL, env=env,
    )


def _git_error(result: subprocess.CompletedProcess[str]) -> str:
    return " ".join((result.stderr.strip() or result.stdout.strip() or f"codigo {result.returncode}").split())


def _base_branch(root: Path) -> str:
    """Local branch the executor branches start from and reap integrates into."""
    integrate = DeskConfig.load(root / "desk").integrate
    return integrate.branch if integrate is not None else "main"


def _agent_branch(name: str) -> str:
    return f"deskops/{name}"


def _worktree_path(root: Path, name: str) -> Path:
    return root / WORKTREES_DIR / name


def _check_on_base(root: Path, base: str) -> str | None:
    """Error text when the main checkout is not on ``base``, else None."""
    head = _git(root, "rev-parse", "--abbrev-ref", "HEAD")
    if head.returncode != 0:
        return f"{root} no es un repo git: {_git_error(head)}"
    if head.stdout.strip() != base:
        return f"el checkout principal esta en '{head.stdout.strip()}', no en '{base}'"
    return None


def _ignore_worktrees(root: Path) -> None:
    """Add ``.worktrees/`` to the local ``info/exclude`` (not versioned) when missing."""
    located = _git(root, "rev-parse", "--git-path", "info/exclude")
    if located.returncode != 0:
        return
    exclude = Path(located.stdout.strip())
    if not exclude.is_absolute():
        exclude = root / exclude
    line = f"{WORKTREES_DIR}/"
    current = exclude.read_text(encoding="utf-8") if exclude.is_file() else ""
    if line in current.splitlines():
        return
    exclude.parent.mkdir(parents=True, exist_ok=True)
    exclude.write_text(current + ("" if not current or current.endswith("\n") else "\n") + line + "\n", encoding="utf-8")


def _remove_worktree(root: Path, name: str) -> subprocess.CompletedProcess[str] | None:
    """Remove the worktree and branch of an agent; the failing git result, or None."""
    path = _worktree_path(root, name)
    if path.exists():
        removed = _git(root, "worktree", "remove", "--force", str(path))
        if removed.returncode != 0:
            return removed
    deleted = _git(root, "branch", "-D", _agent_branch(name))
    return deleted if deleted.returncode != 0 else None


def _integrate_branch(root: Path, name: str) -> tuple[int, str]:
    """Bring the commits of ``deskops/<name>`` onto the local base branch, then drop worktree and branch.

    Returns (0, "") when there was nothing to do or it went through, else (code, message)
    leaving worktree and branch in place.
    """
    branch = _agent_branch(name)
    if _git(root, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}").returncode != 0:
        return 0, ""
    base = _base_branch(root)
    problem = _check_on_base(root, base)
    if problem:
        return EXIT_WORKTREE, f"{problem}: no se integra {branch}"
    pending = _git(root, "rev-list", "--reverse", "--cherry-pick", "--right-only", "--no-merges", f"{base}...{branch}")
    if pending.returncode != 0:
        return EXIT_WORKTREE, f"git rev-list {base}...{branch}: {_git_error(pending)}"
    commits = pending.stdout.split()
    if commits:
        failure = _commit_run_store(root, [name])
        if failure:
            return EXIT_WORKTREE, f"no se pudo commitear el RunDoc de {name}: {failure}"
        if _git(root, "merge-base", "--is-ancestor", base, branch).returncode == 0:
            picked = _git(root, "merge", "--ff-only", "-q", branch)  # keeps the executor's shas
        else:
            picked = _git(root, "cherry-pick", *commits)
            if picked.returncode != 0:
                _git(root, "cherry-pick", "--abort")
        if picked.returncode != 0:
            return EXIT_WORKTREE, f"conflicto al traer {branch} a {base}: {_dirty_overwrite_hint(root, base, branch, _git_error(picked))}"
    failed = _remove_worktree(root, name)
    if failed is not None:
        return EXIT_WORKTREE, f"no se pudo borrar el worktree de {name}: {_git_error(failed)}"
    return 0, f"integrado {len(commits)} commit(s) de {branch} en {base}"


_STORE_RUN_PATHS = (
    ".sldb/store.yaml",
    ".sldb/core/store_index.yaml",
    ".sldb/core/models/RunDoc.yaml",
)


def _run_store_paths(root: Path, name: str) -> list[str]:
    """Store files ``record_scion_run`` touches for agent ``name`` (only the ones that exist).

    Includes the run dir's ``run.md`` (the RunDoc's tracked file), so a committed RunDoc always has it.
    """
    from deskops.runtime.scion import _slug

    shard = f".sldb/core/documents/RunDoc/run-{_slug(name)}.yaml"
    run_docs = [f"{_run_dir_for(name, role)}/run.md" for role in ("executor", "tester")]
    return [rel for rel in (*_STORE_RUN_PATHS, shard, *run_docs) if (root / rel).exists()]


def _commit_run_store(root: Path, names: list[str]) -> str:
    """Commit, with pathspec, the RunDoc store files and run.md of ``names`` that are still uncommitted.

    Returns "" on success or nothing to do, else the git error. Other dirty files are untouched.
    """
    paths: list[str] = []
    for name in names:
        paths += [p for p in _run_store_paths(root, name) if p not in paths]
    if not paths:
        return ""
    dirty = _git(root, "status", "--porcelain", "--", *paths)
    if dirty.returncode != 0:
        return _git_error(dirty)
    if not dirty.stdout.strip():
        return ""
    added = _git(root, "add", "--", *paths)
    if added.returncode != 0:
        return _git_error(added)
    done = _git(root, "commit", "-q", "-m", f"run: {', '.join(names)}", "-m", "[skip ci]", "--", *paths)
    return "" if done.returncode == 0 else _git_error(done)


def _dirty_overwrite_hint(root: Path, base: str, branch: str, message: str) -> str:
    """When git refused because local changes would be overwritten, name the files and say to commit them."""
    if "sobrescrit" not in message and "overwritten" not in message:
        return message
    touched = _git(root, "diff", "--name-only", f"{base}...{branch}")
    dirty = _git(root, "status", "--porcelain", "-uno")
    changed = {line[3:].strip() for line in dirty.stdout.splitlines() if len(line) > 3}
    files = sorted(changed & set(touched.stdout.split()))
    listed = ", ".join(files) if files else "ver git status"
    return f"{message} (commitea o descarta antes estos cambios locales del checkout principal: {listed})"


def _run_dir_for(name: str, role: str) -> str:
    return f"runs/subagents/exec-{name}" + ("-testing" if role == "tester" else "")


def _quick_gates_text(role: str, quick_gates: list[str] | None) -> str:
    if not quick_gates:
        return ""
    command = shlex.join(quick_gates)
    if role == "executor":
        return (
            "\n## Gates rapidos del desk\n\n"
            "Antes del commit corre, con el python del venv (/tmp/ws-venv en PATH):\n\n"
            f"    {command}\n\n"
            "Debe terminar con rc 0 antes de commitear; si falla, corrige y repite. "
            "Anota el comando y su rc en validation.log.\n"
        )
    return (
        "\n## Gates rapidos del desk\n\n"
        "Antes del veredicto corre, con el python del venv (/tmp/ws-venv en PATH):\n\n"
        f"    {command}\n\n"
        "Si termina con rc distinto de 0 el veredicto es FALLA.\n"
    )


def _worktree_text(worktree: Path | None, root: Path) -> str:
    if worktree is None:
        return ""
    return (
        "\n## Tu worktree\n\n"
        f"Tu codigo vive en un worktree propio, en la rama `deskops/{worktree.name}`:\n\n"
        f"    {worktree}\n\n"
        "Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout "
        f"principal {root}. Las operaciones de desk (`deskops ... --root {root}`, evidencia en "
        "runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. "
        "Al terminar, reap trae tus commits a la rama principal y borra el worktree.\n"
    )


def _role_instructions(
    role: str, task_id: str, quick_gates: list[str] | None = None,
    worktree: Path | None = None, root: Path | None = None,
) -> str:
    return (
        _base_instructions(role, task_id)
        + _quick_gates_text(role, quick_gates)
        + (_worktree_text(worktree, root) if root is not None else "")
    )


def _base_instructions(role: str, task_id: str) -> str:
    if role == "executor":
        return (
            "## Entrega del ejecutor\n\n"
            "Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno "
            "(los mismos que listas en result-summary.md):\n\n"
            "    git add <ruta> <ruta> ...\n"
            f"    git commit -m \"<resumen>\" -m \"Task-Id: {task_id}\"\n\n"
            "Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo "
            "ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.\n"
        )
    if role == "tester":
        return (
            "## Como probar (tester)\n\n"
            "Ubica el trabajo del ejecutor:\n\n"
            f"    git log -1 --format=%H --grep \"Task-Id: {task_id}\"   # commit del ejecutor\n"
            "    git show --name-only <commit>                           # sus archivos\n\n"
            "Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py "
            "cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. "
            "No corras la suite completa: la corre integrate en el host.\n\n"
            "Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.\n"
        )
    return ""


def start(root: Path, role: str, task_id: str) -> int:
    from deskops.cli.main import main as deskops_main
    from deskops.runtime.scion import (
        find_role_doc,
        load_scion_context,
        materialize_scion_template,
        record_scion_run,
        scion_child_identity,
        scion_start_argv,
    )

    cfg = _dispatch_config(root)
    role_cfg = getattr(cfg.roles, role)
    task_path = _task_path(root, task_id)

    from deskops.queue import wait_reason

    reason = wait_reason(DeskConfig.load(root / "desk"))
    if reason:
        print(f"ocupado: {reason}")
        return EXIT_BUSY

    identity = scion_child_identity(task_path, role, 1)
    for agent in _list_agents(cfg):
        if agent.get("phase") == "running" and str(agent.get("name", "")).startswith(identity["name"]):
            print(f"ocupado: la tarea ya tiene agente {agent.get('name')}")
            return EXIT_BUSY

    run_dir = _run_dir_for(identity["name"], role)
    if (root / run_dir).exists():
        identity = scion_child_identity(task_path, role, 2)
        run_dir = _run_dir_for(identity["name"], role)
        if (root / run_dir).exists():
            print(f"sin intentos: {task_id} {role}")
            return EXIT_NO_ATTEMPTS
    name = identity["name"]

    worktree: Path | None = None
    if role == "executor":
        base = _base_branch(root)
        problem = _check_on_base(root, base)
        if problem:
            print(f"worktree: {problem}; no se lanza")
            return EXIT_WORKTREE
        worktree = _worktree_path(root, name)

    roles_root = _roles_root(root, cfg)
    _, role_doc = find_role_doc(roles_root, role_cfg.role)
    role_name = str(role_doc["name"])
    context = load_scion_context(Path(cfg.context_file).expanduser())
    target = Path(cfg.templates_dir).expanduser() / role_name
    materialize_scion_template(
        roles_root,
        role_cfg.role,
        task_repo=_task_repo(root),
        harness=role_cfg.harness,
        out_dir=target,
        model_alias=role_cfg.model_alias,
        mode=role,
        context=context,
        harness_auth=role_cfg.harness_auth,
    )
    # A RunDoc left tracked by another session whose run_dir is gone is stale: untrack it
    # so the new run can track the same identity (a RunDoc with its run_dir counts as an attempt).
    from deskops.runtime.scion import _slug

    from deskops import doc_access

    doc_access.untrack_doc(root, f"run-{_slug(name)}")
    try:
        record_scion_run(
            root,
            task_id=task_id,
            role_id=str(role_doc["id"]),
            kind=role_cfg.harness,
            agent_slug=name,
            run_dir=run_dir,
        )
    except Exception:
        leftover = root / run_dir
        if leftover.is_dir() and not any(leftover.iterdir()):
            leftover.rmdir()
        raise
    failure = _commit_run_store(root, [name])
    if failure:
        print(f"aviso: no se pudo commitear el RunDoc de {name}: {failure}")

    sync = _scion(["scion", "templates", "sync", str(target.resolve()), "--project", cfg.project])
    if sync.returncode != 0:
        print(f"scion templates sync fallo ({sync.returncode}): {sync.stderr.strip()}")
        return sync.returncode

    shown = io.StringIO()
    with contextlib.redirect_stdout(shown):
        deskops_main(["show", "task", task_id, "--root", str(root)])
    prompt_path = (root / run_dir / "prompt.md").resolve()
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(
        shown.getvalue().rstrip("\n")
        + "\n\n"
        + task_path.read_text(encoding="utf-8").rstrip("\n")
        + "\n\n"
        + _role_instructions(role, task_id, cfg.quick_gates, worktree, root),
        encoding="utf-8",
    )

    if worktree is not None:
        _ignore_worktrees(root)
        created = _git(root, "worktree", "add", "-q", "-b", _agent_branch(name), str(worktree), base)
        if created.returncode != 0:
            print(f"worktree: git worktree add fallo: {_git_error(created)}")
            return EXIT_WORKTREE

    argv = scion_start_argv(
        identity,
        prompt=(
            f"Tu encargo esta en el archivo {prompt_path}. "
            "Lee el archivo completo antes de empezar y luego cumple el encargo que describe."
        ),
        project=cfg.project,
        workspace=cfg.workspace,
        template=role_name,
        harness_auth=role_cfg.harness_auth,
    )
    if role_cfg.env_config:
        argv += ["--config", role_cfg.env_config]
    started = _scion(argv)
    if started.returncode != 0:
        print(started.stderr.strip())
        if worktree is not None:
            _remove_worktree(root, name)
    print(f"agente {name} run_dir {run_dir}")
    return started.returncode


def reap(root: Path, task_id: str) -> int:
    from deskops.runtime.scion import _scion_task_label

    cfg = _dispatch_config(root)
    label = _scion_task_label(task_id)  # no TaskDoc read: the task may be closed already
    alive = 0
    failed = False
    conflict = False
    for agent in _list_agents(cfg):
        labels = agent.get("labels") or {}
        if labels.get("deskops.task_id") != label:
            continue
        name = str(agent.get("name"))
        role = str(labels.get("deskops.role", ""))
        phase = str(agent.get("phase", ""))
        activity = str(agent.get("activity", ""))
        reason = ""
        if phase != "running":
            reason = f"phase:{phase}"
        elif activity in DONE_ACTIVITIES:
            reason = f"activity:{activity}"
        elif (root / _run_dir_for(name, role) / "result-summary.md").exists():
            reason = "result-summary"
        if not reason:
            print(f"{name} {role} vivo")
            alive += 1
            continue
        stopped = _scion(["scion", "stop", name, "--project", cfg.project])
        if stopped.returncode != 0:
            print(f"{name} {role} error:{stopped.returncode}")
            failed = True
            continue
        deleted = _scion(["scion", "delete", name, "--project", cfg.project, "--yes"])
        if deleted.returncode != 0:
            print(f"{name} {role} error:{deleted.returncode}")
            failed = True
            continue
        print(f"{name} {role} {reason}")
        if role == "executor":
            code, message = _integrate_branch(root, name)
            if message:
                print(f"{name} {message}")
            if code:
                conflict = True
    if alive:
        return EXIT_ALIVE
    if conflict:
        return EXIT_WORKTREE
    return EXIT_SCION_ERROR if failed else 0


class DispatchCLI:
    """`deskops dispatch {start|reap}`; the subcommand is required."""

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        cmd = args.dispatch_command
        if cmd == "start":
            return start(root, args.agent_role, args.task)
        if cmd == "reap":
            return reap(root, args.task)
        raise UsageError(f"Unknown dispatch command: {cmd}")
