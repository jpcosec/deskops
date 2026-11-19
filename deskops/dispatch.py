"""Scion dispatch: `deskops dispatch {start|reap}`.

Chains the deterministic steps of launching the executor or tester of one task
(identity, template, prompt, `scion start`) and of collecting the finished ones
(`scion stop` + `scion delete`). Every call to scion goes through `_scion`.
"""

from __future__ import annotations

import contextlib
import io
import json
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


def _role_instructions(role: str, task_id: str, quick_gates: list[str] | None = None) -> str:
    return _base_instructions(role, task_id) + _quick_gates_text(role, quick_gates)


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

    for agent in _list_agents(cfg):
        if agent.get("phase") == "running":
            print(f"ocupado: {agent.get('name')}")
            return EXIT_BUSY

    identity = scion_child_identity(task_path, role, 1)
    run_dir = _run_dir_for(identity["name"], role)
    if (root / run_dir).exists():
        identity = scion_child_identity(task_path, role, 2)
        run_dir = _run_dir_for(identity["name"], role)
        if (root / run_dir).exists():
            print(f"sin intentos: {task_id} {role}")
            return EXIT_NO_ATTEMPTS
    name = identity["name"]

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
    record_scion_run(
        root,
        task_id=task_id,
        role_id=str(role_doc["id"]),
        kind=role_cfg.harness,
        agent_slug=name,
        run_dir=run_dir,
    )

    sync = _scion(["scion", "templates", "sync", role_name, "--project", cfg.project])
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
        + _role_instructions(role, task_id, cfg.quick_gates),
        encoding="utf-8",
    )

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
    print(f"agente {name} run_dir {run_dir}")
    return started.returncode


def reap(root: Path, task_id: str) -> int:
    from deskops.runtime.scion import _scion_task_label

    cfg = _dispatch_config(root)
    label = _scion_task_label(task_id)  # no TaskDoc read: the task may be closed already
    alive = 0
    failed = False
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
    if alive:
        return EXIT_ALIVE
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
