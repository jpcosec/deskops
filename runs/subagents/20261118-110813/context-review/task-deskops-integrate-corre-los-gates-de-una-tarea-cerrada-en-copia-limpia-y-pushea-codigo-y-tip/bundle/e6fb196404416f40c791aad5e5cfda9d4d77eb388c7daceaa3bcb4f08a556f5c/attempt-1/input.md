FILE:desk/tasks/task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip.md
---
sldb:
  by: agent
  at: '2026-11-18T11:07:01Z'
  authority: generated
  via: save_document_payload
id: task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-un-runner-del-host-toma-de-una-cola-los-trabajos-pesados-que-encolan-los-post-hooks
pills: []
files:
- deskops/config.py
- deskops/cli/registry.py
- deskops/queue.py
- docs/operator-manual.md
- tests/test_cli.py
- tests/test_cli_grammar.py
- tests/test_command_registry.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops integrate corre los gates de una tarea cerrada en copia limpia y pushea codigo y tip

## Rationale

_Explain why this task exists or the business driver behind it._

La integracion (copia limpia, suite completa, checks del desk, push del commit de codigo y luego del tip, actualizar la instalacion de herramientas) la hace hoy a mano el integrador siguiendo la receta escrita en el archivo integrate-recipe.md de la carpeta .bootstrap del workspace. JP quiere que corra sola como trabajo de la cola del host.

## Goal

_Describe the concrete result this task must produce._

Un comando nuevo, `deskops integrate --task <id> --root .` (con `--dry-run` opcional), y su configuracion en el desk.

Configuracion. `DeskConfig` (`deskops/config.py`) gana un campo `integrate` con: `remote_url` (URL o ruta del remoto), `branch` (rama remota), `suite` (lista argv de la suite completa), `suite_timeout` (segundos, por defecto 5400), `tests_lock` (ruta de un archivo de cerrojo; opcional), `tools_checkout` (ruta de un checkout de herramientas; opcional) y `push_env` (mapa de variables de entorno para los comandos git de push; opcional). Sin campo `integrate` el comando sale con codigo 2 y el mensaje `falta el campo integrate en desk/config.json`.

Entrada. La tarea debe estar cerrada: su ultima entrada de history es el registro de cierre. El tip es el commit de cierre de la tarea, que se busca con `git log` por el asunto exacto `closeout: <id de la tarea>`; el commit de codigo es el sha de 40 caracteres que aparece en `references` de la tarea. Si la tarea no esta cerrada o falta alguno de los dos commits, sale con codigo 2 y dice cual falta.

Pasos, en orden; el primero que falla detiene todo, no se pushea nada, se borra la copia y el comando sale con codigo 1 imprimiendo `fallo: <paso>: <detalle>`:
1. `memoria`: los mismos dos gates de `deskops queue run` (campos `queue_min_available_gb` y `queue_max_psi_avg60`), reutilizando la funcion que ya los calcula en el modulo de la cola.
2. `copia`: `git clone --no-hardlinks <root> <dir temporal bajo TMPDIR>`, `git checkout --detach <tip>`, `git remote set-url origin <remote_url>`, `git fetch origin <branch>`.
3. `fast-forward`: `git merge-base --is-ancestor origin/<branch> HEAD` debe salir con 0.
4. `suite`: solo si `git diff --name-only origin/<branch> HEAD` trae alguna ruta que no empieza con `desk/`, `.sldb/` ni `runs/`. Corre el argv `suite` en la copia, con `PYTHONPATH` igual a la copia, tomando antes el cerrojo exclusivo de `tests_lock` (bloqueante, `fcntl.flock`) si esta declarado, con tope `suite_timeout`; la salida va a un log. Falla si el codigo no es 0.
5. `store`: cada ruta `path:` de `.sldb/store.yaml` del tip que no empieza con `../` debe existir en el commit (`git cat-file -e HEAD:<ruta>`).
6. `graph`: la cuenta de faltantes de `deskops graph missing --root <copia>` en el tip no puede ser mayor que la misma cuenta en `origin/<branch>` (se mide en un segundo checkout temporal de esa rama).
7. `push`: `git push origin <sha de codigo>:<branch>` y despues `git push origin <tip>:<branch>`, nunca con force, con las variables de `push_env` agregadas al entorno. Con `--dry-run` no se ejecuta e imprime los dos comandos.
8. `herramientas`: si `tools_checkout` esta declarado, `git -C <tools_checkout> fetch origin` y `git -C <tools_checkout> checkout --detach origin/<branch>`. Con `--dry-run` no se ejecuta.
9. Siempre, al final: borra las copias temporales y agrega a `runs/hooks/events.log` del root la linea `<fecha UTC ISO> <id de tarea> integrate <ok|fallo:<paso>> <tip corto>`. El log de la suite queda en `runs/queue/logs/integrate-<id de tarea>.log` del root.
En exito imprime `integrado <sha de codigo corto> <tip corto> en <branch>` y sale con 0.

El manual del operador gana una seccion `Integrate` con la configuracion, los pasos y el ejemplo de `queue_jobs` `integrate: {run: [deskops, integrate, --task-from-env, --root, .]}`; para eso el comando acepta `--task-from-env`, que toma el id de `DESKOPS_TASK_ID`.

## Scope

_State what is in scope and what is out of scope._

Dentro: un modulo nuevo llamado integrate.py en el paquete deskops, el campo en `deskops/config.py`, el registro del comando en `deskops/cli/registry.py`, un archivo de tests nuevo, las declaraciones del comando en `tests/test_cli.py`, `tests/test_cli_grammar.py` y `tests/test_command_registry.py`, los goldens de ayuda, y `docs/operator-manual.md`. Fuera: declarar la configuracion en desks reales; el timer del host; reintentos o rebase automatico cuando no es fast-forward; cambios en sldb. Checkout principal, sin worktree ni rama, sin git add ni git commit. Los tests jamas tocan un remoto real: el remoto es un repositorio bare creado en `tmp_path`.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- Un archivo de tests nuevo, test_integrate.py en la carpeta tests, pasa con `TMPDIR=/dev/shm pytest -q` sobre ese archivo. Cada test arma en `tmp_path` un repo git real con un desk creado por el CLI, una tarea llevada hasta su cierre con los comandos reales (como lo hacen los tests de closeout vecinos) y un remoto bare local, y comprueba: (a) con gates en verde, el remoto queda con el commit de codigo y el tip en la rama, events.log gana la linea `ok` y el comando imprime `integrado`; (b) `--dry-run` no cambia el remoto e imprime los dos comandos de push; (c) una `suite` que sale con 1 produce `fallo: suite`, codigo 1 y remoto intacto; (d) un rango que solo toca `desk/` no corre la suite (la suite configurada es un comando que fallaria); (e) un tip que no es fast-forward de la rama remota produce `fallo: fast-forward`; (f) una ruta de `.sldb/store.yaml` ausente en el commit produce `fallo: store`; (g) tarea sin cerrar y falta del campo `integrate` salen con codigo 2; (h) tras cualquier corrida no queda ninguna copia temporal bajo TMPDIR.
- Los tests guardianes del CLI pasan con el comando nuevo declarado (`pytest -q tests/test_cli_grammar.py tests/test_command_registry.py` y `pytest -q tests/test_cli.py -k help_uses_deskops_name`) y los goldens de ayuda se regeneran conservando solo los que cambian por el comando nuevo.
- `TMPDIR=/dev/shm pytest -q tests/test_queue.py` sigue pasando.

## Done When

_Name the observable condition that makes the task complete._

Las tres validaciones pasan y el manual tiene la seccion `Integrate`.

FILE:desk/atoms/workflow-model/atom-code-changes-close-with-tests-and-commit.md
---
id: atom-code-changes-close-with-tests-and-commit
title: Code changes close with tests and commit
five_wh_one_plus: when
tags:
- system:deskops
- topic:testing
- topic:git
- topic:closeout
---

# Code changes close with tests and commit

## Answer

A task that modifies code is not closed until relevant tests pass and the completed change is recorded in a descriptive git commit.

FILE:desk/atoms/workflow-model/atom-cli-mutation-testing-uses-sandbox-desk-roots.md
---
id: atom-cli-mutation-testing-uses-sandbox-desk-roots
title: CLI mutation testing uses sandbox desk roots
five_wh_one_plus: how
tags:
- system:deskops
- topic:testing
- topic:cli
- topic:materialization
---

# CLI mutation testing uses sandbox desk roots

## Answer

When testing or exploring mutating deskops CLI commands, agents should point writes at a disposable sandbox root such as `.tmp/deskops-cli-test` instead of the repository's real `desk/`. This keeps generated tasks, lifecycle documents, inbox notes, and other workflow artifacts out of tracked project surfaces unless the mutation is intentionally changing the real desk.

FILE:deskops/config.py
from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from deskops.constants import CURRENT_DESK_FORMAT


class SandboxPolicy(BaseModel):
    enabled: bool = False
    sandbox_root: str | None = None


class VersionExpectations(BaseModel):
    desk_format: str = CURRENT_DESK_FORMAT
    model_version: str = "1.0.0"


class QueueJob(BaseModel):
    run: list[str] = Field(min_length=1, description="argv executed without a shell")
    timeout: int = Field(default=3600, gt=0, description="Seconds before the job is killed")


class DispatchRole(BaseModel):
    role: str = Field(min_length=1, description="RoleDoc id or name")
    harness: str = Field(min_length=1, description="Runtime profile kind / scion harness")
    model_alias: str = Field(min_length=1, description="Scion model size alias")
    harness_auth: str | None = Field(default=None, description="Scion harness auth type")
    env_config: str | None = Field(default=None, description="Path passed to scion start --config")


class DispatchRoles(BaseModel):
    executor: DispatchRole
    tester: DispatchRole


class DispatchConfig(BaseModel):
    project: str = Field(min_length=1, description="Scion project")
    workspace: str = Field(min_length=1, description="Absolute workspace path")
    templates_dir: str = Field(min_length=1, description="Scion project templates folder")
    context_file: str = Field(min_length=1, description="Scion context JSON path")
    roles: DispatchRoles


class DeskConfig(BaseModel):
    project_identity: str = Field(default="unknown-project", description="Canonical project desk identity")
    versions: VersionExpectations = Field(default_factory=VersionExpectations)
    sandbox: SandboxPolicy = Field(default_factory=SandboxPolicy)
    atom_folder_axis: str | None = Field(
        default=None,
        description="Tag namespace used as the physical folder axis for atoms under desk/atoms/. Null keeps flat layout.",
    )
    queue_jobs: dict[str, QueueJob] = Field(
        default_factory=dict,
        description="Host queue job kinds: kind -> {run: argv, timeout: seconds}.",
    )
    dispatch: DispatchConfig | None = Field(
        default=None,
        description="deskops dispatch: scion project, workspace, templates and per-role launch settings.",
    )
    queue_min_available_gb: int = Field(default=8, description="Minimum MemAvailable (GB) to start a queued job.")
    queue_max_psi_avg60: float = Field(default=10, description="Memory PSI some avg60 at or above which jobs wait.")
    load_warnings: list[str] = Field(default_factory=list, exclude=True)

    @property
    def has_load_warnings(self) -> bool:
        return bool(self.load_warnings)

    @classmethod
    def load(cls, desk_root: Path) -> "DeskConfig":
        merged_data: dict[str, Any] = {}
        load_warnings: list[str] = []

        for config_path in (desk_root / "config.json", desk_root / "config.local.json"):
            file_data = _load_json_object(config_path, load_warnings)
            if file_data is None:
                continue
            merged_data = _deep_merge_dicts(merged_data, file_data)

        return cls(**merged_data, load_warnings=load_warnings)


def _load_json_object(path: Path, load_warnings: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        message = f"Failed to parse desk config {path}: {exc.msg}"
        load_warnings.append(message)
        warnings.warn(message, stacklevel=2)
        return None

    if not isinstance(data, dict):
        message = f"Desk config {path} must contain a JSON object at the top level."
        load_warnings.append(message)
        warnings.warn(message, stacklevel=2)
        return None

    return data


def _deep_merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = dict(base)
    for key, override_value in override.items():
        base_value = merged.get(key)
        if isinstance(base_value, dict) and isinstance(override_value, dict):
            merged[key] = _deep_merge_dicts(base_value, override_value)
        else:
            merged[key] = override_value
    return merged

FILE:deskops/queue.py
"""Host job queue: `deskops queue {add|run|list}`.

Post-hooks that run inside a container enqueue heavy jobs (full suite,
integration, push) as JSON files under ``<root>/runs/queue``; a runner on the
host takes them one at a time. A state change is an ``os.replace`` between the
state folders, so a job is always in exactly one of them.
"""

from __future__ import annotations

import contextlib
import fcntl
import io
import json
import os
import signal
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterator

from deskops.cli.render import render
from deskops.config import DeskConfig
from deskops.errors import UsageError

STATES = ("pending", "running", "done", "failed")
LOCK_NAME = "run.lock"
_MEMINFO = Path("/proc/meminfo")
_PRESSURE = Path("/proc/pressure/memory")


def queue_dir(root: Path) -> Path:
    return root / "runs" / "queue"


def _ensure_dirs(queue: Path) -> None:
    for name in (*STATES, "logs"):
        (queue / name).mkdir(parents=True, exist_ok=True)


def _load_config(root: Path) -> DeskConfig:
    return DeskConfig.load(root / "desk")


def _write_job(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def _read_job(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def enqueue(root: Path, kind: str, task_id: str | None, transition: str | None) -> str:
    config = _load_config(root)
    if kind not in config.queue_jobs:
        declared = ", ".join(sorted(config.queue_jobs)) or "(none)"
        raise UsageError(f"Unknown queue job kind '{kind}'. Declared kinds: {declared}")
    task_id = (task_id or os.environ.get("DESKOPS_TASK_ID", "")).strip()
    if not task_id:
        raise UsageError("queue add needs --task or DESKOPS_TASK_ID.")
    transition = (transition if transition is not None else os.environ.get("DESKOPS_TRANSITION", "")).strip()

    queue = queue_dir(root)
    _ensure_dirs(queue)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    while True:
        job_id = f"{now.strftime('%Y%m%dT%H%M%SZ')}-{kind}-{task_id}"
        path = queue / "pending" / f"{job_id}.json"
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        except FileExistsError:
            now = now + timedelta(seconds=1)
            continue
        os.close(fd)
        break
    _write_job(
        path,
        {
            "id": job_id,
            "kind": kind,
            "task_id": task_id,
            "transition": transition,
            "enqueued_at": now.isoformat().replace("+00:00", "Z"),
        },
    )
    return job_id



def _jobs(queue: Path, state: str) -> list[Path]:
    folder = queue / state
    return sorted(folder.glob("*.json")) if folder.is_dir() else []


def _memory_state() -> tuple[float | None, float | None]:
    """(MemAvailable in GB, memory PSI some avg60); None when unreadable."""
    available = None
    try:
        for line in _MEMINFO.read_text(encoding="utf-8").splitlines():
            if line.startswith("MemAvailable:"):
                available = int(line.split()[1]) / (1024 * 1024)
                break
    except (OSError, ValueError, IndexError):
        pass
    avg60 = None
    try:
        for line in _PRESSURE.read_text(encoding="utf-8").splitlines():
            if line.startswith("some "):
                for part in line.split()[1:]:
                    if part.startswith("avg60="):
                        avg60 = float(part.split("=", 1)[1])
    except (OSError, ValueError):
        pass
    return available, avg60


def _wait_reason(config: DeskConfig) -> str | None:
    available, avg60 = _memory_state()
    if available is not None and available < config.queue_min_available_gb:
        return f"memoria disponible {available:.1f} GB < minimo {config.queue_min_available_gb} GB"
    if avg60 is not None and avg60 >= config.queue_max_psi_avg60:
        return f"presion de memoria avg60 {avg60:.2f} >= maximo {config.queue_max_psi_avg60:g}"
    return None


def _notify_failure(root: Path, job: dict[str, Any], *, interrupted: bool) -> None:
    """Leave an inbox note with the function behind `deskops message send`."""
    from deskops.cli.commands.message import MessageCLI

    if interrupted:
        body = f"Trabajo {job['id']} interrumpido. Tipo: {job['kind']}. Tarea: {job['task_id']}."
    else:
        code = "timeout" if job.get("timeout") else job.get("exit_code")
        body = (
            f"Tipo: {job['kind']}. Tarea: {job['task_id']}. "
            f"Codigo de salida: {code}. Log: {job.get('log')}"
        )
    args = SimpleNamespace(
        title=f"queue: {job['id']}",
        message=body,
        kind="unclear",
        root=str(root),
        desk_root=None,
        repo=None,
        store=None,
        pythonpath=None,
        sender=None,
        format="json",
    )
    cwd = os.getcwd()
    try:
        os.chdir(root)
        with contextlib.redirect_stdout(io.StringIO()):
            MessageCLI()._deliver_note(args)
    except Exception as exc:  # the job already failed; a lost note must not hide that
        print(f"Warning: could not leave the inbox note for {job['id']}: {exc}", file=sys.stderr)
    finally:
        os.chdir(cwd)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _recover_interrupted(root: Path, queue: Path) -> None:
    for path in _jobs(queue, "running"):
        job = _read_job(path)
        job.update({"ended_at": _now(), "exit_code": None, "interrupted": True})
        _write_job(path, job)
        os.replace(path, queue / "failed" / path.name)
        _notify_failure(root, job, interrupted=True)


def _execute(root: Path, queue: Path, config: DeskConfig, path: Path) -> bool:
    """Run one pending job; True when it succeeded."""
    running = queue / "running" / path.name
    os.replace(path, running)
    job = _read_job(running)
    spec = config.queue_jobs.get(job["kind"])
    log_path = queue / "logs" / f"{job['id']}.log"
    job["started_at"] = _now()
    job["log"] = str(log_path)
    code: int | None = None
    if spec is None:
        log_path.write_text(f"queue kind '{job['kind']}' is no longer declared in queue_jobs\n", encoding="utf-8")
        code = 127
    else:
        env = dict(os.environ)
        env.update(
            DESKOPS_ROOT=str(root),
            DESKOPS_TASK_ID=job["task_id"],
            DESKOPS_TRANSITION=job.get("transition", ""),
            DESKOPS_JOB_ID=job["id"],
            DESKOPS_JOB_KIND=job["kind"],
        )
        with log_path.open("wb") as log:
            try:
                proc = subprocess.Popen(
                    spec.run, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL, start_new_session=True,
                )
            except OSError as exc:
                log.write(f"cannot start {spec.run}: {exc}\n".encode())
                code = 127
            else:
                try:
                    code = proc.wait(timeout=spec.timeout)
                except subprocess.TimeoutExpired:
                    with contextlib.suppress(ProcessLookupError):
                        os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
                    job["timeout"] = True
                    code = None
    job["ended_at"] = _now()
    if not job.get("timeout"):
        job["exit_code"] = code
    ok = code == 0
    _write_job(running, job)
    os.replace(running, queue / ("done" if ok else "failed") / path.name)
    if not ok:
        _notify_failure(root, job, interrupted=False)
    return ok


@contextlib.contextmanager
def _try_lock(queue: Path) -> Iterator[bool]:
    with (queue / LOCK_NAME).open("a+") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        try:
            yield True
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def run_queue(root: Path, run_all: bool) -> int:
    queue = queue_dir(root)
    _ensure_dirs(queue)
    config = _load_config(root)
    with _try_lock(queue) as locked:
        if not locked:
            print("ocupado: otro queue run en curso")
            return 0
        _recover_interrupted(root, queue)
        while True:
            pending = _jobs(queue, "pending")
            if not pending:
                print("sin trabajos")
                return 0
            reason = _wait_reason(config)
            if reason:
                print(f"en espera: {reason}")
                return 0
            path = pending[0]
            print(f"ejecutando {path.stem}")
            if not _execute(root, queue, config, path):
                print(f"fallo {path.stem}")
                return 1
            print(f"listo {path.stem}")
            if not run_all:
                return 0


def list_jobs(root: Path) -> dict[str, list[dict[str, Any]]]:
    queue = queue_dir(root)
    result: dict[str, list[dict[str, Any]]] = {}
    for state in STATES:
        items = []
        for path in _jobs(queue, state):
            job = _read_job(path)
            job["state"] = state
            items.append(job)
        result[state] = items
    return result


class QueueCLI:
    """`deskops queue {add|run|list}`; the subcommand is required."""

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        cmd = args.queue_command
        if cmd == "add":
            print(enqueue(root, args.kind, args.task, args.transition))
            return 0
        if cmd == "run":
            return run_queue(root, bool(args.all))
        if cmd == "list":
            return render(list_jobs(root), args.format, _format_list)
        raise UsageError(f"Unknown queue command: {cmd}")


def _format_list(data: dict[str, list[dict[str, Any]]]) -> str:
    lines: list[str] = []
    for state in STATES:
        lines.append(f"{state} ({len(data[state])})")
        for job in data[state]:
            extra = ""
            if state in ("done", "failed"):
                extra = " | timeout" if job.get("timeout") else f" | exit {job.get('exit_code')}"
            lines.append(f"  {job['id']} | {job['kind']} | {job['task_id']}{extra}")
    return "\n".join(lines)

FILE:tests/test_cli_grammar.py
"""Classify the top-level CLI grammar by workflow noun.

The parser is generated from ``deskops.cli.registry``; this test states which
top-level nouns are intentional public surfaces so new commands cannot drift
into the namespace just because they exist. It classifies existing nouns only;
it does not change parsing or command behavior.
"""

from __future__ import annotations

from deskops.cli.registry import command_for_path
from deskops.cli.registry import command_registry


TOP_LEVEL_GRAMMAR: dict[str, frozenset[str]] = {
    "operational": frozenset(
        {
            "next",
            "advance",
            "closeout",
            "promote",
            "bind",
            "message",
            "queue",
            "dispatch",
            "graph",
            "drift",
            "runtime",
            "drawer",
            "issue",
            "retire",
            "view",
            "review",
        }
    ),
    "model_crud": frozenset({"add", "edit", "list", "show"}),
    "admin": frozenset(
        {
            "about",
            "doctor",
            "status",
            "faq",
            "bootstrap",
            "init",
            "repo",
            "desk",
        }
    ),
    "mixed": frozenset({"atoms"}),
    "transitional": frozenset({"materialize"}),
}


def test_top_level_nouns_are_classified_exactly_once() -> None:
    classified = [noun for nouns in TOP_LEVEL_GRAMMAR.values() for noun in nouns]

    assert len(classified) == len(set(classified))
    assert set(classified) == {command.path[0] for command in command_registry()}


def test_operational_mutates_guards() -> None:
    assert command_for_path(("next",)).mutates is False
    assert command_for_path(("show",)).mutates is False
    assert command_for_path(("advance",)).mutates is True
    assert command_for_path(("closeout",)).mutates is True
    assert command_for_path(("review",)).mutates is True
    assert command_for_path(("review", "status")).mutates is False
    assert command_for_path(("review", "dispose")).mutates is True

FILE:tests/test_command_registry.py
"""The declared command registry must match the frozen CLI surface.

The help goldens were captured from the hand-built parser by
task-rw-f1-output-golden-files, so comparing registry paths against that
directory catches both dropped commands and accidental new ones.
"""

from __future__ import annotations

from pathlib import Path

from deskops.cli.registry import command_registry


HELP_GOLDENS = Path(__file__).resolve().parent / "fixtures" / "golden" / "help"


def _golden_command_paths() -> set[tuple[str, ...]]:
    paths: set[tuple[str, ...]] = set()
    for path in HELP_GOLDENS.glob("deskops_*.txt"):
        if path.name == "deskops.txt":
            continue
        paths.add(tuple(path.stem.split("_")[1:]))
    return paths


def test_registry_paths_match_help_goldens() -> None:
    declared = {command.path for command in command_registry()}

    assert declared == _golden_command_paths()


def test_registry_paths_are_unique_and_have_parents() -> None:
    commands = command_registry()
    paths = [command.path for command in commands]

    assert len(paths) == len(set(paths))
    declared = set(paths)
    for path in paths:
        assert path
        if len(path) > 1:
            assert path[:-1] in declared


MUTATING_COMMANDS: set[tuple[str, ...]] = {
    ("doctor",),
    ("bootstrap",),
    ("init",),
    ("message",),
    ("message", "send"),
    ("message", "ack"),
    ("queue",),
    ("queue", "add"),
    ("queue", "run"),
    ("dispatch",),
    ("dispatch", "start"),
    ("dispatch", "reap"),
    ("review",),
    ("review", "node"),
    ("review", "preflight"),
    ("review", "bundle"),
    ("review", "dispose"),
    ("review", "record"),
    ("promote",),
    ("promote", "inbox-to-drawer-task"),
    ("drawer",),
    ("drawer", "remove"),
    ("issue",),
    ("issue", "close"),
    ("add",),
    ("add", "task"),
    ("add", "pill"),
    ("add", "ritual"),
    ("add", "board"),
    ("add", "atom"),
    ("add", "materialization"),
    ("add", "repository"),
    ("add", "inbox-note"),
    ("add", "faq-doc"),
    ("add", "step"),
    ("add", "role"),
    ("add", "runtime-profile"),
    ("edit",),
    ("edit", "task"),
    ("edit", "pill"),
    ("edit", "ritual"),
    ("edit", "board"),
    ("edit", "atom"),
    ("edit", "materialization"),
    ("edit", "repository"),
    ("edit", "review"),
    ("edit", "inbox-note"),
    ("edit", "faq-doc"),
    ("edit", "step"),
    ("edit", "role"),
    ("edit", "runtime-profile"),
    ("bind",),
    ("bind", "pill"),
    ("advance",),
    ("advance", "task"),
    ("repo",),
    ("repo", "register"),
    ("repo", "remove"),
    ("retire",),
    ("desk",),
    ("desk", "install"),
    ("desk", "migrate"),
    ("desk", "replace"),
    ("desk", "update"),
    ("atoms",),
    ("atoms", "add-namespace"),
    ("atoms", "reorganize"),
    ("atoms", "create"),
    ("atoms", "delete"),
    ("atoms", "split"),
    ("atoms", "merge"),
    ("atoms", "crossroad"),
    ("atoms", "proto"),
    ("atoms", "type"),
    ("atoms", "citations"),
    ("graph",),
    ("graph", "build"),
    ("graph", "reflect"),
    ("materialize",),
    ("closeout",),
    ("closeout", "commit"),
    ("closeout", "supersede"),
    ("closeout", "retire"),
    ("closeout", "resolved-by"),
    ("closeout", "verify"),
    ("runtime",),
    ("runtime", "init"),
    ("runtime", "stop"),
    ("runtime", "template"),
}


def test_mutating_commands_are_declared_explicitly() -> None:
    """Every command that writes desk files, the store, or git must say so."""
    declared = {command.path for command in command_registry() if command.mutates}

    assert declared == MUTATING_COMMANDS

FILE:instruccion
Cold-bundle de la tarea task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Un archivo de tests nuevo, test_integrate.py en la carpeta tests, pasa con `TMPDIR=/dev/shm pytest -q` sobre ese archivo. Cada test arma en `tmp_path` un repo git real con un desk creado por el CLI, una tarea llevada hasta su cierre con los comandos reales (como lo hacen los tests de closeout vecinos) y un remoto bare local, y comprueba: (a) con gates en verde, el remoto queda con el commit de codigo y el tip en la rama, events.log gana la linea `ok` y el comando imprime `integrado`; (b) `--dry-run` no cambia el remoto e imprime los dos comandos de push; (c) una `suite` que sale con 1 produce `fallo: suite`, codigo 1 y remoto intacto; (d) un rango que solo toca `desk/` no corre la suite (la suite configurada es un comando que fallaria); (e) un tip que no es fast-forward de la rama remota produce `fallo: fast-forward`; (f) una ruta de `.sldb/store.yaml` ausente en el commit produce `fallo: store`; (g) tarea sin cerrar y falta del campo `integrate` salen con codigo 2; (h) tras cualquier corrida no queda ninguna copia temporal bajo TMPDIR.
- Los tests guardianes del CLI pasan con el comando nuevo declarado (`pytest -q tests/test_cli_grammar.py tests/test_command_registry.py` y `pytest -q tests/test_cli.py -k help_uses_deskops_name`) y los goldens de ayuda se regeneran conservando solo los que cambian por el comando nuevo.
- `TMPDIR=/dev/shm pytest -q tests/test_queue.py` sigue pasando.

