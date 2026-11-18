FILE:desk/tasks/task-deskops-dispatch-lanza-y-recoge-por-scion-al-ejecutor-y-al-tester-de-una-tarea-sin-coordinador-agent.md
---
sldb:
  by: agent
  at: '2026-11-18T07:05:36Z'
  authority: generated
  via: save_document_payload
id: task-deskops-dispatch-lanza-y-recoge-por-scion-al-ejecutor-y-al-tester-de-una-tarea-sin-coordinador-agent
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
- deskops/runtime/scion.py
- deskops/config.py
- deskops/cli/registry.py
- docs/operator-manual.md
- tests/test_cli.py
- tests/test_cli_grammar.py
- tests/test_command_registry.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-scion-coordinator-progresses-authorized-work
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops dispatch lanza y recoge por scion al ejecutor y al tester de una tarea sin coordinador agente

## Rationale

_Explain why this task exists or the business driver behind it._

JP quiere que los agentes se lancen solos. Hoy un coordinador agente arma a mano la identidad, el template, el prompt y el scion start de cada ejecutor y tester, y despues detiene y borra el agente. Todo eso es determinista y ya existe como funciones en deskops/runtime/scion.py; falta el comando que las encadena para que la cola del host (deskops queue) lo invoque como trabajo.

## Goal

_Describe the concrete result this task must produce._

Un grupo de comandos nuevo, `deskops dispatch`, con dos subcomandos, y su configuracion en el desk.

Configuracion. `DeskConfig` (`deskops/config.py`) gana un campo `dispatch` con: `project` (proyecto scion), `workspace` (ruta absoluta), `templates_dir` (carpeta de templates del proyecto scion), `context_file` (ruta del JSON de contexto scion) y un mapa `roles` con las claves `executor` y `tester`, cada una con `role` (id o nombre del RoleDoc), `harness`, `model_alias`, `harness_auth` (opcional) y `env_config` (ruta opcional que se pasa a scion start con `--config`). Sin campo `dispatch` los dos subcomandos salen con codigo 2 y un mensaje.

(1) `deskops dispatch start <executor|tester> --task <id> --root .` hace, en orden:
  a. Corre `scion list --project <project> --format json`; si algun agente tiene `phase` igual a `running`, imprime `ocupado: <nombre>` y sale con codigo 3.
  b. Calcula la identidad con `scion_child_identity(<ruta del TaskDoc>, <rol>, 1)`. El run_dir es `runs/subagents/exec-<nombre del agente>` para el ejecutor y `runs/subagents/exec-<nombre del agente>-testing` para el tester (el sufijo va solo en el run_dir, no en el nombre). Si ese run_dir ya existe usa el intento 2; si el del intento 2 tambien existe, sale con codigo 5 y el mensaje `sin intentos: <tarea> <rol>`.
  c. Escribe el template con `materialize_scion_template` (la funcion de `deskops/runtime/scion.py` que usa `deskops runtime template`) con el rol, el harness, el alias y el harness_auth de la configuracion, `mode` igual a `executor` o `tester` segun el subcomando, el context_file, la tarea, el nombre del agente y el run_dir, en la carpeta `<templates_dir>/<nombre del rol>`. Esa llamada tambien escribe el RunDoc.
  d. Corre `scion templates sync <nombre del rol> --project <project>`.
  e. Escribe en `<run_dir>/prompt.md` la salida de `deskops show task <id>` seguida del archivo Markdown completo del TaskDoc.
  f. Arma el argv con `scion_start_argv` (prompt: una linea que nombra la ruta absoluta de prompt.md y pide leerlo completo y cumplirlo; project, workspace, template igual al nombre del rol, harness_auth de la configuracion) y agrega `--config <env_config>` si esta declarado. Lo ejecuta.
  g. Imprime `agente <nombre> run_dir <run_dir>` y sale con el codigo de scion start.

(2) `deskops dispatch reap --task <id> --root .`: de `scion list --project <project> --format json` toma los agentes cuyo `labels["deskops.task_id"]` es igual al valor que `scion_child_identity` pone en esa etiqueta para la tarea. Para cada uno decide, en este orden de prioridad, el motivo de termino: `phase` distinta de `running` (motivo `phase:<valor>`); `activity` igual a `completed`, `blocked` o `limits_exceeded` (motivo `activity:<valor>`); existe `result-summary.md` en su run_dir, que se deduce del nombre y del rol como en (1)b (motivo `result-summary`). A cada terminado le corre `scion stop <nombre> --project <project>` y `scion delete <nombre> --project <project> --yes`. Imprime una linea por agente: `<nombre> <rol> <motivo>` o `<nombre> <rol> vivo`. Sale con codigo 0 si no queda ninguno vivo y con codigo 4 si alguno sigue vivo.

Todas las llamadas a scion pasan por una sola funcion del modulo que recibe el argv y usa `subprocess.run`. Los tests no la reemplazan en Python: ponen primero en el PATH un ejecutable llamado scion, escrito por el test, que guarda cada argv recibido en un archivo y contesta `scion list` con un JSON que el test controla.

## Scope

_State what is in scope and what is out of scope._

Dentro: un modulo nuevo llamado dispatch.py en el paquete deskops, el campo en `deskops/config.py`, el registro del grupo en `deskops/cli/registry.py`, el archivo de tests nuevo, las declaraciones del grupo en `tests/test_cli.py`, `tests/test_cli_grammar.py` y `tests/test_command_registry.py`, los goldens de ayuda, y `docs/operator-manual.md` con un ejemplo de `queue_jobs` que usa estos comandos. Fuera: integrar y pushear (otra tarea); declarar configuracion u hooks en desks reales; cambios en scion. Checkout principal, sin worktree ni rama, sin git add ni git commit.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- Un archivo de tests nuevo, test_dispatch.py en la carpeta tests, pasa con `TMPDIR=/dev/shm pytest -q` sobre ese archivo. Con el scion de prueba en el PATH y un desk desechable de `tmp_path` con roles y una tarea creados por el CLI, comprueba: (a) `dispatch start executor` ejecuta `templates sync` y `start` con el argv esperado (nombre, tipo, proyecto, workspace, etiquetas, `--config`), deja el template, el RunDoc y prompt.md; (b) lo mismo para tester con su run_dir terminado en `-testing`; (c) con un agente en phase running sale con 3 y no ejecuta start; (d) el segundo start de la misma tarea y rol usa el intento 2 y el tercero sale con 5; (e) `dispatch reap` detiene y borra por cada uno de los tres motivos, deja vivo al que sigue trabajando y sale con 4; (f) sin campo `dispatch` en la configuracion los dos subcomandos salen con 2.
- `TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py` sigue pasando.
- Los tests guardianes del CLI pasan con el grupo nuevo declarado: `pytest -q tests/test_cli_grammar.py tests/test_command_registry.py` y `pytest -q tests/test_cli.py -k help_uses_deskops_name`; los goldens de ayuda se regeneran con `pytest -n 4 tests/test_output_goldens.py -k help --update-golden` conservando solo los que cambian por el grupo nuevo.

## Done When

_Name the observable condition that makes the task complete._

Con un scion falso en el PATH y un desk desechable, dispatch start arma y ejecuta el argv esperado para ejecutor y tester y se niega si hay un agente vivo; dispatch reap detiene y borra los terminados y deja los vivos.

FILE:desk/atoms/workflow-model/atom-scion-coordinator-progresses-authorized-work.md
---
sldb:
  by: agent
  at: '2026-11-10T17:16:49Z'
  authority: generated
  via: update_document
id: atom-scion-coordinator-progresses-authorized-work
title: Scion coordinator progresses authorized work
five_wh_one_plus: how
tags:
- system:deskops
- topic:workflow
- topic:scion
- topic:autonomy
provenance: desk/tasks/task-scion-autonomy-coordinator-contract.md
---

# Scion coordinator progresses authorized work

## Answer

A Scion coordinator is a long-lived workflow supervisor, not a second scheduler or lifecycle engine. It recovers the configured current desk and tool sources from runtime context, checks canonical and dirty repository state, reads Board order and lifecycle/review gates, and inspects existing ownership from Scion labels, RunDoc and worktrees before selecting work. Source roots are tool import locations; implementation and test commands run from the configured desk_root, which is the task repository containing desk/. It skips tasks owned by another agent, but reconciles its own existing executor/tester lanes and completed handoffs first: a restart or successful child completion never makes the coordinator skip its own task or launch a duplicate. Only after that reconciliation does it select one dependency-ready unowned leaf; Board order is the only tie-breaker.

Reconciliation distinguishes Scion activity from phase. The native bridge can report phase=running while activity=completed; inspect activity=completed and the handoff evidence before deciding the child is still busy, using activity first and phase only as fallback. The coordinator may mutate modeled workflow state through the deskops and sldb CLIs, including routing, review disposition, run intent, advancement and closeout, but it never implements code. Ordinary factual or implementation questions are answered from task and source evidence; only unresolved owner decisions, real ownership conflicts, external credentials or permissions, and genuine human decisions are escalated. An accepted review is never rerun with unchanged input; technical retries are bounded to two attempts per unchanged input, and implementation correction plus independent retest cycles are bounded to two per task contract.

A dependency-ready authored task that still lacks preflight or bundle receipts is routine coordinator work, not a human blocker. The coordinator runs the existing cheap context-review CLI/ritual, adjudicates factual findings, and only then treats the task as reviewed-ready for dispatch; implementation waits until the execution gates pass. Dispatch identity is deterministic from the task contract: deskops-e for an executor or deskops-t for an independent tester, plus the first 12 hex characters of SHA256 over task id, NUL, the SLDB task contract digest, NUL and role. Attempt 1 uses that base name; attempt 2 appends -a2; there is no attempt 3. The child carries labels deskops.task_id, deskops.contract_sha256, deskops.role and deskops.attempt.

The coordinator writes RunDoc launch intent with outcome in_progress in the assigned run_dir before start; the summary says this is launch intent, not proof of start. Reconciliation reuses an existing matching RunDoc without rewriting it, and only a missing intent calls the runtime template to create one; a retry gets a new run_dir. A matching activity=completed child is inspected and its handoff reviewed before any correction launch; a stopped child resumes the same identity; unknown or unavailable Scion state is recorded as a blocker instead of duplicated. RunDoc attempts and evidence are immutable.

One executor runs per repository. A successful executor is followed by an independent tester with its own role identity and tester scope; a failed tester cannot support closeout, so the coordinator requests one bounded correction and a fresh test while preserving the failure evidence. After reviewing evidence the coordinator runs closeout verify, reviews the diff, and stages only the scoped implementation, evidence and review paths with deskops closeout commit --paths; it never uses git add -A. It reconciles the phase, then recovers and selects again. Only after all authorized work is closed, declared evidence verified and required phase integration/commit done does it write the final evidence summary and call sciontool status task_completed; an external blocker is persisted and signalled as blocked, while only an actual owner decision uses ask_user. Runtime context names absolute workspace, desk, source and sldb source roots plus the Scion project, emits DESKOPS_* environment variables and a workspace volume, and never carries secrets. Native Scion label values are printable ASCII of at most63characters. The helper preserves the full canonical contract hash and task id for name derivation and TaskDoc/RunDoc metadata, while the native contract label is its63-hex prefix. Short printable-ASCII task-id labels stay literal; longer or non-ASCII ids use a stable bounded hash descriptor. Copy helper labels exactly instead of reconstructing invalid64-hex labels.

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

FILE:deskops/runtime/scion.py
"""Project a RoleDoc + its RuntimeProfileDoc onto a Scion agent template.

Scion (github.com/GoogleCloudPlatform/scion) launches an agent from a
*template* directory: ``scion-agent.yaml`` plus the prose files it points at
(``system-prompt.md``, ``agents.md``). A template describes the job, never the
environment: the harness-config decides image, auth and concrete model, and
the template only carries a portable model *size alias*.

This module is the Scion counterpart of ``materializers.roles`` (pi agent
files): the RoleDoc stays the tracked source and the template is a
materialization. Pure except for the two writers at the bottom; it never
calls ``scion``. Dispatch (``scion start``) is the supervisor's gesture.

Nothing is dropped silently: every RoleDoc setting the template cannot carry
is written into ``scion-agent.yaml`` as a comment that names the setting and
why it was left out.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any

from sldb.runtime.validation import extract_model_data
from sldb.store.graph.language.contract_hash import contract_hash
from sldb.store.hashing import hash_fields_with_map

from deskops import doc_access
from deskops.materializers.roles import iter_role_doc_paths, load_role_doc
from deskops.materializers.runtime_profiles import build_agent_spec_args, load_runtime_profiles
from deskops.models import RunDoc, TaskDoc

#: RuntimeProfileDoc.kind -> Scion harness-config name. Only ``claude`` and
#: ``gemini`` ship installed; the rest need ``scion harness-config install``
#: (``pi`` needs a bundle of our own; see the scion fork's desk).
HARNESS_BY_KIND: dict[str, str] = {
    "claude": "claude",
    "codex": "codex",
    "antigravity": "antigravity",
    "gemini": "gemini",
    "opencode": "opencode",
    "pi": "pi",
}

#: Scion's portable model size aliases (``local/templates.md``).
MODEL_SIZE_ALIASES: tuple[str, ...] = ("small", "medium", "large", "extra-large")

#: ``medium`` by default: the owner's rule is that subagents never run on the
#: largest tier. Pass ``model_alias`` to change it per template.
DEFAULT_MODEL_ALIAS = "medium"
DEFAULT_MAX_TURNS = 200
DEFAULT_MAX_DURATION = "2h"
#: A coordinator waits blocked on its children and Scion counts that idle time,
#: so the executor's limit would kill it mid-review.
COORDINATOR_MAX_TURNS = 1000
COORDINATOR_MAX_DURATION = "24h"

#: Without this the Hub picks whichever credential it finds; a stale
#: ``CLAUDE_AUTH`` file beats a project token and the agent is not logged in.
HARNESS_AUTH: dict[str, str] = {"claude": "oauth-token"}

#: Auth a ``scion start`` names when nobody chose one: the same default the
#: claude template carries, so a coordinator never launches a subscription
#: child with ``api-key`` (it would ask for ANTHROPIC_API_KEY and not start).
DEFAULT_HARNESS_AUTH = HARNESS_AUTH["claude"]

#: Auth types a template may select (``auth_selectedType``); the harness-config
#: decides which secrets each one needs (claude: oauth-token ->
#: CLAUDE_CODE_OAUTH_TOKEN, auth-file -> the CLAUDE_AUTH credentials file).
HARNESS_AUTH_TYPES: tuple[str, ...] = ("api-key", "oauth-token", "auth-file", "vertex-ai")

TEMPLATE_FILES: tuple[str, ...] = ("scion-agent.yaml", "system-prompt.md", "agents.md")

#: The only keys a Scion runtime context may carry. Paths are absolute and inside
#: ``workspace_root``; ``project`` is the Scion project slug or UUID, never a path.
SCION_CONTEXT_KEYS: tuple[str, ...] = ("project", "workspace_root", "desk_root", "source_root", "sldb_root")

#: Optional container keys: how this machine runs the agent, not where the desk is.
#: ``memory_limit``/``cpu_limit`` become ``resources.limits``; ``shared_paths`` are host
#: paths bound at the same path (e.g. ``/dev/shm``, so tests share the host's tmpfs and
#: its lock files); ``env`` adds static variables (e.g. ``TMPDIR``). Omitted: no change.
SCION_CONTEXT_OPTIONAL_KEYS: tuple[str, ...] = ("memory_limit", "cpu_limit", "shared_paths", "env")

_PROJECT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_MEMORY_RE = re.compile(r"^[0-9]+(\.[0-9]+)?([KMGT]i?)?$")
_CPU_RE = re.compile(r"^[0-9]+(\.[0-9]+)?$")
_ENV_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
#: Variables the context already derives; ``env`` may not redefine them.
_DERIVED_ENV = frozenset(
    {"DESKOPS_DESK_ROOT", "DESKOPS_SOURCE_ROOT", "DESKOPS_SLDB_SOURCE_ROOT", "DESKOPS_WORKSPACE_ROOT",
     "DESKOPS_SCION_PROJECT", "PYTHONPATH"}
)


def _context_absolute_path(key: str, value: object) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"context {key} must be a non-empty absolute path")
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise ValueError(f"context {key} must be an absolute path, got '{value}'")
    return path.resolve()


def _validate_container_keys(context: dict[str, Any], workspace_root: Path) -> dict[str, Any]:
    """The optional container keys, validated; absent keys are left out."""
    resolved: dict[str, Any] = {}
    if "memory_limit" in context:
        value = context["memory_limit"]
        if not isinstance(value, str) or _MEMORY_RE.fullmatch(value.strip()) is None:
            raise ValueError(f"context memory_limit must be a size such as '6Gi' or '6G', got {value!r}")
        resolved["memory_limit"] = value.strip()
    if "cpu_limit" in context:
        value = context["cpu_limit"]
        if not isinstance(value, str) or _CPU_RE.fullmatch(value.strip()) is None or float(value) <= 0:
            raise ValueError(f"context cpu_limit must be a positive number of cores as a string, got {value!r}")
        resolved["cpu_limit"] = value.strip()
    if "shared_paths" in context:
        value = context["shared_paths"]
        if not isinstance(value, list):
            raise ValueError("context shared_paths must be a list of absolute host paths")
        paths: list[str] = []
        for item in value:
            path = _context_absolute_path("shared_paths", item)
            if not path.exists():
                raise ValueError(f"context shared_paths entry does not exist on this host: {path}")
            if path == workspace_root:
                raise ValueError(f"context shared_paths must not repeat workspace_root: {path}")
            if str(path) not in paths:
                paths.append(str(path))
        resolved["shared_paths"] = paths
    if "env" in context:
        value = context["env"]
        if not isinstance(value, dict):
            raise ValueError("context env must be an object of NAME: value strings")
        env: dict[str, str] = {}
        for name, item in value.items():
            if not isinstance(name, str) or _ENV_NAME_RE.fullmatch(name) is None:
                raise ValueError(f"context env name is not a valid variable name: {name!r}")
            if name in _DERIVED_ENV:
                raise ValueError(f"context env must not redefine {name}; the context derives it")
            if not isinstance(item, str):
                raise ValueError(f"context env {name} must be a string")
            env[name] = item
        resolved["env"] = env
    return resolved


def validate_scion_context(context: dict[str, Any]) -> dict[str, Any]:
    """Validate the five-key runtime context before any template output is written.

    ``project`` is a non-empty Scion slug or UUID. Every other value is an
    absolute directory: ``workspace_root`` contains the rest, ``desk_root``
    contains ``desk/``, ``source_root`` contains the ``deskops`` package and
    ``sldb_root`` is sldb's ``src`` directory. Missing, unknown, relative,
    outside-workspace or invalid paths are refused with no partial defaults.
    """
    if not isinstance(context, dict):
        raise ValueError("Scion context must be a JSON object")
    missing = [key for key in SCION_CONTEXT_KEYS if key not in context]
    unknown = sorted(
        str(key) for key in context if key not in SCION_CONTEXT_KEYS and key not in SCION_CONTEXT_OPTIONAL_KEYS
    )
    if missing:
        raise ValueError(f"Scion context is missing required key(s): {', '.join(missing)}")
    if unknown:
        raise ValueError(f"Scion context has unknown key(s): {', '.join(unknown)}")

    project = context["project"]
    if not isinstance(project, str) or not project.strip():
        raise ValueError("context project must be a non-empty Scion slug or UUID")
    project = project.strip()
    if "/" in project or "\\" in project or project in {".", ".."} or _PROJECT_RE.fullmatch(project) is None:
        raise ValueError(f"context project must be a Scion slug or UUID, not a filesystem path: '{project}'")

    workspace_root = _context_absolute_path("workspace_root", context["workspace_root"])
    if not workspace_root.is_dir():
        raise ValueError(f"context workspace_root is not a directory: {workspace_root}")
    resolved: dict[str, Any] = {"project": project, "workspace_root": str(workspace_root)}
    for key in SCION_CONTEXT_KEYS[2:]:
        path = _context_absolute_path(key, context[key])
        try:
            path.relative_to(workspace_root)
        except ValueError as exc:
            raise ValueError(f"context {key} must be inside workspace_root ({workspace_root}): {path}") from exc
        resolved[key] = str(path)

    if not (Path(resolved["desk_root"]) / "desk").is_dir():
        raise ValueError(f"context desk_root must be the repository root containing desk/: {resolved['desk_root']}")
    if not (Path(resolved["source_root"]) / "deskops").is_dir():
        raise ValueError(f"context source_root must be the repository root containing the deskops package: {resolved['source_root']}")
    if not (Path(resolved["sldb_root"]) / "sldb").is_dir():
        raise ValueError(f"context sldb_root must be the sldb src directory containing the sldb package: {resolved['sldb_root']}")
    resolved.update(_validate_container_keys(context, workspace_root))
    return resolved


def load_scion_context(path: Path) -> dict[str, Any]:
    """Read and validate a JSON context file; nothing is generated before this succeeds."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read Scion context file {path}: {exc}") from exc
    return validate_scion_context(raw)


def task_contract_sha256(markdown: str) -> str:
    """The SLDB ``__contract__`` digest of a task document (no local hash recipe)."""
    try:
        _, field_hashes = hash_fields_with_map(TaskDoc, markdown)
        return contract_hash(TaskDoc, field_hashes)
    except Exception as exc:  # noqa: BLE001 - surface the model's own diagnostic
        raise ValueError(f"cannot read the task contract: {exc}") from exc


def _scion_task_label(task_id: str) -> str:
    """Bound native metadata without altering the canonical task identity."""
    if len(task_id) <= 63 and all(0x20 <= ord(char) <= 0x7E for char in task_id):
        return task_id
    return "t-" + hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:61]


def scion_child_identity(task_path: str | Path, role: str, attempt: int = 1) -> dict[str, Any]:
    """Deterministic Scion child name and labels for one task contract and role.

    Status, history and references never move the identity; the SLDB task
    ``__contract__`` digest does, so a goal/scope/files/validation change does.
    Attempt is exactly 1 or 2: attempt 2 appends ``-a2`` and a third attempt is
    refused. This helper derives identity only; it does not start anything.
    """
    role_name = str(role).strip().lower()
    if role_name not in {"executor", "tester", "specialist"}:
        raise ValueError(f"role must be executor, tester or specialist, got '{role}'")
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt not in {1, 2}:
        raise ValueError(f"attempt must be 1 or 2, got {attempt!r}")

    path = Path(task_path)
    try:
        markdown = path.read_text(encoding="utf-8")
        task_id = str(extract_model_data(TaskDoc, markdown)["id"])
    except Exception as exc:  # noqa: BLE001 - one diagnostic for an unreadable task
        raise ValueError(f"cannot read task {path}: {exc}") from exc
    contract_sha256 = task_contract_sha256(markdown)
    digest = hashlib.sha256(f"{task_id}\0{contract_sha256}\0{role_name}".encode("utf-8")).hexdigest()[:12]
    prefix = {"executor": "deskops-e", "tester": "deskops-t", "specialist": "deskops-s"}[role_name]
    name = f"{prefix}-{digest}" + ("-a2" if attempt == 2 else "")
    return {
        "name": name,
        "task_id": task_id,
        "contract_sha256": contract_sha256,
        "role": role_name,
        "attempt": attempt,
        "labels": {
            "deskops.task_id": _scion_task_label(task_id),
            "deskops.contract_sha256": contract_sha256[:63],
            "deskops.role": role_name,
            "deskops.attempt": str(attempt),
        },
    }


def scion_start_argv(
    identity: dict[str, Any],
    *,
    prompt: str,
    project: str,
    workspace: str,
    template: str,
    harness_auth: str | None = DEFAULT_HARNESS_AUTH,
) -> list[str]:
    """The explicit native Scion start argv for one deterministic child identity.

    ``harness_auth`` is the auth the child's template selects (``auth_selectedType``);
    by default ``oauth-token``, the claude template default. ``None`` leaves
    ``--harness-auth`` out so the child's template decides alone.
    """
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    if harness_auth is not None and harness_auth not in HARNESS_AUTH_TYPES:
        raise ValueError(f"harness auth must be one of {HARNESS_AUTH_TYPES}, got '{harness_auth}'")
    argv = [
        "scion",
        "start",
        str(identity["name"]),
        prompt,
        "--type",
        template,
        "--project",
        project,
        "--workspace",
        workspace,
        *(["--harness-auth", harness_auth] if harness_auth is not None else []),
        "--non-interactive",
    ]
    for key, value in (identity.get("labels") or {}).items():
        argv += ["--label", f"{key}={value}"]
    return argv


def pick_harness_config(runtime_kind: str) -> str:
    """Scion harness-config name for a RuntimeProfileDoc kind."""
    try:
        return HARNESS_BY_KIND[runtime_kind]
    except KeyError as exc:
        known = ", ".join(sorted(HARNESS_BY_KIND))
        raise ValueError(f"no Scion harness-config is known for runtime kind '{runtime_kind}' (known: {known})") from exc


def find_role_doc(root: Path, role_id: str) -> tuple[Path, dict[str, Any]]:
    """Locate a tracked RoleDoc by ``id`` or ``name`` (``role-x`` and ``x`` both resolve)."""
    wanted = {role_id, f"role-{role_id}"}
    for path in iter_role_doc_paths(root):
        role_doc = load_role_doc(path)
        if role_doc.get("id") in wanted or role_doc.get("name") in wanted:
            return path, role_doc
    raise ValueError(f"no RoleDoc with id or name '{role_id}' under {root / 'desk' / 'roles'}")


def template_dir_for(root: Path, role_doc: dict[str, Any], out_dir: Path | None = None) -> Path:
    """Default destination: ``<root>/.scion/templates/<role-name>/`` (a Scion project template)."""
    if out_dir is not None:
        return out_dir
    name = str(role_doc.get("name") or role_doc.get("id") or "").strip()
    if not name:
        raise ValueError("Role doc is missing a name")
    return root / ".scion" / "templates" / name


def _yaml_scalar(value: Any) -> str:
    """One-line YAML for a scalar or list: JSON is a YAML subset, and it never wraps."""
    return json.dumps(value, ensure_ascii=False)


def _command_args(role_doc: dict[str, Any], profile: dict[str, Any]) -> list[str]:
    """Role settings that only exist as CLI flags (today: ``tools``).

    Model and system prompt have template fields of their own, the session is
    Scion's, and the profile's ``extra_args`` describe a non-interactive
    invocation (``--print``) that Scion must not inherit. What is left is the
    tools vocabulary, folded through the profile's own flag.
    """
    stripped = dict(profile)
    stripped.update(model_flag="", fallback_models_flag="", system_prompt_flag="", session_flag="", extra_args=[])
    args = list(build_agent_spec_args(role_doc, stripped))
    # Scion puts the task prompt (and more options) after command_args. A variadic
    # flag such as Claude's ``--allowedTools <tools...>`` would swallow the prompt as
    # one more tool, so every flag/value pair is emitted as a single ``flag=value``.
    return [f"{flag}={value}" for flag, value in zip(args[::2], args[1::2], strict=True)]


def scion_template_files(
    role_doc: dict[str, Any],
    profile: dict[str, Any],
    *,
    harness: str,
    model_alias: str = DEFAULT_MODEL_ALIAS,
    task_repo: str | None = None,
    source: str | None = None,
    mode: str | None = None,
    context: dict[str, Any] | None = None,
    harness_auth: str | None = None,
) -> dict[str, str]:
    """Render the three template files as ``{filename: text}``.

    ``source`` is a human-readable provenance line (role path + runtime path)
    written at the top of ``scion-agent.yaml``. ``mode`` picks the
    ``agents.md``: ``executor`` (one bounded task), ``tester`` (independent
    verification), ``specialist`` (leaves the sldb store clean) or ``coordinator`` (owns a desk); by default the selected
    role's own name/id decides, and an explicit mode always wins.

    ``context`` is the optional five-key Scion runtime context. Omitted, the
    CLI and path/environment behavior is preserved; the generated prompt text is
    corrected intentionally rather than kept byte-identical. Supplied, it adds
    the DESKOPS_* environment, a workspace volume and concrete command paths.
    """
    if mode not in (None, "executor", "coordinator", "tester", "specialist"):
        raise ValueError(f"mode must be executor, coordinator, tester or specialist, got '{mode}'")
    if harness_auth is not None and harness_auth not in HARNESS_AUTH_TYPES:
        raise ValueError(f"harness auth must be one of {HARNESS_AUTH_TYPES}, got '{harness_auth}'")
    if model_alias not in MODEL_SIZE_ALIASES:
        raise ValueError(f"model alias must be one of {MODEL_SIZE_ALIASES}, got '{model_alias}'")
    if harness not in HARNESS_BY_KIND.values():
        raise ValueError(f"unknown Scion harness-config '{harness}' (known: {', '.join(sorted(set(HARNESS_BY_KIND.values())))})")

    runtime_context = validate_scion_context(context) if context is not None else None

    role_name = str(role_doc.get("name") or role_doc.get("id") or "role")
    role_id = str(role_doc.get("id") or "")
    if mode:
        resolved_mode = mode
    elif role_name.endswith("-tester") or role_id.endswith("-tester"):
        resolved_mode = "tester"
    elif role_name.endswith("-specialist") or role_id.endswith("-specialist"):
        resolved_mode = "specialist"
    elif (
        "supervisor" in role_name
        or "coordinator" in role_name
        or "supervisor" in role_id
        or "coordinator" in role_id
    ):
        resolved_mode = "coordinator"
    else:
        resolved_mode = "executor"
    description = str(role_doc.get("description") or "").strip()
    body = str(role_doc.get("body") or "").strip()
    unsupported = set(profile.get("unsupported_role_fields") or [])

    lines: list[str] = []
    lines.append(f"# Generated by `deskops runtime template {role_doc.get('id') or role_name} --harness {harness}`.")
    if source:
        lines.append(f"# Source: {source}")
    lines.append("# Edit the RoleDoc / RuntimeProfileDoc and regenerate; do not edit this file by hand.")
    lines.append('schema_version: "1"')
    lines.append(f"description: {_yaml_scalar(description or role_name)}")
    lines.append("agent_instructions: agents.md")
    lines.append("system_prompt: system-prompt.md")
    lines.append(f"default_harness_config: {harness}")

    concrete_model = role_doc.get("model")
    if concrete_model:
        lines.append(
            f"# RoleDoc.model is {_yaml_scalar(concrete_model)}. A template carries a portable size alias; "
            f"the harness-config '{harness}' resolves it to a concrete model (Scion local/templates.md)."
        )
    lines.append(f"model: {model_alias}")
    auth_type = harness_auth or HARNESS_AUTH.get(harness)
    if auth_type:
        lines.append(f"auth_selectedType: {auth_type}")
    coordinator = resolved_mode == "coordinator"
    lines.append(f"max_turns: {COORDINATOR_MAX_TURNS if coordinator else DEFAULT_MAX_TURNS}")
    lines.append(f"max_duration: {COORDINATOR_MAX_DURATION if coordinator else DEFAULT_MAX_DURATION}")

    command_args = _command_args(role_doc, profile)
    if command_args:
        lines.append("# RoleDoc.tools, folded through the runtime profile's tools flag:")
        lines.append(f"command_args: {_yaml_scalar(command_args)}")

    if runtime_context is not None:
        lines.append("# Runtime context from --context-file (absolute paths, no secrets):")
        lines.append("env:")
        for key, value in (
            ("DESKOPS_DESK_ROOT", runtime_context["desk_root"]),
            ("DESKOPS_SOURCE_ROOT", runtime_context["source_root"]),
            ("DESKOPS_SLDB_SOURCE_ROOT", runtime_context["sldb_root"]),
            ("DESKOPS_WORKSPACE_ROOT", runtime_context["workspace_root"]),
            ("DESKOPS_SCION_PROJECT", runtime_context["project"]),
            ("PYTHONPATH", runtime_context["source_root"] + os.pathsep + runtime_context["sldb_root"]),
        ):
            lines.append(f"  {key}: {_yaml_scalar(value)}")
        for key, value in (runtime_context.get("env") or {}).items():
            lines.append(f"  {key}: {_yaml_scalar(value)}")
        lines.append("volumes:")
        for path in (runtime_context["workspace_root"], *(runtime_context.get("shared_paths") or [])):
            lines.append(f"  - source: {_yaml_scalar(path)}")
            lines.append(f"    target: {_yaml_scalar(path)}")
        limits = [(key, runtime_context[f"{key}_limit"]) for key in ("cpu", "memory") if runtime_context.get(f"{key}_limit")]
        if limits:
            lines.append("resources:")
            lines.append("  limits:")
            lines.extend(f"    {key}: {_yaml_scalar(value)}" for key, value in limits)

    omitted: list[str] = []
    fallback_models = role_doc.get("fallback_models") or []
    if fallback_models:
        reason = (
            f"RuntimeProfileDoc '{profile.get('id') or profile.get('kind')}' lists it in unsupported_role_fields"
            if "fallback_models" in unsupported
            else "a Scion template has no field for it"
        )
        omitted.append(f"fallback_models: {_yaml_scalar(list(fallback_models))}  ({reason})")
    tools = role_doc.get("tools") or []
    if tools and not command_args:
        reason = (
            f"RuntimeProfileDoc '{profile.get('id') or profile.get('kind')}' lists it in unsupported_role_fields"
            if "tools" in unsupported
            else f"RuntimeProfileDoc '{profile.get('id') or profile.get('kind')}' declares no tools_flag"
        )
        omitted.append(f"tools: {_yaml_scalar(list(tools))}  ({reason})")
    for key in ("system_prompt_mode", "inherit_project_context", "inherit_skills", "default_context"):
        if key in role_doc and role_doc.get(key) not in (None, ""):
            omitted.append(f"{key}: {_yaml_scalar(role_doc[key])}  (pi agent setting; Scion templates have no equivalent)")
    if omitted:
        lines.append("# Omitted on purpose (nothing is dropped silently):")
        lines.extend(f"#   {item}" for item in omitted)

    agent_yaml = "\n".join(lines) + "\n"
    system_prompt = (body or f"# {role_name}") + "\n"
    if resolved_mode == "coordinator":
        agents_md = _render_coordinator_agents_md(
            role_name, harness, task_repo, runtime_context, child_auth=auth_type or DEFAULT_HARNESS_AUTH
        )
    elif resolved_mode == "tester":
        agents_md = _render_tester_agents_md(role_name, harness, task_repo, runtime_context)
    elif resolved_mode == "specialist":
        agents_md = _render_specialist_agents_md(role_name, harness, task_repo, runtime_context)
    else:
        agents_md = _render_agents_md(role_name, harness, task_repo, runtime_context)
    return {"scion-agent.yaml": agent_yaml, "system-prompt.md": system_prompt, "agents.md": agents_md}


def _example_roots(task_repo: str | None, context: dict[str, str] | None) -> tuple[str, str, str, str]:
    """(workspace, desk_root, source_root, project) for generated command examples."""
    if context is not None:
        return context["workspace_root"], context["desk_root"], context["source_root"], context["project"]
    repo = task_repo or "<repo>"
    return "/workspace", f"/workspace/{repo}", "/workspace/deskops", "<project>"


def _render_coordinator_agents_md(
    role_name: str,
    harness: str,
    task_repo: str | None,
    context: dict[str, str] | None,
    *,
    child_auth: str = DEFAULT_HARNESS_AUTH,
) -> str:
    """Instructions for the long-lived agent that owns one desk.

    ``child_auth`` is the ``--harness-auth`` its ``scion start`` examples name:
    the auth this coordinator's own template selected, ``oauth-token`` by default.

    One coordinator per desk is the shape the owner chose (2026-10-29). It
    mutates modeled workflow state through the CLIs, never implements code,
    dispatches one executor/tester at a time and reconciles before acting.
    """
    repo = task_repo or "<repo>"
    workspace, desk_root, source_root, project = _example_roots(task_repo, context)
    sldb_root = str((context or {}).get("sldb_root", "<sldb_root>"))
    return (
        f"# {role_name}: coordinator of the `{repo}` desk on Scion ({harness})\n"
        "\n"
        "You are the long-lived coordinator of ONE desk. The desk, not your memory, holds the state; every time you\n"
        "wake up, recover the configured current state again. You are the only agent that writes this desk's\n"
        "workflow documents, and you do that with the CLIs, never by editing source code.\n"
        "\n"
        "## Configured current state\n"
        "\n"
        "Use the absolute roots supplied by the template environment; do not infer them from the current cwd.\n"
        "Run implementation and validation commands from the actual desk_root, not from a descriptive repo alias.\n"
        "The source and sldb roots are tool import locations, not task write locations.\n"
        "\n"
        "```bash\n"
        f"cd {desk_root}\n"
        f"deskops show board Board --root {desk_root}\n"
        f"deskops list tasks --root {desk_root}\n"
        f"deskops message list --root {desk_root}\n"
        "git status --short --branch\n"
        f"scion list --project {project} --format json\n"
        "```\n"
        "\n"
        f"The source checkout is `{source_root}`; the sldb source is `{sldb_root}`.\n"
        "A stale, dirty or unreadable state is a finding to report, not a reason to guess.\n"
        "\n"
        "## Each cycle\n"
        "\n"
        "1. **Reconcile ownership first.** Inspect existing executor/tester lanes by exact project, name and labels,\n"
        "   and read their RunDoc and handoff evidence. Distinguish Scion activity from phase: activity=completed\n"
        "   with phase=running means the child completed, so inspect activity=completed first and use phase only as\n"
        "   fallback (Scion v0.2.21 uses activity first). Reconcile your OWN completed or stopped lane before\n"
        "   selecting anything; a restart or successful child completion must not skip your own task or launch a\n"
        "   duplicate. Skip only tasks owned elsewhere. A conflicting owner blocks that task only; unknown or\n"
        "   unavailable Scion state is recorded as a blocker.\n"
        "2. **Select and prepare one leaf.** After reconciling your own lanes, select one dependency-ready unowned\n"
        "   leaf from Board order (the only deterministic tie-breaker). If its preflight or bundle receipt is missing,\n"
        "   run the existing cheap context-review CLI/ritual and adjudicate factual findings: this is routine\n"
        "   coordinator work, not a human blocker. Do not implement until the execution gates pass.\n"
        "3. **Derive identity before dispatch.** For role `executor` or `tester`, compute the child name as\n"
        "   `deskops-e-<12hex>` or `deskops-t-<12hex>`, where the 12 hex are SHA256 of\n"
        "   `task_id + NUL + contract_sha256 + NUL + role`. `contract_sha256` is the SLDB TaskDoc `__contract__`\n"
        "   digest, not a raw file hash. Attempt 1 uses the base name; attempt 2 appends `-a2`; there is no attempt 3.\n"
        "   Labels are `deskops.task_id`, `deskops.contract_sha256`, `deskops.role`, `deskops.attempt`. The runtime\n"
        "   helper `scion_child_identity(task_path, role, attempt)` returns this name and label set.\n"
        "   Copy the helper labels exactly: native values must be printable ASCII and at most 63 characters.\n"
        "   The contract label is the 63-hex prefix; invalid/long task-id labels use a bounded hash descriptor.\n"
        "   Full task id and full canonical contract hash remain in TaskDoc/RunDoc and name derivation; never\n"
        "   paste the full 64-hex hash as a native label or change the canonical contract to fit labels.\n"
        "4. **Reuse or write intent, then start.** A matching RunDoc is reused without rewriting it; only a missing\n"
        "   intent calls the runtime template to create the in_progress RunDoc. Its summary says launch intent, not\n"
        "   proof of start. Write that intent before the native Scion start; a retry gets a new run_dir. Never\n"
        "   overwrite a previous attempt's RunDoc or evidence. One executor or tester per repository at a time.\n"
        "5. **Dispatch the executor.** Build the prompt from `deskops show task <id> --root <desk_root>`: task id and\n"
        "   contract, repository, exact scope, validation, evidence, assigned run_dir/attempt and prohibitions. Tell the executor to run\n"
        f"   implementation and validation from `{desk_root}`. The executor implements one bounded task and does not\n"
        "   close it. Template artifacts and evidence stay under the assigned desk runs directory, never /tmp:\n"
        "\n"
        "```bash\n"
        f"RUN_DIR={desk_root}/runs/subagents/<run>\n"
        f"deskops runtime template role-deskops-executor --root {source_root} --out \"$RUN_DIR/scion-template\" \\\n"
        f"  --mode executor --task <task-id> --agent deskops-e-<12hex> --task-root {desk_root} --run-dir runs/subagents/<run>\n"
        f"scion start deskops-e-<12hex> \"<task prompt>\" --type deskops-executor --project {project} \\\n"
        f"  --workspace {workspace} --harness-auth {child_auth} --non-interactive \\\n"
        "  --label deskops.task_id=<helper-task-label> --label deskops.contract_sha256=<helper-contract-label> \\\n"
        "  --label deskops.role=executor --label deskops.attempt=1\n"
        f"sciontool status blocked \"waiting on deskops-e-<12hex>\"\n"
        "```\n"
        "\n"
        "   One executor per repository at a time; different repositories may run in parallel.\n"
        "   The executor itself runs `deskops advance task` on its task once its evidence is written; you do not\n"
        "   advance that transition. If it signalled `blocked` with an `advance` finding or a failed post-hook,\n"
        "   the task is back at its previous node: read the finding and the hook log it names, and decide the retry.\n"
        "6. **Test independently.** When activity=completed, verify that the executor's advance happened with\n"
        f"   `deskops show task <id> --root {desk_root}` (status and current_node changed) and inspect its handoff\n"
        "   before testing. Dispatch a\n"
        "   fresh tester with role-deskops-tester, `--mode tester`, its own `deskops-t-<12hex>` identity and a run dir\n"
        f"   ending in `-testing`. Tell it to run validation from `{desk_root}`. The tester proves the contract and\n"
        "   guardrails; it does not implement or close.\n"
        "\n"
        "```bash\n"
        f"TEST_RUN={desk_root}/runs/subagents/<run>-testing\n"
        f"deskops runtime template role-deskops-tester --root {source_root} --out \"$TEST_RUN/scion-template\" \\\n"
        f"  --mode tester --task <task-id> --agent deskops-t-<12hex> --task-root {desk_root} --run-dir runs/subagents/<run>-testing\n"
        f"scion start deskops-t-<12hex> \"<test prompt>\" --type deskops-tester --project {project} \\\n"
        f"  --workspace {workspace} --harness-auth {child_auth} --non-interactive \\\n"
        "  --label deskops.task_id=<helper-task-label> --label deskops.contract_sha256=<helper-contract-label> \\\n"
        "  --label deskops.role=tester --label deskops.attempt=1\n"
        "```\n"
        "\n"
        "7. **Close explicitly and continue.** Review the evidence and diff, then run\n"
        f"   `deskops closeout verify --task <id> --root {desk_root}` and\n"
        f"   `deskops closeout commit --task <id> --run-dir <run> --paths <scoped implementation, evidence and review paths> --root {desk_root}`.\n"
        "   Never use `git add -A` or stage unrelated work. A failed tester cannot support closeout: request one\n"
        "   bounded correction and a fresh test, preserving the failure evidence, with at most two\n"
        "   implementation/test cycles per task contract. Reconcile the phase, then reconcile ownership and select again.\n"
        f"   Stop each completed child with `scion stop <name> --project {project}`. Do not push.\n"
        "\n"
        "## Bounds and human decisions\n"
        "\n"
        "- Never rerun an accepted review with unchanged input. Bound technical retries to 2 attempts per unchanged\n"
        "  input and report the exact blocker instead of looping broadly.\n"
        "- Answer ordinary factual and implementation questions from the task and source evidence; do not\n"
        "  blanket-surface every question. Escalate only unresolved owner decisions, real ownership conflicts,\n"
        "  external credentials/permissions, or genuine human decisions.\n"
        "- Waiting for a child uses Scion activity/completion notifications (already subscribed); do not poll in a\n"
        "  loop. Only a genuine human decision uses `sciontool status ask_user \"<question>\"`.\n"
        "\n"
        "## Completion\n"
        "\n"
        "- Only after all authorized work is closed, declared evidence verified and required phase integration/commit\n"
        "  done, write the final evidence summary and call `sciontool status task_completed \"<one-line summary>\"`.\n"
        "- If externally blocked, persist the exact blocker and signal `sciontool status blocked \"<blocker>\"`.\n"
        "- Only an actual owner decision uses `ask_user`.\n"
        "\n"
        "## Never\n"
        "\n"
        "- Never implement code, edit source files or hand-edit a tracked desk document; use `deskops` / `sldb` CLIs\n"
        "  for modeled workflow mutations (`--help` first).\n"
        f"- Never write outside `{workspace}` except `runs/` evidence inside the configured desk root.\n"
        "- Never duplicate a running or completed child, create attempt 3, or overwrite prior RunDoc evidence.\n"
        "- Never decide for the owner: releases, policy, model design, anything a note marks as theirs.\n"
    )


def _render_tester_agents_md(
    role_name: str,
    harness: str,
    task_repo: str | None,
    context: dict[str, str] | None,
) -> str:
    """Independent verification instructions, intentionally separate from the executor."""
    _workspace, desk_root, source_root, project = _example_roots(task_repo, context)
    repo_line = (
        f"- Your task lives in the repository at `{desk_root}` (`{task_repo}` is descriptive only)."
        if task_repo
        else f"- Your task lives in the repository at `{desk_root}`."
    )
    return (
        f"# {role_name}: independent tester on Scion ({harness})\n"
        "\n"
        "You are an independent tester. You do not implement or fix the task; you prove whether the\n"
        "executor's handoff satisfies the task contract and its guardrails.\n"
        "\n"
        "## Tester scope\n"
        "\n"
        f"{repo_line}\n"
        "- Test one bounded task only. Do not route the board, edit implementation, alter tests, or close the task.\n"
        "- Confirm the incoming contract names the intended result, touched surfaces and guardrails to prove.\n"
        f"- Run every validation command from `{desk_root}`. `{source_root}` is the tool import source, not a task\n"
        "  write location. Persist evidence under the assigned `runs/subagents/<run>-testing/` directory.\n"
        "\n"
        "## Recover state first\n"
        "\n"
        "```bash\n"
        f"cd {desk_root}\n"
        f"deskops show board Board --root {desk_root}\n"
        f"deskops show task <task-id> --root {desk_root}\n"
        f"deskops next <task-id> --root {desk_root}\n"
        "git status --short --branch\n"
        "```\n"
        "\n"
        "## Verify\n"
        "\n"
        "- Read the executor's `result-summary.md`, `validation.log` and changed-file list before trusting a green\n"
        "  exit code.\n"
        "- Run the smallest task-specific validation first, then the negative or boundary checks the task and pills\n"
        "  imply. Report stale or missing tests instead of treating them as proof.\n"
        "- Record exact commands and genuine outputs. A failed check is a blocker for closeout, not something to fix\n"
        "  in this role.\n"
        "\n"
        "## Completion\n"
        "\n"
        "- Write `result-summary.md` with the task id, role `tester`, run id/session, validations, pass/fail,\n"
        "  guardrails proven, stale/missing tests and any follow-up.\n"
        "- Hand back to the coordinator. Do not run `deskops closeout`; the coordinator closes only after reviewing\n"
        "  your evidence and a passing independent test.\n"
        "- Say you are done with `sciontool status task_completed \"<one-line pass/fail summary>\"`: Scion wakes the\n"
        "  coordinator on that status.\n"
        f"\nProject: `{project}`. Runtime: `{harness}`.\n"
    )


def _render_specialist_agents_md(
    role_name: str,
    harness: str,
    task_repo: str | None,
    context: dict[str, str] | None,
) -> str:
    """Store-cleaning specialist: mechanical sldb repairs only, notes for the rest."""
    _workspace, desk_root, _source_root, project = _example_roots(task_repo, context)
    return (
        f"# {role_name}: sldb store specialist on Scion ({harness})\n"
        "\n"
        "You leave the desk's sldb store clean. You repair only mechanical findings and report the rest.\n"
        "\n"
        "## Scope\n"
        "\n"
        f"- Work from the desk root `{desk_root}` (`DESKOPS_DESK_ROOT`): `cd {desk_root}` first.\n"
        "- Use exactly the run_dir the coordinator wrote in your start prompt; never invent a different\n"
        "  timestamp directory. Create it if missing.\n"
        "\n"
        "## 1. Check\n"
        "\n"
        "```bash\n"
        f"cd {desk_root}\n"
        "RUN_DIR=<run_dir from the start prompt>; mkdir -p \"$RUN_DIR\"\n"
        "sldb stores check --store .sldb --format json > \"$RUN_DIR/stores-check-before.json\"\n"
        "deskops doctor --root . > \"$RUN_DIR/doctor-before.txt\"\n"
        "```\n"
        "\n"
        "## 2. Repair (only these four commands define \"mechanical\")\n"
        "\n"
        "- `sldb docs track <path>`: a Markdown file under `desk/` the check reports as unregistered.\n"
        "- `sldb docs update <path>`: a registered document whose file changed outside the CLI. It registers the\n"
        "  file as it is; you never change its text.\n"
        "- `sldb docs untrack <id>`: an indexed document whose file no longer exists.\n"
        "- `sldb stores rebuild-index --store .sldb`: the check reports a stale derived index.\n"
        "\n"
        "## 3. Everything else: leave a note, touch nothing\n"
        "\n"
        "Any finding those four commands do not fix (lost anchors included, and anything that would need you to\n"
        "change a document's text) is not touched. Send one note per finding:\n"
        "\n"
        "```bash\n"
        "deskops message send \"<finding verbatim and affected document>\" --kind unclear \\\n"
        "  --title \"store: <document id, or file path if it has no id>\" --root .\n"
        "```\n"
        "\n"
        "## 4. Re-check and report\n"
        "\n"
        "```bash\n"
        "sldb stores check --store .sldb --format json > \"$RUN_DIR/stores-check-after.json\"\n"
        "```\n"
        "\n"
        "Write `$RUN_DIR/result-summary.md` with: findings before, commands run, findings after, notes sent.\n"
        "\n"
        "## Forbidden\n"
        "\n"
        "- Editing files by hand, touching code or tests.\n"
        "- `git commit` and `git add`: changes stay uncommitted for the coordinator.\n"
        "- `deskops closeout` and `deskops advance task`.\n"
        "\n"
        "## Completion\n"
        "\n"
        "- Say you are done with `sciontool status task_completed \"<one-line summary>\"`.\n"
        f"\nProject: `{project}`. Runtime: `{harness}`.\n"
    )


def _render_agents_md(
    role_name: str,
    harness: str,
    task_repo: str | None,
    context: dict[str, str] | None,
) -> str:
    _workspace, desk_root, source_root, project = _example_roots(task_repo, context)
    repo_line = (
        f"- Your task lives in the repository `{task_repo}` at `{desk_root}` (the alias is descriptive only). Write only there."
        if task_repo
        else f"- Your task lives in the repository at `{desk_root}`. Write only there; the other repositories are context."
    )
    return (
        f"# {role_name} on Scion ({harness})\n"
        "\n"
        "You are a deskops executor running as a Scion agent. The desk, not your memory, holds the state.\n"
        "\n"
        "## Scope\n"
        "\n"
        f"{repo_line}\n"
        "- One bounded task. Do not route the board, touch other tasks, or close the task yourself.\n"
        f"- Run implementation and validation from `{desk_root}`. `{source_root}` is the tool import source, not a\n"
        "  task write location.\n"
        "- The CLIs are `deskops` and `sldb`; learn them with `--help`. Never edit a tracked desk document by hand.\n"
        "\n"
        "## Recover state first\n"
        "\n"
        "```bash\n"
        f"cd {desk_root}\n"
        f"deskops show board Board --root {desk_root}\n"
        f"deskops show task <task-id> --root {desk_root}\n"
        f"deskops next <task-id> --root {desk_root}\n"
        "git status --short --branch\n"
        "```\n"
        "\n"
        "## Evidence\n"
        "\n"
        "Use the exact run_dir assigned by the coordinator; never invent a different timestamp directory.\n"
        "Snapshot the state inside that assigned run_dir and preserve its existing RunDoc intent.\n"
        "`deskops closeout commit --run-dir` refuses a run dir without `board.txt` and `git-status.txt`:\n"
        "\n"
        "```bash\n"
        'RUN_DIR=runs/subagents/<assigned-run>; mkdir -p "$RUN_DIR"\n'
        f"deskops show board Board --root {desk_root} > \"$RUN_DIR/board.txt\"\n"
        f"deskops show task <task-id> --root {desk_root} > \"$RUN_DIR/task.txt\"\n"
        f"deskops next <task-id> --root {desk_root} > \"$RUN_DIR/next.txt\"\n"
        f"deskops graph missing --root {desk_root} > \"$RUN_DIR/graph.txt\"\n"
        f"git status --short --branch > \"$RUN_DIR/git-status.txt\"\n"
        "```\n"
        "\n"
        "- Then `validation.log` (the exact command and its exit code) and `result-summary.md`.\n"
        "- `result-summary.md` is the handoff: what you did, what you ran, what the supervisor must review.\n"
        "- Run the smallest relevant validation first.\n"
        "\n"
        "## When done\n"
        "\n"
        "- Leave scoped implementation changes uncommitted and clearly described in `result-summary.md`; the coordinator\n"
        "  stages the deliverable and evidence through `deskops closeout commit`. Do not commit or close the task yourself.\n"
        "- With the evidence written, ask to advance your task before you finish:\n"
        "\n"
        "```bash\n"
        f"deskops advance task <task-id> --root {desk_root}\n"
        "```\n"
        "\n"
        "  Run it once, right before `sciontool status task_completed`. The transition may run post-hooks the desk\n"
        "  declared (`deskops next` lists them). If `advance` is blocked or a hook fails (it exits non-zero and the task\n"
        "  stays where it was), put that finding line in `result-summary.md` and signal\n"
        "  `sciontool status blocked \"<the finding line>\"` instead of `task_completed`.\n"
        "  Advancing is the only lifecycle step you take: never close the task, commit or touch other tasks.\n"
        "- Say you are done with `sciontool status task_completed \"<one-line summary>\"`: Scion wakes the coordinator\n"
        "  on that status, not on `blocked`.\n"
        f"\nProject: `{project}`.\n"
    )


def materialize_scion_template(
    root: Path,
    role_id: str,
    *,
    harness: str | None = None,
    out_dir: Path | None = None,
    model_alias: str = DEFAULT_MODEL_ALIAS,
    task_repo: str | None = None,
    mode: str | None = None,
    context: dict[str, Any] | None = None,
    harness_auth: str | None = None,
) -> Path:
    """Write the template for ``role_id`` and return its directory.

    The runtime profile is the one matching the role's ``kind`` unless
    ``harness`` names another installed kind; ``harness`` also decides
    ``default_harness_config``. ``context`` is validated before any output.
    """
    role_path, role_doc = find_role_doc(root, role_id)
    profiles = load_runtime_profiles(root)
    kind = harness or str(role_doc.get("kind") or "")
    profile = profiles.get(kind) or profiles.get(str(role_doc.get("kind") or ""))
    if profile is None:
        raise ValueError(f"no RuntimeProfileDoc for kind '{kind}' under {root / 'desk' / 'runtimes'}")
    harness_name = pick_harness_config(kind)
    source = f"{role_path.relative_to(root).as_posix()} + desk/runtimes/{profile.get('id', kind)}.md"
    files = scion_template_files(
        role_doc,
        profile,
        harness=harness_name,
        model_alias=model_alias,
        task_repo=task_repo,
        source=source,
        mode=mode,
        context=context,
        harness_auth=harness_auth,
    )
    target = template_dir_for(root, role_doc, out_dir)
    target.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (target / name).write_text(text, encoding="utf-8")
    return target


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slug(value: str) -> str:
    return _SLUG_RE.sub("-", value.lower()).strip("-")


def record_scion_run(
    root: Path,
    *,
    task_id: str,
    role_id: str,
    kind: str,
    agent_slug: str,
    run_dir: str | None = None,
    outcome: str = "in_progress",
    summary: str = "",
) -> Path:
    """Write the in_progress intent RunDoc for one Scion dispatch.

    The RunDoc lives at ``<run_dir>/run.md`` so the evidence directory and its
    record travel together. It is written before a native Scion start, so it
    records intent, not proof of start. An existing RunDoc is never overwritten:
    attempts and their evidence are immutable, and a new attempt gets a new
    run_dir and ``-a2`` identity.
    """
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_dir = run_dir or f"runs/subagents/{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{_slug(task_id)}"
    run_id = f"run-{_slug(agent_slug)}"
    payload = {
        "id": run_id,
        "title": f"Scion agent {agent_slug} on {task_id}",
        "summary": summary or (
            f"Launch intent for `scion start {agent_slug}` from role {role_id} ({kind}); "
            "intent, not proof of start."
        ),
        "task_id": task_id,
        "role_id": role_id,
        "kind": kind,
        "run_dir": run_dir,
        "herdr_pane_id": "",
        "session_path": f"scion://agent/{agent_slug}",
        "session_sha256": "",
        "started_at": now,
        "ended_at": "" if outcome == "in_progress" else now,
        "outcome": outcome,
        "commit_sha": "",
        "tags": ["system:deskops", "runtime:scion"],
    }
    path = root / Path(run_dir) / "run.md"
    if path.exists():
        raise ValueError(
            f"RunDoc already exists at {path}: attempts and evidence are immutable; "
            "use a new run_dir and the attempt-2 identity instead of overwriting it"
        )
    doc_access.create_doc(root, path, RunDoc, payload, run_id)
    return path

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
Cold-bundle de la tarea task-deskops-dispatch-lanza-y-recoge-por-scion-al-ejecutor-y-al-tester-de-una-tarea-sin-coordinador-agent: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Un archivo de tests nuevo, test_dispatch.py en la carpeta tests, pasa con `TMPDIR=/dev/shm pytest -q` sobre ese archivo. Con el scion de prueba en el PATH y un desk desechable de `tmp_path` con roles y una tarea creados por el CLI, comprueba: (a) `dispatch start executor` ejecuta `templates sync` y `start` con el argv esperado (nombre, tipo, proyecto, workspace, etiquetas, `--config`), deja el template, el RunDoc y prompt.md; (b) lo mismo para tester con su run_dir terminado en `-testing`; (c) con un agente en phase running sale con 3 y no ejecuta start; (d) el segundo start de la misma tarea y rol usa el intento 2 y el tercero sale con 5; (e) `dispatch reap` detiene y borra por cada uno de los tres motivos, deja vivo al que sigue trabajando y sale con 4; (f) sin campo `dispatch` en la configuracion los dos subcomandos salen con 2.
- `TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py` sigue pasando.
- Los tests guardianes del CLI pasan con el grupo nuevo declarado: `pytest -q tests/test_cli_grammar.py tests/test_command_registry.py` y `pytest -q tests/test_cli.py -k help_uses_deskops_name`; los goldens de ayuda se regeneran con `pytest -n 4 tests/test_output_goldens.py -k help --update-golden` conservando solo los que cambian por el grupo nuevo.

