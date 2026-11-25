FILE:desk/tasks/task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar.md
---
sldb:
  by: agent
  at: '2026-11-23T04:38:38Z'
  authority: generated
  via: create_document
id: task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-234509-suggestion-seguridad-todo-agente-claude-del-broker-recibe-sldb-1-y-dev-shm-en-escritura-sea-del-proyecto-que-sea.md
depends_on:
- task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale
pills: []
files:
- deskops/dispatch.py
- docs/operator-manual.md
- tests/test_dispatch.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# dispatch start se niega a lanzar un rol cuyo env_config no declara volumes propios, para poder quitar el montaje global de SLDB_1 y /dev/shm de los agentes claude

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261122-234509 (scion-coordination, medido el 2026-11-23): todo agente claude del broker recibe /mnt/ssd/proyectos/SLDB_1 y /dev/shm montados en escritura, 6 Gi y red del host, sea del proyecto que sea, aunque se pase otro --config: viene de profiles.local.harness_overrides.claude en el settings.yaml de scion del usuario (piloto IR). Un agente de mepu, ftcourier o un desk de heyantonia puede escribir en deskops y sldb; Governance lo marca como bloqueante para usar scion con sus desks. Quitar ese montaje global es decisión de JP y lo ejecuta scion-coordination en ventana, no esta tarea. ORDEN: esta tarea no corre antes de que cierre task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale, es decir, antes de que las plantillas deskops-executor y deskops-tester declaren sus propios volumes en su --config; si no, al quitar el montaje global los ejecutores y testers se quedan sin workspace.

## Goal

_Describe the concrete result this task must produce._

(1) deskops dispatch start lee el env_config del rol (DispatchRole.env_config) antes de lanzar; si el archivo no existe, no declara volumes, o ninguno de sus volumes contiene cfg.workspace, no lanza, imprime "env_config <ruta> no declara un volume que contenga <workspace>" y sale con un código distinto de 0 (no reintentable por la cola). (2) deskops doctor avisa lo mismo para cada rol de dispatch del desk. (3) docs/operator-manual.md, en la sección de despacho, dice que cada rol declara sus volumes y que el montaje global de scion se retira (por decisión de JP) una vez que todos los desks despachados lo hacen.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/dispatch.py, el chequeo de doctor, docs/operator-manual.md, tests/test_dispatch.py y el test de doctor que corresponda. No entra: editar el settings.yaml de scion ni reiniciar el server (scion-coordination, en ventana, con OK de JP), los env_config de .bootstrap (son de la máquina), el piloto wf-desks (declara sus propios volumes aparte).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_dispatch.py con scion falso: test_start_refuses_role_without_volumes, test_start_refuses_volumes_that_do_not_cover_workspace, test_start_launches_when_volumes_cover_workspace. p2: test de doctor con un env_config sin volumes. p3: implementar. p4: suite con -n 4. p5: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_dispatch.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_doctor_alerts.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan; con el desk/config.json real de deskops y los env_config de .bootstrap ya con volumes (de la tarea runtime-template), deskops doctor --root . no da el aviso nuevo.

FILE:deskops/dispatch.py
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


def _pr_mode(root: Path) -> bool:
    integrate = DeskConfig.load(root / "desk").integrate
    return integrate is not None and integrate.mode == "pr"


def task_branch(task_id: str) -> str:
    return f"task/{task_id}"


def _agent_branch(name: str) -> str:
    return f"deskops/{name}"


def _worktree_path(root: Path, name: str) -> Path:
    return root / WORKTREES_DIR / name


def _check_on_base(root: Path, base: str) -> str | None:
    """Error text when the main checkout is not on ``base``, else None.

    In pr mode a ``task/<id>`` branch (where reap left the executor's commits and the closeout goes) also counts.
    """
    head = _git(root, "rev-parse", "--abbrev-ref", "HEAD")
    if head.returncode != 0:
        return f"{root} no es un repo git: {_git_error(head)}"
    if _pr_mode(root) and head.stdout.strip().startswith("task/"):
        return None
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


def _dirty_worktree_message(root: Path, name: str) -> str | None:
    """Wait message when the worktree of ``name`` holds uncommitted changes, else None."""
    path = _worktree_path(root, name)
    if not path.is_dir():
        return None
    status = _git(path, "status", "--porcelain")
    if status.returncode == 0 and status.stdout.strip():
        return f"en espera: el worktree de {name} tiene cambios sin commitear"
    return None


def _remove_worktree(root: Path, name: str) -> subprocess.CompletedProcess[str] | None:
    """Remove the worktree and branch of an agent; the failing git result, or None."""
    path = _worktree_path(root, name)
    if path.exists():
        removed = _git(root, "worktree", "remove", str(path))
        if removed.returncode != 0:
            return removed
    deleted = _git(root, "branch", "-D", _agent_branch(name))
    return deleted if deleted.returncode != 0 else None


def _prepare_target(root: Path, base: str, task_id: str) -> tuple[str, str]:
    """(branch that receives the commits, error). In pr mode: ``task/<id>`` from the base, checked out."""
    if not _pr_mode(root):
        return base, ""
    target = task_branch(task_id)
    head = _git(root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if head == target:
        return target, ""
    exists = _git(root, "rev-parse", "--verify", "--quiet", f"refs/heads/{target}").returncode == 0
    if not exists:
        made = _git(root, "branch", target, base)
        if made.returncode != 0:
            return target, f"git branch {target} {base}: {_git_error(made)}"
    switched = _git(root, "checkout", "-q", target)
    if switched.returncode != 0:
        return target, f"git checkout {target}: {_dirty_overwrite_hint(root, base, target, _git_error(switched))}"
    return target, ""


def _integrate_branch(root: Path, name: str, task_id: str = "") -> tuple[int, str]:
    """Bring the commits of ``deskops/<name>`` onto the local base branch, then drop worktree and branch.

    In pr mode the target is the local branch ``task/<task id>`` (created from the base and checked out
    in the main checkout, so the closeout commits land on it), never the base itself.

    Returns (0, "") when there was nothing to do or it went through, else (code, message)
    leaving worktree and branch in place.
    """
    branch = _agent_branch(name)
    if _git(root, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}").returncode != 0:
        return 0, ""
    waiting = _dirty_worktree_message(root, name)
    if waiting:
        return EXIT_BUSY, waiting
    base = _base_branch(root)
    problem = _check_on_base(root, base)
    if problem:
        return EXIT_WORKTREE, f"{problem}: no se integra {branch}"
    base, problem = _prepare_target(root, base, task_id)
    if problem:
        return EXIT_WORKTREE, f"no se pudo preparar {base}: {problem}"
    pending = _git(root, "rev-list", "--reverse", "--no-merges", f"{base}..{branch}")
    if pending.returncode != 0:
        return EXIT_WORKTREE, f"git rev-list {base}..{branch}: {_git_error(pending)}"
    commits = pending.stdout.split()
    if not commits:
        # never drop a branch whose tip is not in base, whatever the count said
        tip = _git(root, "rev-parse", branch)
        if tip.returncode != 0:
            return EXIT_WORKTREE, f"git rev-parse {branch}: {_git_error(tip)}"
        if _git(root, "merge-base", "--is-ancestor", branch, base).returncode != 0:
            return EXIT_WORKTREE, f"no se borra {branch}: su punta {tip.stdout.strip()} no esta en {base} y no se conto ningun commit"
    if commits:
        failure = _commit_run_store(root, [name])
        if failure:
            return EXIT_WORKTREE, f"no se pudo commitear el RunDoc de {name}: {failure}"
        if _git(root, "merge-base", "--is-ancestor", base, branch).returncode == 0:
            picked = _git(root, "merge", "--ff-only", "-q", branch)  # keeps the executor's shas
        else:
            picked = _git(root, "cherry-pick", "--keep-redundant-commits", *commits)
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


def _unintegrated_executor_branch(root: Path, task_path: Path) -> str | None:
    """Branch of an executor of the task (attempts 1 and 2) with commits not on the base branch."""
    from deskops.runtime.scion import scion_child_identity

    base = "HEAD" if _pr_mode(root) else _base_branch(root)
    for attempt in (1, 2):
        branch = _agent_branch(scion_child_identity(task_path, "executor", attempt)["name"])
        if _git(root, "rev-parse", "--verify", "-q", f"refs/heads/{branch}").returncode != 0:
            continue
        ahead = _git(root, "rev-list", "--count", f"{base}..{branch}")
        if ahead.returncode == 0 and ahead.stdout.strip() not in ("", "0"):
            return branch
    return None


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

    if role == "tester":
        pending = _unintegrated_executor_branch(root, task_path)
        if pending:
            print(f"en espera: la rama {pending} de la tarea no está integrada")
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
        if _pr_mode(root):
            base = "HEAD"  # the base or the task branch the checkout is on
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
            attempt=int(identity["attempt"]),
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
    else:
        from deskops.runtime.scion import confirm_scion_dispatch

        if any(str(agent.get("name")) == name for agent in _list_agents(cfg)):
            try:
                confirm_scion_dispatch(root, run_dir)
            except Exception as exc:  # noqa: BLE001 - confirmation is best effort
                print(f"aviso: no se pudo confirmar el despacho de {name}: {exc}")
    print(f"agente {name} run_dir {run_dir}")
    return started.returncode


def reap(root: Path, task_id: str) -> int:
    from deskops.runtime.scion import _scion_task_label

    cfg = _dispatch_config(root)
    label = _scion_task_label(task_id)  # no TaskDoc read: the task may be closed already
    alive = 0
    failed = False
    conflict = False
    busy = False
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
        if role == "executor":
            if reason == "result-summary" and phase == "running" and activity not in ("completed", "stopped", "exited"):
                print(f"en espera: {name} sigue vivo")
                busy = True
                continue
            waiting = _dirty_worktree_message(root, name)
            if waiting:
                print(waiting)
                busy = True
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
            code, message = _integrate_branch(root, name, task_id)
            if message:
                print(f"{name} {message}")
            if code == EXIT_BUSY:
                busy = True
            elif code:
                conflict = True
    if alive:
        return EXIT_ALIVE
    if conflict:
        return EXIT_WORKTREE
    if busy:
        return EXIT_BUSY
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

FILE:tests/test_dispatch.py
"""`deskops dispatch {start|reap}` against a fake scion executable and a throwaway desk."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]

FAKE_SCION = """#!{python}
import json, os, sys
with open(os.environ["FAKE_SCION_LOG"], "a") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
if sys.argv[1:2] == ["list"]:
    with open(os.environ["FAKE_SCION_LIST"]) as handle:
        sys.stdout.write(handle.read())
if sys.argv[1:2] == ["stop"] and sys.argv[2:3] == [os.environ.get("FAKE_SCION_FAIL_STOP")]:
    sys.exit(9)
sys.exit(int(os.environ.get("FAKE_SCION_START_CODE", "0")) if sys.argv[1:2] == ["start"] else 0)
"""


class Env:
    def __init__(self, tmp_path: Path, root: Path) -> None:
        self.root = root
        self.log = tmp_path / "scion.log"
        self.listing = tmp_path / "list.json"
        self.listing.write_text("[]")
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir()
        scion = bin_dir / "scion"
        scion.write_text(FAKE_SCION.format(python=sys.executable))
        scion.chmod(0o755)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("DESKOPS_")}
        self.env["PATH"] = f"{bin_dir}{os.pathsep}{self.env['PATH']}"
        self.env["PYTHONPATH"] = str(ROOT) + os.pathsep + self.env.get("PYTHONPATH", "")
        self.env["FAKE_SCION_LOG"] = str(self.log)
        self.env["FAKE_SCION_LIST"] = str(self.listing)

    def cli(self, *argv: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "deskops", *argv, "--root", "."],
            cwd=self.root, capture_output=True, text=True, env=self.env,
        )

    def calls(self) -> list[list[str]]:
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def agents(self, *items: dict) -> None:
        self.listing.write_text(json.dumps(list(items)))


def _role_config(role: str, **extra) -> dict:
    return {"role": role, "harness": "claude", "model_alias": "medium", "harness_auth": "oauth-token", **extra}


@pytest.fixture
def env(lifecycle_desk: Path, tmp_path: Path) -> Env:
    root = lifecycle_desk
    e = Env(tmp_path, root)
    for sub in ("src/deskops", "sldbsrc/sldb"):
        (tmp_path / sub).mkdir(parents=True)
    context = tmp_path / "context.json"
    context.write_text(json.dumps({
        "project": "proj", "workspace_root": str(tmp_path), "desk_root": str(root),
        "source_root": str(tmp_path / "src"), "sldb_root": str(tmp_path / "sldbsrc"),
    }))
    for name in ("disp-executor", "disp-tester"):
        added = e.cli("add", "role", "--name", name, "--kind", "claude", "--description", f"{name}.", "--body", f"# {name}\n")
        assert added.returncode == 0, added.stdout + added.stderr
    added = e.cli("add", "runtime-profile", "--title", "Claude on Scion", "--kind", "claude",
                  "--binary", "claude", "--status", "active", "--tools-flag=--allowedTools")
    assert added.returncode == 0, added.stdout + added.stderr
    added = e.cli("add", "task", "--title", "Dispatch me", "--goal", "g", "--scope", "s",
                  "--validation", "pytest", "--task-type", "task.code")
    assert added.returncode == 0, added.stdout + added.stderr
    config = {
        "project_identity": "dispatch-test",
        "queue_min_available_gb": 0,
        "queue_max_psi_avg60": 1000,
        "dispatch": {
            "project": "proj", "workspace": str(tmp_path), "templates_dir": str(tmp_path / "templates"),
            "context_file": str(context),
            "roles": {
                "executor": _role_config("role-disp-executor", env_config=str(tmp_path / "env.yaml")),
                "tester": _role_config("disp-tester"),
            },
        },
    }
    (root / "desk" / "config.json").write_text(json.dumps(config))
    subprocess.run(["git", "checkout", "-q", "-B", "main"], cwd=root, check=True)
    return e


TASK = "task-dispatch-me"


def _start_call(env: Env) -> list[str]:
    return next(c for c in env.calls() if c[0] == "start")


def test_start_executor(env: Env, tmp_path: Path) -> None:
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    start = _start_call(env)
    name = start[1]
    assert name.startswith("deskops-e-")
    run_dir = f"runs/subagents/exec-{name}"
    assert result.stdout.strip() == f"agente {name} run_dir {run_dir}"
    assert env.calls()[0] == ["list", "--project", "proj", "--format", "json"]
    assert ["templates", "sync", str((tmp_path / "templates" / "disp-executor").resolve()), "--project", "proj"] in env.calls()
    prompt_file = (env.root / run_dir / "prompt.md").resolve()
    assert start[2] == (
        f"Tu encargo esta en el archivo {prompt_file}. "
        "Lee el archivo completo antes de empezar y luego cumple el encargo que describe."
    )
    assert start[3:9] == ["--type", "disp-executor", "--project", "proj", "--workspace", str(tmp_path)]
    assert "--harness-auth" in start and "oauth-token" in start
    assert start[start.index("--config") + 1] == str(tmp_path / "env.yaml")
    assert "deskops.role=executor" in start and f"deskops.task_id={TASK}" in start
    assert (tmp_path / "templates" / "disp-executor" / "scion-agent.yaml").is_file()
    assert (env.root / run_dir / "run.md").is_file()
    text = prompt_file.read_text()
    assert TASK in text and "# Dispatch me" in text


def test_start_syncs_the_template_by_path_in_a_desk_with_its_own_scion(env: Env, tmp_path: Path) -> None:
    (env.root / ".scion").mkdir()
    (env.root / ".scion" / "settings.yaml").write_text("hub:\n  enabled: true\n")
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    target = (tmp_path / "templates" / "disp-executor").resolve()
    assert ["templates", "sync", str(target), "--project", "proj"] in env.calls()
    assert _start_call(env)[3:5] == ["--type", "disp-executor"]


def test_start_tester_run_dir_has_testing_suffix(env: Env, tmp_path: Path) -> None:
    result = env.cli("dispatch", "start", "tester", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    start = _start_call(env)
    name = start[1]
    assert name.startswith("deskops-t-") and not name.endswith("-testing")
    run_dir = f"runs/subagents/exec-{name}-testing"
    assert result.stdout.strip() == f"agente {name} run_dir {run_dir}"
    assert "--config" not in start
    assert (env.root / run_dir / "prompt.md").is_file() and (env.root / run_dir / "run.md").is_file()
    assert ["templates", "sync", str((tmp_path / "templates" / "disp-tester").resolve()), "--project", "proj"] in env.calls()
    assert (tmp_path / "templates" / "disp-tester").is_dir()


def _set_config(env: Env, **fields) -> None:
    path = env.root / "desk" / "config.json"
    data = json.loads(path.read_text())
    data.update(fields)
    path.write_text(json.dumps(data))


def test_start_launches_while_another_task_agent_is_running(env: Env) -> None:
    env.agents({"name": "other-agent", "phase": "running"}, {"name": "old", "phase": "stopped"})
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert any(call[0] == "start" for call in env.calls())


def test_start_refuses_when_the_task_already_has_a_running_agent(env: Env) -> None:
    first = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert first.returncode == 0, first.stdout + first.stderr
    name = _start_call(env)[1]
    env.log.unlink()
    env.agents({"name": name, "phase": "running"})
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 3
    assert f"ocupado: la tarea ya tiene agente {name}" in result.stdout
    assert all(call[0] == "list" for call in env.calls())


def test_start_refuses_when_memory_is_under_the_gate(env: Env) -> None:
    _set_config(env, queue_min_available_gb=100000)
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 3
    assert "ocupado: memoria disponible" in result.stdout
    assert not any(call[0] == "start" for call in env.calls())


def test_attempts_then_no_more(env: Env) -> None:
    first = env.cli("dispatch", "start", "executor", "--task", TASK)
    second = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert first.returncode == 0 and second.returncode == 0
    names = [c[1] for c in env.calls() if c[0] == "start"]
    assert len(names) == 2 and names[1] == names[0] + "-a2"
    third = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert third.returncode == 5
    assert third.stdout.strip() == f"sin intentos: {TASK} executor"
    assert len([c for c in env.calls() if c[0] == "start"]) == 2


def test_start_returns_scion_start_exit_code(env: Env) -> None:
    env.env["FAKE_SCION_START_CODE"] = "7"
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 7 and "agente deskops-e-" in result.stdout


def test_reap(env: Env) -> None:
    labels = lambda role: {"deskops.task_id": TASK, "deskops.role": role}  # noqa: E731
    summary_dir = env.root / "runs" / "subagents" / "exec-deskops-t-aaa-testing"
    summary_dir.mkdir(parents=True)
    (summary_dir / "result-summary.md").write_text("done")
    env.agents(
        {"name": "deskops-e-phase", "phase": "stopped", "activity": "idle", "labels": labels("executor")},
        {"name": "deskops-e-act", "phase": "running", "activity": "blocked", "labels": labels("executor")},
        {"name": "deskops-t-aaa", "phase": "running", "activity": "working", "labels": labels("tester")},
        {"name": "deskops-e-live", "phase": "running", "activity": "working", "labels": labels("executor")},
        {"name": "unrelated", "phase": "stopped", "labels": {"deskops.task_id": "task-other", "deskops.role": "executor"}},
    )
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 4, result.stdout + result.stderr
    assert result.stdout.splitlines() == [
        "deskops-e-phase executor phase:stopped",
        "deskops-e-act executor activity:blocked",
        "deskops-t-aaa tester result-summary",
        "deskops-e-live executor vivo",
    ]
    calls = env.calls()
    for name in ("deskops-e-phase", "deskops-e-act", "deskops-t-aaa"):
        assert ["stop", name, "--project", "proj"] in calls
        assert ["delete", name, "--project", "proj", "--yes"] in calls
    assert not any(len(c) > 1 and c[1] in ("deskops-e-live", "unrelated") for c in calls)


def test_reap_all_finished_exits_zero(env: Env) -> None:
    env.agents({"name": "deskops-e-x", "phase": "stopped", "labels": {"deskops.task_id": TASK, "deskops.role": "executor"}})
    assert env.cli("dispatch", "reap", "--task", TASK).returncode == 0


def test_reap_after_the_task_was_deleted(env: Env) -> None:
    (env.root / "desk" / "tasks" / f"{TASK}.md").unlink()
    env.agents({"name": "deskops-e-x", "phase": "stopped", "labels": {"deskops.task_id": TASK, "deskops.role": "executor"}})
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert ["delete", "deskops-e-x", "--project", "proj", "--yes"] in env.calls()


def test_reap_scion_error_continues_and_fails(env: Env) -> None:
    labels = {"deskops.task_id": TASK, "deskops.role": "executor"}
    env.env["FAKE_SCION_FAIL_STOP"] = "deskops-e-bad"
    env.agents(
        {"name": "deskops-e-bad", "phase": "stopped", "labels": labels},
        {"name": "deskops-e-ok", "phase": "stopped", "labels": labels},
    )
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode != 0
    assert result.stdout.splitlines() == ["deskops-e-bad executor error:9", "deskops-e-ok executor phase:stopped"]
    assert ["delete", "deskops-e-ok", "--project", "proj", "--yes"] in env.calls()


def test_executor_prompt_asks_for_named_commit_with_task_id(env: Env) -> None:
    assert env.cli("dispatch", "start", "executor", "--task", TASK).returncode == 0
    name = _start_call(env)[1]
    text = (env.root / f"runs/subagents/exec-{name}/prompt.md").read_text()
    assert f"Task-Id: {TASK}" in text and "uno por uno" in text
    assert "git add -A" in text and "git stash" in text and "deskops advance task" in text
    assert "--grep" not in text


def test_tester_prompt_runs_only_touched_tests(env: Env) -> None:
    assert env.cli("dispatch", "start", "tester", "--task", TASK).returncode == 0
    name = _start_call(env)[1]
    text = (env.root / f"runs/subagents/exec-{name}-testing/prompt.md").read_text()
    assert f'git log -1 --format=%H --grep "Task-Id: {TASK}"' in text
    assert "git show --name-only" in text and "TMPDIR=/tmp" in text
    assert "PASA o FALLA" in text and "integrate en el host" in text


@pytest.mark.parametrize("argv", [("start", "executor"), ("start", "tester"), ("reap",)])
def test_without_dispatch_config_exits_2(env: Env, argv: tuple[str, ...]) -> None:
    (env.root / "desk" / "config.json").write_text(json.dumps({"project_identity": "x"}))
    result = env.cli("dispatch", *argv, "--task", TASK)
    assert result.returncode == 2
    assert "falta el campo dispatch en desk/config.json" in result.stdout + result.stderr
    assert env.calls() == []


@pytest.fixture
def roleless(env: Env, tmp_path: Path) -> Env:
    """A task desk without roles; its dispatch config takes them from the `env` desk."""
    import shutil

    taskdesk = tmp_path / "taskdesk"
    shutil.copytree(env.root, taskdesk, ignore=shutil.ignore_patterns("roles"))
    assert not (taskdesk / "desk" / "roles").exists()
    config = json.loads((env.root / "desk" / "config.json").read_text())
    config["project_identity"] = "taskdesk-identity"
    config["dispatch"]["roles_root"] = str(env.root)
    (taskdesk / "desk" / "config.json").write_text(json.dumps(config))
    env.root = taskdesk
    return env


def test_start_takes_roles_from_roles_root(roleless: Env, tmp_path: Path) -> None:
    result = roleless.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    start = _start_call(roleless)
    name = start[1]
    run_dir = f"runs/subagents/exec-{name}"
    assert start[3:5] == ["--type", "disp-executor"]
    assert (tmp_path / "templates" / "disp-executor" / "scion-agent.yaml").is_file()
    assert "taskdesk-identity" in (tmp_path / "templates" / "disp-executor" / "agents.md").read_text()
    assert (roleless.root / run_dir / "run.md").is_file()
    assert (roleless.root / run_dir / "prompt.md").is_file()


def test_roles_root_relative_resolves_against_task_root(roleless: Env, tmp_path: Path) -> None:
    path = roleless.root / "desk" / "config.json"
    config = json.loads(path.read_text())
    config["dispatch"]["roles_root"] = "../repo"
    path.write_text(json.dumps(config))
    result = roleless.cli("dispatch", "start", "tester", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _start_call(roleless)[3:5] == ["--type", "disp-tester"]


def test_start_without_roles_root_and_without_roles_fails(roleless: Env) -> None:
    path = roleless.root / "desk" / "config.json"
    config = json.loads(path.read_text())
    del config["dispatch"]["roles_root"]
    path.write_text(json.dumps(config))
    result = roleless.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode != 0
    assert not any(c[0] == "start" for c in roleless.calls())


def test_reap_works_on_a_desk_without_roles(roleless: Env) -> None:
    roleless.agents({"name": "deskops-e-x", "phase": "stopped", "labels": {"deskops.task_id": TASK, "deskops.role": "executor"}})
    result = roleless.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert ["stop", "deskops-e-x", "--project", "proj"] in roleless.calls()


def _set_quick_gates(env: Env, gates: list[str] | None) -> None:
    path = env.root / "desk" / "config.json"
    config = json.loads(path.read_text())
    if gates is not None:
        config["dispatch"]["quick_gates"] = gates
    path.write_text(json.dumps(config))


@pytest.mark.parametrize("role", ["executor", "tester"])
def test_prompts_require_quick_gates_when_declared(env: Env, role: str) -> None:
    _set_quick_gates(env, ["bash", "tools/check.sh", "--fast"])
    assert env.cli("dispatch", "start", role, "--task", TASK).returncode == 0
    name = _start_call(env)[1]
    suffix = "-testing" if role == "tester" else ""
    text = (env.root / f"runs/subagents/exec-{name}{suffix}/prompt.md").read_text()
    assert "bash tools/check.sh --fast" in text
    assert ("rc 0 antes de commitear" if role == "executor" else "veredicto es FALLA") in text


@pytest.mark.parametrize("role", ["executor", "tester"])
def test_prompts_without_quick_gates_do_not_mention_them(env: Env, role: str) -> None:
    _set_quick_gates(env, None)
    assert env.cli("dispatch", "start", role, "--task", TASK).returncode == 0
    name = _start_call(env)[1]
    suffix = "-testing" if role == "tester" else ""
    text = (env.root / f"runs/subagents/exec-{name}{suffix}/prompt.md").read_text()
    assert "Gates rapidos" not in text


# --- worktree por ejecutor ---------------------------------------------------


def _git(cwd: Path, *argv: str) -> str:
    done = subprocess.run(["git", *argv], cwd=cwd, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    return done.stdout.strip()


def _start_executor(env: Env, task: str = TASK) -> str:
    result = env.cli("dispatch", "start", "executor", "--task", task)
    assert result.returncode == 0, result.stdout + result.stderr
    return next(c for c in reversed(env.calls()) if c[0] == "start")[1]


def _commit_in(worktree: Path, filename: str, text: str) -> str:
    (worktree / filename).write_text(text)
    _git(worktree, "add", filename)
    _git(worktree, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", f"add {filename}")
    return _git(worktree, "rev-parse", "HEAD")


def _finished(env: Env, *names: str) -> None:
    env.agents(*({"name": n, "phase": "stopped", "labels": {"deskops.task_id": TASK, "deskops.role": "executor"}} for n in names))


def test_start_executor_creates_own_worktree_and_branch(env: Env) -> None:
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    assert worktree.is_dir()
    assert _git(worktree, "rev-parse", "--abbrev-ref", "HEAD") == f"deskops/{name}"
    assert _git(worktree, "rev-parse", "HEAD") == _git(env.root, "rev-parse", "main")
    assert ".worktrees/" in (env.root / ".git" / "info" / "exclude").read_text().splitlines()
    assert ".worktrees" not in _git(env.root, "status", "--short")
    prompt = (env.root / f"runs/subagents/exec-{name}" / "prompt.md").read_text()
    assert f"{worktree}" in prompt and f"deskops/{name}" in prompt


def test_start_tester_has_no_worktree(env: Env) -> None:
    assert env.cli("dispatch", "start", "tester", "--task", TASK).returncode == 0
    assert not (env.root / ".worktrees").exists()


def test_start_tester_waits_while_the_executor_branch_is_not_integrated(env: Env) -> None:
    name = _start_executor(env)
    _commit_in(env.root / ".worktrees" / name, "one.txt", "1")
    _finished(env, name)
    result = env.cli("dispatch", "start", "tester", "--task", TASK)
    assert result.returncode == 3, result.stdout + result.stderr
    assert f"en espera: la rama deskops/{name} de la tarea no está integrada" in result.stdout
    assert not any(c[0] == "start" and c[1].startswith("deskops-t-") for c in env.calls())
    assert env.cli("dispatch", "reap", "--task", TASK).returncode == 0
    assert env.cli("dispatch", "start", "tester", "--task", TASK).returncode == 0


def test_start_tester_launches_when_the_executor_branch_has_no_new_commits(env: Env) -> None:
    name = _start_executor(env)
    _finished(env, name)
    assert env.cli("dispatch", "start", "tester", "--task", TASK).returncode == 0


def test_start_refuses_when_checkout_is_not_on_base_branch(env: Env) -> None:
    _git(env.root, "checkout", "-q", "-b", "other")
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 8 and "no en 'main'" in result.stdout
    assert not any(c[0] == "start" for c in env.calls())


def test_start_scion_failure_removes_the_worktree(env: Env) -> None:
    env.env["FAKE_SCION_START_CODE"] = "7"
    assert env.cli("dispatch", "start", "executor", "--task", TASK).returncode == 7
    assert not list((env.root / ".worktrees").glob("*"))
    assert "deskops/" not in _git(env.root, "branch", "--list")


def test_two_executors_do_not_share_tree_or_index(env: Env) -> None:
    add = env.cli("add", "task", "--title", "Second", "--goal", "g", "--scope", "s",
                  "--validation", "pytest", "--task-type", "task.code")
    assert add.returncode == 0, add.stdout + add.stderr
    first = _start_executor(env)
    second = _start_executor(env, "task-second")
    assert first != second
    one, two = env.root / ".worktrees" / first, env.root / ".worktrees" / second
    _commit_in(one, "one.txt", "1")
    (two / "dirty.txt").write_text("x")
    assert not (two / "one.txt").exists() and not (one / "dirty.txt").exists()
    assert _git(two, "status", "--short") == "?? dirty.txt"
    assert _git(env.root, "branch", "--list", "deskops/*").count("deskops/") == 2


def test_reap_fast_forwards_commit_and_removes_worktree(env: Env) -> None:
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    sha = _commit_in(worktree, "one.txt", "1")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(env.root, "rev-parse", "main") == sha
    assert not worktree.exists()
    assert _git(env.root, "branch", "--list", "deskops/*") == ""


def test_reap_cherry_picks_only_the_task_commit(env: Env) -> None:
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    _commit_in(worktree, "mine.txt", "m")
    (env.root / "other.txt").write_text("o")
    _git(env.root, "add", "other.txt")
    _git(env.root, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "main moved")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(env.root, "show", "--name-only", "--format=", "main") == "mine.txt"
    assert (env.root / "other.txt").is_file()
    assert not worktree.exists()


def test_reap_conflict_aborts_and_keeps_worktree(env: Env) -> None:
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    _commit_in(worktree, "same.txt", "mine")
    (env.root / "same.txt").write_text("theirs")
    _git(env.root, "add", "same.txt")
    _git(env.root, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "main same")
    before = _git(env.root, "rev-parse", "main")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 8 and "conflicto" in result.stdout
    assert _git(env.root, "rev-parse", "main") == before
    assert worktree.is_dir() and f"deskops/{name}" in _git(env.root, "branch", "--list", "deskops/*")
    assert not (env.root / ".git" / "CHERRY_PICK_HEAD").exists()


def test_start_commits_the_rundoc_so_reap_brings_an_executor_commit_touching_the_store(env: Env) -> None:
    _git(env.root, "add", ".sldb", "desk")
    _git(env.root, "commit", "-q", "-m", "desk")
    (env.root / "unrelated.txt").write_text("dirty")  # foreign dirty work must stay uncommitted
    name = _start_executor(env)
    assert _git(env.root, "status", "--short", "--", ".sldb") == ""
    assert _git(env.root, "log", "-1", "--format=%s%n%b", "--", ".sldb").splitlines()[0] == f"run: {name}"
    assert "[skip ci]" in _git(env.root, "log", "-1", "--format=%B")
    assert _git(env.root, "status", "--short", "unrelated.txt") == "?? unrelated.txt"
    worktree = env.root / ".worktrees" / name
    index = worktree / ".sldb/core/store_index.yaml"
    index.write_text(index.read_text() + "\n# executor sync\n")
    _git(worktree, "add", ".sldb/core/store_index.yaml")
    _git(worktree, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "sync store")
    (env.root / "main.txt").write_text("m")
    _git(env.root, "add", "main.txt")
    _git(env.root, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "main moved")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "executor sync" in (env.root / ".sldb/core/store_index.yaml").read_text()
    assert not worktree.exists()


def test_start_commits_the_run_md_with_the_rundoc_and_the_store_gate_passes(env: Env) -> None:
    from deskops.integrate import _collect_paths

    _git(env.root, "add", ".sldb", "desk", "sldb")
    _git(env.root, "commit", "-q", "-m", "desk")
    name = _start_executor(env)
    run_md = f"runs/subagents/exec-{name}/run.md"
    files = _git(env.root, "show", "--name-only", "--format=%s", "HEAD").splitlines()
    assert files[0] == f"run: {name}"
    assert run_md in files and any("RunDoc/run-" in f for f in files)
    store = yaml.safe_load(_git(env.root, "show", "HEAD:.sldb/store.yaml"))
    for path in _collect_paths(store):
        if not path.startswith("../"):
            _git(env.root, "cat-file", "-e", f"HEAD:{path.rstrip('/') or '.'}")


def test_reap_names_the_files_when_local_changes_block_the_pick(env: Env) -> None:
    _git(env.root, "add", ".sldb", "desk")
    _git(env.root, "commit", "-q", "-m", "desk")
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    _commit_in(worktree, "shared.txt", "mine")
    (env.root / "main.txt").write_text("m")
    _git(env.root, "add", "main.txt")
    _git(env.root, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "main moved")
    (env.root / "shared.txt").write_text("local")
    _git(env.root, "add", "shared.txt")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 8 and "shared.txt" in result.stdout and "commitea" in result.stdout


def test_reap_names_the_files_under_a_spanish_locale(env: Env) -> None:
    env.env.update({"LANG": "es_ES.UTF-8", "LC_ALL": "es_ES.UTF-8", "LANGUAGE": "es"})
    test_reap_names_the_files_when_local_changes_block_the_pick(env)


def test_start_untracks_a_stale_rundoc_whose_run_dir_is_missing(env: Env) -> None:
    import shutil

    name = _start_executor(env)
    _git(env.root, "worktree", "remove", "--force", str(env.root / ".worktrees" / name))
    _git(env.root, "branch", "-D", f"deskops/{name}")
    shutil.rmtree(env.root / f"runs/subagents/exec-{name}")  # RunDoc stays tracked in the store
    result = env.cli("dispatch", "start", "executor", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert (env.root / f"runs/subagents/exec-{name}/run.md").is_file()
    assert [c[1] for c in env.calls() if c[0] == "start"] == [name, name]


def test_reap_brings_the_commit_made_on_top_of_a_run_commit_made_in_main(env: Env) -> None:
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    (env.root / "marker.txt").write_text("r")  # the 'run:' commit made in main after the branch was created
    _git(env.root, "add", "marker.txt")
    _git(env.root, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", f"run: {name}")
    _git(worktree, "merge", "--ff-only", "-q", "main")  # the executor's commit sits on top of it ...
    (worktree / "marker.txt").write_text("r2")
    _git(worktree, "add", "marker.txt")
    _git(worktree, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "mine", "-m", "Task-Id: t")
    # ... and another main commit repeats its patch, so `--cherry-pick` would count it as already in main
    (env.root / "marker.txt").write_text("r2")
    _git(env.root, "add", "marker.txt")
    _git(env.root, "-c", "user.email=a@b", "-c", "user.name=A", "commit", "-q", "-m", "same patch")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "integrado 1 commit(s)" in result.stdout
    assert "Task-Id: t" in _git(env.root, "log", "--format=%B", "main")
    assert not worktree.exists()


def test_reap_keeps_the_branch_when_no_commit_is_counted_but_the_tip_is_not_in_main(env: Env, monkeypatch) -> None:
    from deskops import dispatch

    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    sha = _commit_in(worktree, "mine.txt", "m")
    real = dispatch._git

    def blind(root, *args):  # a miscount: rev-list reports nothing pending
        if args[:1] == ("rev-list",) and "--count" not in args:
            return subprocess.CompletedProcess(args, 0, "", "")
        return real(root, *args)

    monkeypatch.setattr(dispatch, "_git", blind)
    code, message = dispatch._integrate_branch(env.root, name)
    assert code == 8 and f"deskops/{name}" in message and sha in message
    assert worktree.is_dir() and f"deskops/{name}" in _git(env.root, "branch", "--list", "deskops/*")


def test_reap_waits_while_the_worktree_has_uncommitted_changes(env: Env) -> None:
    name = _start_executor(env)
    worktree = env.root / ".worktrees" / name
    (worktree / "late.txt").write_text("not committed yet")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 3, result.stdout + result.stderr
    assert f"en espera: el worktree de {name} tiene cambios sin commitear" in result.stdout
    assert (worktree / "late.txt").read_text() == "not committed yet"
    assert f"deskops/{name}" in _git(env.root, "branch", "--list", "deskops/*")
    assert not any(c[0] == "delete" for c in env.calls())
    _git(worktree, "add", "late.txt")
    sha = _commit_in(worktree, "other.txt", "o")
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(env.root, "rev-parse", "main") == sha and (env.root / "late.txt").is_file()
    assert not worktree.exists()


def test_reap_waits_while_the_executor_is_alive(env: Env) -> None:
    name = _start_executor(env)
    (env.root / "runs" / "subagents" / f"exec-{name}" / "result-summary.md").write_text("done")
    env.agents({"name": name, "phase": "running", "activity": "working", "labels": {"deskops.task_id": TASK, "deskops.role": "executor"}})
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 3, result.stdout + result.stderr
    assert f"en espera: {name} sigue vivo" in result.stdout
    assert (env.root / ".worktrees" / name).is_dir()
    assert not any(c[0] in ("stop", "delete") for c in env.calls())


def test_reap_in_pr_mode_brings_commits_to_the_task_branch_not_the_base(env: Env) -> None:
    _set_config(env, integrate={"remote_url": "unused", "branch": "main", "suite": ["true"], "mode": "pr"})
    name = _start_executor(env)
    base_sha = _git(env.root, "rev-parse", "main")  # start commits the RunDoc on the base
    worktree = env.root / ".worktrees" / name
    sha = _commit_in(worktree, "one.txt", "1")
    _finished(env, name)
    result = env.cli("dispatch", "reap", "--task", TASK)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(env.root, "rev-parse", "main") == base_sha
    assert _git(env.root, "rev-parse", f"task/{TASK}") == sha
    assert _git(env.root, "rev-parse", "--abbrev-ref", "HEAD") == f"task/{TASK}"
    assert not worktree.exists()

FILE:instruccion
Cold-bundle de la tarea task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_dispatch.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_doctor_alerts.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

