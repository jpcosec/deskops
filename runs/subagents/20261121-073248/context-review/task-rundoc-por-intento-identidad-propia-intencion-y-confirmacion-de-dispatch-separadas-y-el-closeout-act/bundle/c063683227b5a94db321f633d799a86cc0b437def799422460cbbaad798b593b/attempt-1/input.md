FILE:desk/tasks/task-rundoc-por-intento-identidad-propia-intencion-y-confirmacion-de-dispatch-separadas-y-el-closeout-act.md
---
sldb:
  by: agent
  at: '2026-11-16T06:01:09Z'
  authority: generated
  via: save_document_payload
id: task-rundoc-por-intento-identidad-propia-intencion-y-confirmacion-de-dispatch-separadas-y-el-closeout-act
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-002453-suggestion-piloto-scion-fase-1-brechas-del-coordinador-y-del-ejecutor-claude-en-contenedor.md
depends_on: []
pills: []
files:
- deskops/runtime/scion.py
- deskops/models/run.py
- deskops/services/closure.py
- tests/test_scion_runtime.py
- tests/test_closeout.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
- atom-scion-coordinator-progresses-authorized-work
from_drawer: desk/drawer/tasks/task-correlacionar-intentos-scion-con-rundoc-y-closeout.md
---

# RunDoc por intento: identidad propia, intencion y confirmacion de dispatch separadas y el closeout actualiza el intento

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (auditoria del 2026-10-30) y requisito D6 de Governance. deskops/runtime/scion.py:842 usa run_id = run-<agent_slug>, sin distinguir reintentos; deskops/services/closure.py no toca RunDoc; la docstring de deskops/models/run.py:9-15 dice que nada lo escribe, pero record_scion_run (scion.py:823) si lo hace. La nota del piloto scion fase 1 confirma que el coordinador despacho sin escribir el RunDoc de intencion.

## Goal

_Describe the concrete result this task must produce._

Cada intento tiene un RunDoc propio: id run-<agent_slug> en el intento 1 y run-<agent_slug>-a2 en el 2 (como el nombre del hijo en el contrato de despacho de desk/roles/deskops-supervisor.md, seccion Dispatch contract); el intento sale de la etiqueta deskops.attempt del despacho, sin contador nuevo. RunDoc gana dos campos: intent_at (cuando runtime template registra la intencion, outcome in_progress) y dispatch_confirmed_at (cuando se observa el agente en scion), mas external_ref scion://agent/<slug>. Un reintento nunca sobrescribe el anterior. closeout commit con --run-dir actualiza el RunDoc cuyo campo run_dir coincide (outcome, commit, finished_at); resolved-by no tiene run-dir y no toca RunDoc. La docstring de deskops/models/run.py describe quien escribe RunDoc, estos campos y el formato del id.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/runtime/scion.py, deskops/models/run.py, deskops/services/closure.py, tests/test_scion_runtime.py y tests/test_closeout.py. Primero se verifica en el repo scion hermano (/mnt/ssd/proyectos/SLDB_1/scion) que identidad de ejecucion expone la API (Agent.RunID/PreviousRunIDs en pkg/store/models.go); si no esta expuesta, se usa solo la identidad interna. No entra: importar conversaciones o mensajes de scion, otro broker, replicacion, UI. Precisiones del preflight 1: el id es run-<agent_slug> en el intento 1 y run-<agent_slug>-a2 en el 2, igual que el nombre del hijo en el contrato de despacho del rol deskops-supervisor (no hay intento 3). El intento sale de la etiqueta deskops.attempt del despacho, no de un contador nuevo. Si la API de scion no expone el run id, se usa solo la identidad interna y la docstring de run.py lo dice. El cierre localiza el RunDoc por su campo run_dir igual al --run-dir de closeout commit; resolved-by, que no tiene run-dir, no toca RunDoc. La docstring de run.py describe: quien escribe RunDoc (runtime template y closeout), los campos de intencion y confirmacion y el formato del id. tests/test_model_contract_snapshot.py y tests/fixtures/model_contract_hashes.json se actualizan con pytest --update-golden si el test lo admite, o editando el hash como indica el mensaje del test.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer scion.py:800-860, models/run.py y close_from_run en closure.py. 2) id por intento desde deskops.attempt. 3) Campos intent_at, dispatch_confirmed_at y external_ref. 4) closure actualiza el RunDoc del run_dir. 5) Tests: dos intentos -> dos RunDoc; el cierre del segundo actualiza solo el segundo; RunDocs viejos sin los campos nuevos siguen leyendose.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_scion_runtime.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_model_contract_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los tres casos del paso 5 pasan y el cambio de contrato de RunDoc queda registrado en el snapshot de modelos.

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


def _command_args(role_doc: dict[str, Any], profile: dict[str, Any], harness: str = "") -> list[str]:
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
    if harness == "pi":
        # pi rejects ``--tools=a,b`` (Unknown option) and takes option and value as two args.
        return list(args)
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

    command_args = _command_args(role_doc, profile, harness)
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
        + _render_python_env_section(desk_root, context)
        +
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


def _render_python_env_section(desk_root: str, context: dict[str, str] | None) -> str:
    """Startup step: the container builds its own Python 3.12 venv (the workspace .venv does not run there)."""
    sldb_pkg = (
        str(Path(context["sldb_root"]).parent) if context is not None else "<sldb checkout>"
    )
    return (
        "## Python environment (run first)\n"
        "\n"
        "The workspace `.venv` links to the host's `/usr/bin/python3.12`, which this image lacks. Build your own\n"
        "venv from the task repo's `pyproject.toml` before any test (about 30 s) and put it first on `PATH`:\n"
        "\n"
        "```bash\n"
        "export PATH=\"$HOME/.local/bin:$PATH\" TMPDIR=/tmp; unset PYTHONPATH\n"
        "uv venv /tmp/ws-venv --python 3.12\n"
        f"VIRTUAL_ENV=/tmp/ws-venv uv pip install -e \"{desk_root}[dev]\" -e {sldb_pkg}\n"
        "export VIRTUAL_ENV=/tmp/ws-venv PATH=\"/tmp/ws-venv/bin:$PATH\"\n"
        "python -m pytest -q -p no:cacheprovider <tests>\n"
        "```\n"
        "\n"
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
        + _render_python_env_section(desk_root, context)
        +
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
        "- If you end blocked or without changes, do NOT run `deskops advance task`: write the blocker in\n"
        "  `result-summary.md` and finish with `sciontool status blocked \"<reason>\"`.\n"
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

FILE:deskops/models/run.py
from pydantic import Field

from sldb import StructuredNLDoc


class RunDoc(StructuredNLDoc):
    """One supervised agent execution.

    Additive by design: this document type is defined and registered so it
    can be tracked, drift-checked, and traversed like any other desk
    artifact, but nothing writes it yet. `deskops/cli/commands/closeout.py`
    still writes `run.yaml` and `runs/subagents/index.jsonl` unchanged. The
    next step — having one manifest drive both `run.yaml` and a tracked
    `RunDoc` instead of two independently-maintained records — is tracked in
    `desk/drawer/features/feature-herdr-supervised-execution-runtime.md`.
    """

    __references__ = ["task_id", "role_id"]
    __semantics__ = {"type": ["workflow", "run"], "workspace": ["desk", "runs"]}
    __template__ = """---
# run-xxx
id: ⸢rev•id⸥
# Task identifier this run executed against
task_id: ⸢rev•task_id⸥
# Role identifier dispatched for this run
role_id: ⸢rev•role_id⸥
# Runtime binary identifier, matching RuntimeProfileDoc.kind
kind: ⸢rev•kind⸥
# Run evidence directory, relative to the project root
run_dir: ⸢rev•run_dir⸥
# Herdr pane identifier, empty if not recorded
herdr_pane_id: ⸢rev•herdr_pane_id⸥
# Session/transcript file path, relative to the project root
session_path: ⸢rev•session_path⸥
# SHA-256 digest of the session file
session_sha256: ⸢rev•session_sha256⸥
# ISO 8601 start timestamp
started_at: ⸢rev•started_at⸥
# ISO 8601 end timestamp, empty while in progress
ended_at: ⸢rev•ended_at⸥
# in_progress | success | failure | aborted
outcome: ⸢rev•outcome⸥
# Closeout commit hash, empty until closeout completes
commit_sha: ⸢rev•commit_sha⸥
# e.g. system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize what this run attempted and its result._

⸢rev•summary⸥
""".strip()

    id: str = Field(description="Stable run identifier, conventionally 'run-<slug>'.")
    title: str = Field(description="Short human-readable label for the run.")
    summary: str = Field(description="Short summary of what this run attempted and its result.")
    task_id: str = Field(description="TaskDoc identifier this run executed against.")
    role_id: str = Field(description="RoleDoc identifier that was dispatched for this run.")
    kind: str = Field(description="Runtime binary identifier used for this run, matching RuntimeProfileDoc.kind.")
    run_dir: str = Field(description="Path to the run evidence directory under runs/subagents/, relative to the project root.")
    herdr_pane_id: str = Field(
        default="", description="Herdr pane identifier the agent ran in; empty if not recorded or the pane no longer exists."
    )
    session_path: str = Field(
        default="", description="Path to the session/transcript file produced by the runtime, relative to the project root."
    )
    session_sha256: str = Field(
        default="",
        description="SHA-256 digest of the session file at the time it was last recorded, matching the closeout commit trailer.",
    )
    started_at: str = Field(description="ISO 8601 timestamp when the run started.")
    ended_at: str = Field(default="", description="ISO 8601 timestamp when the run ended; empty while the run is in progress.")
    outcome: str = Field(default="in_progress", description="Run outcome: in_progress, success, failure, or aborted.")
    commit_sha: str = Field(
        default="", description="Git commit hash of the closeout commit linked to this run; empty until closeout completes."
    )
    tags: list[str] = Field(
        default_factory=list, description="Semantic tags placed at the end, using namespaced forms such as 'system:deskops'."
    )

FILE:tests/test_scion_runtime.py
"""RoleDoc + RuntimeProfileDoc -> Scion agent template, against this repo's real desk."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.cli.main import main
from deskops.materializers.runtime_profiles import load_runtime_profiles
from deskops.models import RunDoc, TaskDoc
from deskops.runtime.scion import (
    TEMPLATE_FILES,
    find_role_doc,
    load_scion_context,
    materialize_scion_template,
    pick_harness_config,
    record_scion_run,
    scion_child_identity,
    scion_start_argv,
    scion_template_files,
    validate_scion_context,
)
from sldb.runtime.validation import extract_model_data, render_model_markdown
from sldb.store.graph.language.contract_hash import contract_hash
from sldb.store.hashing import hash_fields_with_map


@pytest.fixture(scope="module")
def executor() -> dict:
    _, role_doc = find_role_doc(ROOT, "role-deskops-executor")
    return role_doc


@pytest.fixture(scope="module")
def profiles() -> dict[str, dict]:
    return load_runtime_profiles(ROOT)


def test_harness_for_every_tracked_runtime_kind(profiles: dict[str, dict]) -> None:
    for kind in profiles:
        assert pick_harness_config(kind)
    with pytest.raises(ValueError, match="no Scion harness-config"):
        pick_harness_config("emacs")


def test_find_role_doc_accepts_id_and_name() -> None:
    by_id = find_role_doc(ROOT, "role-deskops-executor")[1]
    by_name = find_role_doc(ROOT, "deskops-executor")[1]
    assert by_id == by_name
    with pytest.raises(ValueError, match="no RoleDoc"):
        find_role_doc(ROOT, "role-nobody")


def test_claude_template_is_portable_and_loud_about_omissions(executor: dict, profiles: dict[str, dict]) -> None:
    files = scion_template_files(executor, profiles["claude"], harness="claude", source="desk/roles/x.md")
    assert set(files) == set(TEMPLATE_FILES)

    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert agent["schema_version"] == "1"
    assert agent["default_harness_config"] == "claude"
    assert agent["model"] == "medium"  # size alias, never the concrete RoleDoc model
    assert agent["auth_selectedType"] == "oauth-token"  # never left to whatever credential the Hub finds
    assert agent["agent_instructions"] == "agents.md"
    assert agent["system_prompt"] == "system-prompt.md"
    assert agent["max_turns"] and agent["max_duration"]
    assert "image" not in agent  # environment keys belong to the harness-config

    text = files["scion-agent.yaml"]
    assert "# Source: desk/roles/x.md" in text
    assert executor["model"] in text  # the concrete model is named in a comment
    assert "fallback_models" in text and "unsupported_role_fields" in text  # dropped, but said so
    assert files["system-prompt.md"].strip() == executor["body"].strip()
    assert "Write only there" in files["agents.md"]
    assert "deskops closeout" in files["agents.md"]


def test_pi_template_targets_the_pi_harness_config(executor: dict, profiles: dict[str, dict]) -> None:
    files = scion_template_files(executor, profiles["pi"], harness="pi", model_alias="small", task_repo="sldb")
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert agent["default_harness_config"] == "pi"
    assert agent["model"] == "small"
    assert "auth_selectedType" not in agent
    assert "repository `sldb`" in files["agents.md"]


def test_supervisor_role_gets_coordinator_instructions(profiles: dict[str, dict]) -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    files = scion_template_files(supervisor, profiles["claude"], harness="claude", task_repo="deskops")
    agents = files["agents.md"]
    assert "coordinator of the `deskops` desk" in agents
    assert "One executor per repository at a time" in agents
    assert "Do not push" in agents and "Never decide for the owner" in agents
    # the executor text is not in it, and an explicit mode overrides the name
    assert "You are a deskops executor" not in agents
    forced = scion_template_files(supervisor, profiles["claude"], harness="claude", mode="executor")
    assert "You are a deskops executor" in forced["agents.md"]
    with pytest.raises(ValueError, match="mode must be"):
        scion_template_files(supervisor, profiles["claude"], harness="claude", mode="boss")


def test_statuses_are_ones_sciontool_has_and_wake_the_coordinator(executor: dict, profiles: dict[str, dict]) -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    coordinator = scion_template_files(supervisor, profiles["claude"], harness="claude", task_repo="deskops")
    worker = scion_template_files(executor, profiles["claude"], harness="claude", task_repo="deskops")
    for text in (coordinator["agents.md"], worker["agents.md"]):
        statuses = set(re.findall(r"sciontool status (\w+)", text))
        assert statuses <= {"ask_user", "blocked", "task_completed"}, statuses
    assert "sciontool status task_completed" in worker["agents.md"]  # blocked would not wake the coordinator
    # an executor that ends blocked or without changes does not advance the task
    assert "sciontool status blocked" in worker["agents.md"]
    assert "do NOT run `deskops advance task`" in worker["agents.md"]

    # A coordinator idles blocked on its children; the executor's limit would kill it.
    assert yaml.safe_load(coordinator["scion-agent.yaml"])["max_duration"] == "24h"
    assert yaml.safe_load(worker["scion-agent.yaml"])["max_duration"] == "2h"


def test_the_executor_asks_to_advance_before_completing_and_the_coordinator_only_verifies(executor: dict, profiles: dict[str, dict]) -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    coordinator = scion_template_files(supervisor, profiles["claude"], harness="claude", task_repo="deskops")["agents.md"]
    worker = scion_template_files(executor, profiles["claude"], harness="claude", task_repo="deskops")["agents.md"]

    advance, done = worker.index("deskops advance task <task-id>"), worker.index('sciontool status task_completed "<one-line summary>"')
    assert advance < done
    assert "sciontool status blocked" in worker[advance:done] and "result-summary.md" in worker[advance:done]
    assert "never close the task, commit or touch other tasks" in worker

    assert "deskops advance task" in coordinator and "you do not\n   advance that transition" in coordinator
    assert "deskops show task <id>" in coordinator and "status and current_node changed" in coordinator


def test_tools_fold_into_command_args_when_the_profile_has_a_flag(profiles: dict[str, dict]) -> None:
    role = {"id": "role-x", "name": "x", "description": "d", "kind": "claude", "model": "", "tools": ["Read", "Bash"], "body": "# x"}
    agent = yaml.safe_load(scion_template_files(role, profiles["claude"], harness="claude")["scion-agent.yaml"])
    # One token per pair: Scion appends the prompt after command_args, and a variadic
    # flag (Claude's --allowedTools <tools...>) followed by a bare value would eat it.
    assert agent["command_args"] == ["--allowedTools=Read", "--allowedTools=Bash"]


def test_pi_tools_are_option_and_value_as_separate_args(profiles: dict[str, dict]) -> None:
    role = {"id": "role-x", "name": "x", "description": "d", "kind": "pi", "model": "", "tools": ["read", "grep", "bash"], "body": "# x"}
    agent = yaml.safe_load(scion_template_files(role, profiles["pi"], harness="pi")["scion-agent.yaml"])
    assert agent["command_args"] == ["--tools", "read,grep,bash"]


def test_bad_alias_and_bad_harness_are_refused(executor: dict, profiles: dict[str, dict]) -> None:
    with pytest.raises(ValueError, match="model alias"):
        scion_template_files(executor, profiles["claude"], harness="claude", model_alias="huge")
    with pytest.raises(ValueError, match="unknown Scion harness-config"):
        scion_template_files(executor, profiles["claude"], harness="emacs")


def test_materialize_writes_the_three_files(tmp_path: Path) -> None:
    target = materialize_scion_template(ROOT, "deskops-executor", harness="claude", out_dir=tmp_path / "t")
    assert target == tmp_path / "t"
    assert sorted(p.name for p in target.iterdir()) == sorted(TEMPLATE_FILES)
    assert "Source: desk/roles/deskops-executor.md + desk/runtimes/runtime-claude.md" in (target / "scion-agent.yaml").read_text()


def test_cli_runtime_template(tmp_path: Path, capsys) -> None:
    code = main(["runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude", "--out", str(tmp_path / "t")])
    out = capsys.readouterr().out
    assert code == 0, out
    assert "Scion template:" in out and "scion start" in out
    assert (tmp_path / "t" / "scion-agent.yaml").exists()


def test_cli_task_root_puts_the_rundoc_next_to_the_task(tmp_path: Path, capsys) -> None:
    task_root = tmp_path / "other-repo"
    task_root.mkdir()
    code = main([
        "runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude",
        "--out", str(tmp_path / "t"), "--task", "task-x", "--agent", "agent-x", "--task-root", str(task_root),
    ])
    out = capsys.readouterr().out
    assert code == 0, out
    runs = list((task_root / "runs" / "subagents").glob("*-task-x/run.md"))
    assert len(runs) == 1, out

    # An agent that already made its own evidence dir: the RunDoc points there.
    code = main([
        "runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude",
        "--out", str(tmp_path / "t"), "--task", "task-x", "--agent", "agent-y", "--task-root", str(task_root),
        "--run-dir", "runs/subagents/20261029-000000-task-x",
    ])
    assert code == 0, capsys.readouterr().out
    doc = extract_model_data(RunDoc, (task_root / "runs/subagents/20261029-000000-task-x/run.md").read_text(encoding="utf-8"))
    assert doc["run_dir"] == "runs/subagents/20261029-000000-task-x" and doc["id"] == "run-agent-y"
    assert not list((ROOT / "runs" / "subagents").glob("*-task-x"))  # nothing written into the roles' repo
    assert extract_model_data(RunDoc, runs[0].read_text(encoding="utf-8"))["id"] == "run-agent-x"


def test_cli_task_without_agent_is_an_error(tmp_path: Path, capsys) -> None:
    code = main(["runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--out", str(tmp_path / "t"), "--task", "task-x"])
    captured = capsys.readouterr()
    assert code != 0
    assert "--task and --agent go together" in captured.out + captured.err


def test_record_scion_run_writes_a_rundoc_that_roundtrips(tmp_path: Path) -> None:
    path = record_scion_run(
        tmp_path,
        task_id="task-close-serve",
        role_id="role-deskops-executor",
        kind="claude",
        agent_slug="sldb-close-serve",
        run_dir="runs/subagents/20261029-000000-task-close-serve",
    )
    assert path == tmp_path / "runs/subagents/20261029-000000-task-close-serve/run.md"
    data = extract_model_data(RunDoc, path.read_text(encoding="utf-8"))
    assert data["id"] == "run-sldb-close-serve"
    assert data["task_id"] == "task-close-serve"
    assert data["session_path"] == "scion://agent/sldb-close-serve"
    assert data["outcome"] == "in_progress" and data["ended_at"] == ""
    assert "intent, not proof of start" in data["summary"]
    assert data["tags"] == ["system:deskops", "runtime:scion"]


def test_record_scion_run_never_overwrites_a_previous_attempt(tmp_path: Path) -> None:
    run_dir = "runs/subagents/20261029-000000-task-close-serve"
    record_scion_run(
        tmp_path,
        task_id="task-close-serve",
        role_id="role-deskops-executor",
        kind="claude",
        agent_slug="deskops-e-abc123abc123",
        run_dir=run_dir,
    )
    original = (tmp_path / run_dir / "run.md").read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="immutable"):
        record_scion_run(
            tmp_path,
            task_id="task-close-serve",
            role_id="role-deskops-executor",
            kind="claude",
            agent_slug="deskops-e-abc123abc123-a2",
            run_dir=run_dir,
        )
    assert (tmp_path / run_dir / "run.md").read_text(encoding="utf-8") == original


def _task_payload(**updates) -> dict:
    payload = {
        "id": "task-contract-identity",
        "title": "Identity test task",
        "status": "draft",
        "summary": "",
        "tags": ["workspace:desk", "artifact:task"],
        "current_node": "ritual-execution",
        "history": [],
        "references": ["tests/test_scion_runtime.py"],
        "depends_on": [],
        "pills": [],
        "files": ["deskops/runtime/scion.py"],
        "task_type": "task.code",
        "inherits_from": [],
        "inherit_acceptance_context": False,
        "atoms": [],
        "why": "Test why.",
        "goal": "Test goal.",
        "scope": "Test scope.",
        "implementation_path": "Test implementation.",
        "validation": ["pytest tests/test_scion_runtime.py"],
        "done_when": "The test passes.",
    }
    payload.update(updates)
    return payload


def _write_task(tmp_path: Path, name: str, **updates) -> Path:
    path = tmp_path / f"{name}.md"
    path.write_text(render_model_markdown(TaskDoc, _task_payload(**updates)) + "\n", encoding="utf-8")
    return path


def test_identity_uses_the_canonical_sldb_contract_digest(tmp_path: Path) -> None:
    path = _write_task(tmp_path, "task")
    markdown = path.read_text(encoding="utf-8")
    _, fields = hash_fields_with_map(TaskDoc, markdown)
    expected_contract = contract_hash(TaskDoc, fields)
    expected_name = "deskops-e-" + hashlib.sha256(
        f"task-contract-identity\0{expected_contract}\0executor".encode("utf-8")
    ).hexdigest()[:12]

    identity = scion_child_identity(path, "executor")
    assert identity["contract_sha256"] == expected_contract
    assert identity["name"] == expected_name
    assert identity["labels"] == {
        "deskops.task_id": "task-contract-identity",
        "deskops.contract_sha256": expected_contract[:63],
        "deskops.role": "executor",
        "deskops.attempt": "1",
    }
    assert scion_child_identity(path, "tester")["name"].startswith("deskops-t-")

    attempt_2 = scion_child_identity(path, "executor", attempt=2)
    assert attempt_2["name"] == expected_name + "-a2"
    assert attempt_2["labels"]["deskops.attempt"] == "2"
    for bad in (0, 3, True):
        with pytest.raises(ValueError, match="attempt must be 1 or 2"):
            scion_child_identity(path, "executor", attempt=bad)
    with pytest.raises(ValueError, match="role must be"):
        scion_child_identity(path, "coordinator")


def test_identity_ignores_status_history_and_references_but_moves_with_contract(tmp_path: Path) -> None:
    entry = scion_child_identity(_write_task(tmp_path, "entry"), "executor")
    active = scion_child_identity(
        _write_task(
            tmp_path,
            "active",
            status="active",
            current_node="ritual-testing",
            history=["task_activates"],
            references=["other.md"],
            summary="Different summary",
            tags=["workspace:desk", "artifact:task", "state:changed"],
        ),
        "executor",
    )
    finished = scion_child_identity(
        _write_task(
            tmp_path,
            "finished",
            status="closed",
            current_node="complete",
            history=["task_activates", "task_hands_to_closeout", "task_completes"],
            references=[],
        ),
        "executor",
    )
    assert entry["name"] == active["name"] == finished["name"]
    assert entry["contract_sha256"] == active["contract_sha256"] == finished["contract_sha256"]

    changed_goal = scion_child_identity(_write_task(tmp_path, "goal", goal="A changed goal."), "executor")
    changed_scope = scion_child_identity(_write_task(tmp_path, "scope", scope="A changed scope."), "executor")
    assert changed_goal["name"] != entry["name"]
    assert changed_scope["contract_sha256"] != entry["contract_sha256"]


def test_start_argv_carries_explicit_project_workspace_auth_and_labels(tmp_path: Path) -> None:
    identity = scion_child_identity(_write_task(tmp_path, "task"), "tester")
    argv = scion_start_argv(
        identity,
        prompt="Verify the contract.",
        project="sldb-1",
        workspace="/workspace",
        template="deskops-tester",
    )
    assert argv[:4] == ["scion", "start", identity["name"], "Verify the contract."]
    assert "--type" in argv and argv[argv.index("--type") + 1] == "deskops-tester"
    assert "--project" in argv and argv[argv.index("--project") + 1] == "sldb-1"
    assert "--workspace" in argv and argv[argv.index("--workspace") + 1] == "/workspace"
    assert "--harness-auth" in argv and argv[argv.index("--harness-auth") + 1] == "oauth-token"
    assert "--non-interactive" in argv
    labels = {argv[index + 1].split("=", 1)[0]: argv[index + 1].split("=", 1)[1] for index, item in enumerate(argv) if item == "--label"}
    assert labels == identity["labels"]


def _context(tmp_path: Path) -> tuple[dict, dict[str, Path]]:
    workspace = tmp_path / "workspace"
    desk_root = workspace / "repo"
    source_root = workspace / "source"
    sldb_root = workspace / "sldb" / "src"
    for path in (desk_root / "desk", source_root / "deskops", sldb_root / "sldb"):
        path.mkdir(parents=True)
    context = {
        "project": "sldb-1",
        "workspace_root": str(workspace),
        "desk_root": str(desk_root),
        "source_root": str(source_root),
        "sldb_root": str(sldb_root),
    }
    return context, {
        "workspace": workspace,
        "desk": desk_root,
        "source": source_root,
        "sldb": sldb_root,
    }


def test_context_emits_environment_volume_and_concrete_examples(tmp_path: Path) -> None:
    context, paths = _context(tmp_path)
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    files = scion_template_files(
        supervisor, load_runtime_profiles(ROOT)["claude"], harness="claude", mode="coordinator", context=context
    )
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert agent["env"] == {
        "DESKOPS_DESK_ROOT": str(paths["desk"]),
        "DESKOPS_SOURCE_ROOT": str(paths["source"]),
        "DESKOPS_SLDB_SOURCE_ROOT": str(paths["sldb"]),
        "DESKOPS_WORKSPACE_ROOT": str(paths["workspace"]),
        "DESKOPS_SCION_PROJECT": "sldb-1",
        "PYTHONPATH": f"{paths['source']}:{paths['sldb']}",
    }
    assert agent["volumes"] == [{"source": str(paths["workspace"]), "target": str(paths["workspace"])}]
    agents = files["agents.md"]
    for fragment in (
        f"--root {paths['desk']}",
        f"--project sldb-1",
        f"--workspace {paths['workspace']}",
        "--type deskops-executor",
        "--type deskops-tester",
        "--harness-auth oauth-token",
        "--non-interactive",
        "--mode tester",
        "scion_child_identity(task_path, role, attempt)",
    ):
        assert fragment in agents


def test_omitted_context_keeps_the_template_without_env_or_volumes() -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    files = scion_template_files(supervisor, load_runtime_profiles(ROOT)["claude"], harness="claude")
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert "env" not in agent and "volumes" not in agent
    assert "coordinator of the `<repo>` desk" in files["agents.md"]


def test_context_rejects_missing_unknown_relative_and_out_of_workspace_paths(tmp_path: Path) -> None:
    context, paths = _context(tmp_path)
    assert validate_scion_context(context)["project"] == "sldb-1"

    with pytest.raises(ValueError, match="missing required key"):
        validate_scion_context({key: value for key, value in context.items() if key != "sldb_root"})
    with pytest.raises(ValueError, match="unknown key"):
        validate_scion_context({**context, "secret": "nope"})
    with pytest.raises(ValueError, match="absolute path"):
        validate_scion_context({**context, "desk_root": "repo"})
    with pytest.raises(ValueError, match="inside workspace_root"):
        validate_scion_context({**context, "desk_root": str(tmp_path / "outside")})
    with pytest.raises(ValueError, match="slug or UUID"):
        validate_scion_context({**context, "project": str(paths["workspace"])})
    with pytest.raises(ValueError, match="containing desk/"):
        validate_scion_context({**context, "desk_root": str(paths["workspace"])})
    with pytest.raises(ValueError, match="containing the deskops package"):
        validate_scion_context({**context, "source_root": str(paths["workspace"])})
    with pytest.raises(ValueError, match="sldb src directory"):
        validate_scion_context({**context, "sldb_root": str(paths["source"])})


def test_context_container_keys_emit_limits_shared_paths_and_env(tmp_path: Path) -> None:
    context, paths = _context(tmp_path)
    shared = tmp_path / "shm"
    shared.mkdir()
    context.update(
        memory_limit="6Gi",
        cpu_limit="4",
        shared_paths=[str(shared), str(shared)],
        env={"TMPDIR": str(shared)},
    )
    _, executor_role = find_role_doc(ROOT, "role-deskops-executor")
    files = scion_template_files(
        executor_role, load_runtime_profiles(ROOT)["claude"], harness="claude", mode="executor", context=context
    )
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert agent["resources"] == {"limits": {"cpu": "4", "memory": "6Gi"}}
    assert agent["volumes"] == [
        {"source": str(paths["workspace"]), "target": str(paths["workspace"])},
        {"source": str(shared), "target": str(shared)},
    ]
    assert agent["env"]["TMPDIR"] == str(shared)
    assert agent["env"]["DESKOPS_SCION_PROJECT"] == "sldb-1"


def test_context_without_container_keys_has_no_resources(tmp_path: Path) -> None:
    context, _ = _context(tmp_path)
    _, executor_role = find_role_doc(ROOT, "role-deskops-executor")
    files = scion_template_files(
        executor_role, load_runtime_profiles(ROOT)["claude"], harness="claude", mode="executor", context=context
    )
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert "resources" not in agent
    assert len(agent["volumes"]) == 1 and "TMPDIR" not in agent["env"]


def test_harness_auth_selects_the_template_auth_type(tmp_path: Path) -> None:
    _, executor_role = find_role_doc(ROOT, "role-deskops-executor")
    profile = load_runtime_profiles(ROOT)["claude"]
    default = yaml.safe_load(scion_template_files(executor_role, profile, harness="claude")["scion-agent.yaml"])
    assert default["auth_selectedType"] == "oauth-token"
    chosen = yaml.safe_load(
        scion_template_files(executor_role, profile, harness="claude", harness_auth="auth-file")["scion-agent.yaml"]
    )
    assert chosen["auth_selectedType"] == "auth-file"
    with pytest.raises(ValueError, match="harness auth"):
        scion_template_files(executor_role, profile, harness="claude", harness_auth="password")

    out_dir = tmp_path / "tpl"
    assert main(
        ["runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude",
         "--out", str(out_dir), "--harness-auth", "auth-file"]
    ) == 0
    assert yaml.safe_load((out_dir / "scion-agent.yaml").read_text(encoding="utf-8"))["auth_selectedType"] == "auth-file"


def test_start_auth_follows_the_template_never_a_fixed_api_key(tmp_path: Path) -> None:
    identity = scion_child_identity(_write_task(tmp_path, "task"), "executor")
    common = dict(prompt="Do the task.", project="sldb-1", workspace="/workspace", template="deskops-executor")
    chosen = scion_start_argv(identity, **common, harness_auth="auth-file")
    assert chosen[chosen.index("--harness-auth") + 1] == "auth-file"
    assert "--harness-auth" not in scion_start_argv(identity, **common, harness_auth=None)
    with pytest.raises(ValueError, match="harness auth"):
        scion_start_argv(identity, **common, harness_auth="password")

    context, _ = _context(tmp_path)
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    profile = load_runtime_profiles(ROOT)["claude"]
    for auth, expected in ((None, "oauth-token"), ("auth-file", "auth-file")):
        agents = scion_template_files(
            supervisor, profile, harness="claude", mode="coordinator", context=context, harness_auth=auth
        )["agents.md"]
        assert agents.count(f"--harness-auth {expected} --non-interactive") == 2
        assert "--harness-auth api-key" not in agents

    out_dir = tmp_path / "coordinator"
    assert main(
        ["runtime", "template", "role-deskops-supervisor", "--root", str(ROOT), "--harness", "claude",
         "--mode", "coordinator", "--out", str(out_dir), "--harness-auth", "auth-file"]
    ) == 0
    written = (out_dir / "agents.md").read_text(encoding="utf-8")
    assert written.count("--harness-auth auth-file") == 2 and "api-key" not in written
    assert yaml.safe_load((out_dir / "scion-agent.yaml").read_text(encoding="utf-8"))["auth_selectedType"] == "auth-file"


def test_context_rejects_bad_container_keys(tmp_path: Path) -> None:
    context, paths = _context(tmp_path)
    with pytest.raises(ValueError, match="memory_limit"):
        validate_scion_context({**context, "memory_limit": "lots"})
    with pytest.raises(ValueError, match="cpu_limit"):
        validate_scion_context({**context, "cpu_limit": "0"})
    with pytest.raises(ValueError, match="absolute path"):
        validate_scion_context({**context, "shared_paths": ["shm"]})
    with pytest.raises(ValueError, match="does not exist"):
        validate_scion_context({**context, "shared_paths": [str(tmp_path / "missing")]})
    with pytest.raises(ValueError, match="must not repeat workspace_root"):
        validate_scion_context({**context, "shared_paths": [str(paths["workspace"])]})
    with pytest.raises(ValueError, match="must not redefine PYTHONPATH"):
        validate_scion_context({**context, "env": {"PYTHONPATH": "/x"}})
    with pytest.raises(ValueError, match="valid variable name"):
        validate_scion_context({**context, "env": {"BAD-NAME": "x"}})
    with pytest.raises(ValueError, match="must be a string"):
        validate_scion_context({**context, "env": {"TMPDIR": 3}})


def test_load_context_validates_json_and_cli_writes_nothing_on_failure(tmp_path: Path, capsys) -> None:
    context, _ = _context(tmp_path)
    valid = tmp_path / "context.json"
    valid.write_text(json.dumps(context), encoding="utf-8")
    assert load_scion_context(valid)["desk_root"] == validate_scion_context(context)["desk_root"]

    invalid = tmp_path / "invalid.json"
    invalid.write_text(json.dumps({key: value for key, value in context.items() if key != "project"}), encoding="utf-8")
    out_dir = tmp_path / "out"
    code = main([
        "runtime", "template", "role-deskops-executor", "--root", str(ROOT),
        "--harness", "claude", "--out", str(out_dir), "--context-file", str(invalid),
    ])
    captured = capsys.readouterr()
    assert code != 0
    assert "missing required key" in captured.out + captured.err
    assert not out_dir.exists()


def test_tester_mode_is_autodetected_and_explicit_mode_wins() -> None:
    profiles = load_runtime_profiles(ROOT)
    _, tester = find_role_doc(ROOT, "role-deskops-tester")
    auto = scion_template_files(tester, profiles["claude"], harness="claude", task_repo="deskops")
    assert "independent tester" in auto["agents.md"]
    assert "## Tester scope" in auto["agents.md"]
    assert "## Completion" in auto["agents.md"]
    assert "You are a deskops executor" not in auto["agents.md"]
    assert "Do not run `deskops closeout`" in auto["agents.md"]

    _, executor = find_role_doc(ROOT, "role-deskops-executor")
    forced = scion_template_files(executor, profiles["claude"], harness="claude", mode="tester")
    assert "independent tester" in forced["agents.md"]
    explicit = scion_template_files(tester, profiles["claude"], harness="claude", mode="executor")
    assert "You are a deskops executor" in explicit["agents.md"]

    id_tester = {"id": "role-x-tester", "name": "custom reviewer", "description": "d", "kind": "claude", "body": "# t"}
    assert "independent tester" in scion_template_files(id_tester, profiles["claude"], harness="claude")["agents.md"]
    not_tester = {"id": "role-x", "name": "tester", "description": "d", "kind": "claude", "body": "# t"}
    assert "You are a deskops executor" in scion_template_files(not_tester, profiles["claude"], harness="claude")["agents.md"]

    id_coordinator = {"id": "role-x-coordinator", "name": "custom lead", "description": "d", "kind": "claude", "body": "# t"}
    coordinator = scion_template_files(id_coordinator, profiles["claude"], harness="claude")
    assert "coordinator of the" in coordinator["agents.md"]
    explicit_executor = scion_template_files(id_coordinator, profiles["claude"], harness="claude", mode="executor")
    assert "You are a deskops executor" in explicit_executor["agents.md"]


def _normalized(text: str) -> str:
    return " ".join(text.split())


def test_coordinator_reconciles_activity_own_lanes_and_reviews_before_dispatch() -> None:
    profiles = load_runtime_profiles(ROOT)
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    agents = _normalized(
        scion_template_files(supervisor, profiles["claude"], harness="claude", task_repo="deskops")["agents.md"]
    )
    assert "Never answer an executor's or tester's question" not in agents
    for fragment in (
        "activity=completed with phase=running means the child completed",
        "inspect activity=completed first and use phase only as fallback",
        "Reconcile your OWN completed or stopped lane",
        "must not skip your own task",
        "If its preflight or bundle receipt is missing",
        "routine coordinator work, not a human blocker",
        "do not blanket-surface every question",
        "closeout verify --task <id>",
        "--paths <scoped implementation, evidence and review paths>",
        "Never use `git add -A`",
        "Only an actual owner decision uses `ask_user`",
        "sciontool status task_completed",
        "Do not push.",
    ):
        assert fragment in agents, fragment
    assert "/tmp/scion" not in agents


def test_all_three_modes_receive_the_actual_context_roots(tmp_path: Path) -> None:
    context, paths = _context(tmp_path)
    profiles = load_runtime_profiles(ROOT)
    roles = {
        "role-deskops-executor": "executor",
        "role-deskops-tester": "tester",
        "role-deskops-supervisor": "coordinator",
    }
    for role_id, mode in roles.items():
        _, role = find_role_doc(ROOT, role_id)
        files = scion_template_files(role, profiles["claude"], harness="claude", context=context)
        agents = files["agents.md"]
        assert str(paths["desk"]) in agents, mode
        assert str(paths["source"]) in agents, mode
        assert f"cd {paths['desk']}" in agents, mode
        assert "/tmp/scion" not in agents, mode
        agent = yaml.safe_load(files["scion-agent.yaml"])
        assert agent["env"]["DESKOPS_DESK_ROOT"] == str(paths["desk"]), mode


def test_cli_tester_mode_and_context_file_are_available(tmp_path: Path, capsys) -> None:
    context, paths = _context(tmp_path)
    context_file = tmp_path / "context.json"
    context_file.write_text(json.dumps(context), encoding="utf-8")
    out_dir = tmp_path / "tester-template"
    code = main([
        "runtime", "template", "role-deskops-tester", "--root", str(ROOT),
        "--harness", "claude", "--out", str(out_dir), "--context-file", str(context_file),
    ])
    out = capsys.readouterr().out
    assert code == 0, out
    assert "independent tester" in (out_dir / "agents.md").read_text(encoding="utf-8")
    agent = yaml.safe_load((out_dir / "scion-agent.yaml").read_text(encoding="utf-8"))
    assert agent["env"]["DESKOPS_DESK_ROOT"] == str(paths["desk"])


def test_executor_preserves_assigned_run_and_coordinator_commit_boundary(executor, profiles) -> None:
    agents = scion_template_files(executor, profiles["pi"], harness="pi", task_repo="example")["agents.md"]
    assert "Use the exact run_dir assigned by the coordinator" in agents
    assert "preserve its existing RunDoc intent" in agents
    assert "$(date" not in agents
    assert "graph.txt" in agents
    assert "Do not commit or close the task yourself" in agents


def test_omitted_context_keeps_legacy_tool_root_separate_from_task_repo(profiles) -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    files = scion_template_files(supervisor, profiles["pi"], harness="pi", task_repo="example")
    assert "cd /workspace/example" in files["agents.md"]
    assert "--root /workspace/deskops" in files["agents.md"]
    assert "env:" not in files["scion-agent.yaml"]


@pytest.mark.parametrize("task_id", ["task-" + "a" * 58, "task-" + "b" * 59, "task-construcción"])
def test_native_labels_fit_scion_without_changing_canonical_identity(tmp_path, task_id) -> None:
    path = _write_task(tmp_path, "native-labels", id=task_id)
    identity = scion_child_identity(path, "executor")
    labels = identity["labels"]
    assert identity["task_id"] == task_id
    assert len(identity["contract_sha256"]) == 64
    assert labels["deskops.contract_sha256"] == identity["contract_sha256"][:63]
    assert len(labels) <= 16
    assert all(len(k) <= 63 and len(v) <= 63 for k, v in labels.items())
    assert all(all(0x20 <= ord(c) <= 0x7E for c in key + value) for key, value in labels.items())
    if len(task_id) <= 63 and task_id.isascii():
        assert labels["deskops.task_id"] == task_id
    else:
        assert labels["deskops.task_id"] == "t-" + hashlib.sha256(task_id.encode()).hexdigest()[:61]
    expected = hashlib.sha256(f"{task_id}\0{identity['contract_sha256']}\0executor".encode()).hexdigest()[:12]
    assert identity["name"] == "deskops-e-" + expected


def test_specialist_mode_writes_the_three_files_with_the_repair_contract(tmp_path: Path, capsys) -> None:
    out_dir = tmp_path / "t"
    code = main([
        "runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude",
        "--mode", "specialist", "--out", str(out_dir),
    ])
    assert code == 0, capsys.readouterr().out
    assert sorted(p.name for p in out_dir.iterdir()) == sorted(TEMPLATE_FILES)
    agents = (out_dir / "agents.md").read_text(encoding="utf-8")
    for needle in (
        "sldb stores check", "deskops doctor", "sldb docs track", "sldb docs update",
        "sldb docs untrack", "sldb stores rebuild-index", "deskops message send",
    ):
        assert needle in agents
    forbidden = agents.split("## Forbidden", 1)[1].split("## Completion", 1)[0]
    assert "deskops closeout" in forbidden and "deskops advance task" in forbidden
    assert "You are a deskops executor" not in agents


def test_specialist_role_name_resolves_the_mode_and_unknown_mode_still_fails() -> None:
    profiles = load_runtime_profiles(ROOT)
    role = {"id": "role-x", "name": "x-specialist", "description": "d", "kind": "claude", "body": "# s"}
    files = scion_template_files(role, profiles["claude"], harness="claude")
    assert "sldb store specialist" in files["agents.md"]
    by_id = {"id": "role-x-specialist", "name": "x", "description": "d", "kind": "claude", "body": "# s"}
    assert "sldb store specialist" in scion_template_files(by_id, profiles["claude"], harness="claude")["agents.md"]
    with pytest.raises(ValueError, match="mode must be"):
        scion_template_files(role, profiles["claude"], harness="claude", mode="bogus")


def test_specialist_identity_uses_the_s_prefix(tmp_path: Path) -> None:
    identity = scion_child_identity(_write_task(tmp_path, "task"), "specialist")
    assert re.fullmatch(r"deskops-s-[0-9a-f]{12}", identity["name"])
    assert identity["role"] == "specialist"


@pytest.mark.parametrize("mode", ["executor", "tester"])
def test_executor_and_tester_agents_md_build_their_own_py312_venv(
    executor: dict, profiles: dict[str, dict], mode: str, tmp_path: Path
) -> None:
    for d in ("desk/desk", "desk/deskops", "sldb/src/sldb"):
        (tmp_path / d).mkdir(parents=True)
    ws = str(tmp_path)
    ctx = {
        "desk_root": f"{ws}/desk",
        "source_root": f"{ws}/desk",
        "sldb_root": f"{ws}/sldb/src",
        "workspace_root": ws,
        "project": "p",
    }
    files = scion_template_files(executor, profiles["claude"], harness="claude", mode=mode, context=ctx)
    text = files["agents.md"]
    assert "uv venv /tmp/ws-venv --python 3.12" in text
    assert f'uv pip install -e "{ws}/desk[dev]" -e {ws}/sldb' in text
    assert 'PATH="/tmp/ws-venv/bin:$PATH"' in text and "unset PYTHONPATH" in text
    assert text.index("Python environment") < text.index("Recover state first")

FILE:tests/test_closeout.py
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.cli.commands.closeout import CloseoutCLI
from deskops.cli.main import main


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _make_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    (root / "seed.txt").write_text("seed\n", encoding="utf-8")
    (root / ".gitignore").write_text(".deskops.log\n", encoding="utf-8")
    _git(root, "add", "seed.txt", ".gitignore")
    _git(root, "commit", "-q", "-m", "seed")
    return root


def _make_run_dir(root: Path, name: str = "20260729-120000-task-x") -> Path:
    run_dir = root / "runs" / "subagents" / name
    run_dir.mkdir(parents=True)
    for fname in ["board.txt", "task.txt", "git-status.txt", "result-summary.md"]:
        (run_dir / fname).write_text(f"{fname}\n", encoding="utf-8")
    return run_dir


def _args(root: Path, **overrides) -> SimpleNamespace:
    base = {
        "closeout_command": "commit",
        "root": str(root),
        "run_dir": "runs/subagents/20260729-120000-task-x",
        "task": "task-x",
        "message": None,
        "paths": None,
        "run_id": None,
        "session": None,
    }
    base.update(overrides)
    return SimpleNamespace(**base)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_atom(root: Path, atom_id: str = "atom-evidence") -> None:
    _write(
        root / "desk" / "atoms" / f"{atom_id}.md",
        f"""---
id: {atom_id}
title: Evidence Atom
five_wh_one_plus: what
tags: []
provenance: null
---

# Evidence Atom

## Answer

Closeout evidence.
""",
    )


def _write_task(root: Path, references: list[str], files: list[str], *, task_id: str = "task-x") -> None:
    _write(
        root / "desk" / "tasks" / f"{task_id}.md",
        f"""---
id: {task_id}
status: active
current_node: ritual-testing
history:
- task_activates
references:
{yaml.safe_dump(references, sort_keys=False).rstrip()}
depends_on: []
pills: []
files:
{yaml.safe_dump(files, sort_keys=False).rstrip()}
checklists: []
tags: []
---

# Task X

## Rationale

Not provided.

## Goal

Verify closeout.

## Scope

Stay scoped.

## Implementation Path

Implement verify.

## Validation

- pytest

## Done When

Verified.
""",
    )


def test_closeout_commit_links_commit_to_run(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    run_dir = _make_run_dir(root)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    session = tmp_path / "session.jsonl"
    session.write_text('{"type":"session"}\n', encoding="utf-8")

    rc = CloseoutCLI().run(
        _args(
            root,
            paths=["feature.py"],
            run_id="6046eaef",
            session=str(session),
        )
    )

    assert rc == 0
    message = _git(root, "log", "-1", "--format=%B")
    assert "closeout: task-x" in message
    assert "Task-Id: task-x" in message
    assert "Run-Dir: runs/subagents/20260729-120000-task-x" in message
    assert "Run-Id: 6046eaef" in message
    assert "Session-Sha256:" in message

    commit = _git(root, "rev-parse", "HEAD")
    index = (root / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").strip()
    entry = json.loads(index.splitlines()[-1])
    assert entry["commit"] is None
    assert entry["run_id"] == "6046eaef"
    assert entry["task_id"] == "task-x"
    assert _git(root, "log", "-1", "--format=%H", "--grep", "Task-Id: task-x") == commit

    manifest = yaml.safe_load((run_dir / "run.yaml").read_text(encoding="utf-8"))
    assert manifest["run_id"] == "6046eaef"
    assert manifest["session_sha256"] == entry["session_sha256"]

    committed_files = _git(root, "show", "--name-only", "--format=", "HEAD").split()
    assert "feature.py" in committed_files
    assert "runs/subagents/20260729-120000-task-x/run.yaml" in committed_files


def test_closeout_commit_requires_evidence(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    run_dir = root / "runs" / "subagents" / "20260729-120000-task-x"
    run_dir.mkdir(parents=True)

    rc = CloseoutCLI().run(_args(root, paths=["feature.py"]))

    assert rc == 1


def test_closeout_commit_rejects_run_dir_outside_surface(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    elsewhere = root / "tmp" / "fake-run"
    elsewhere.mkdir(parents=True)
    for fname in ["board.txt", "task.txt", "git-status.txt", "result-summary.md"]:
        (elsewhere / fname).write_text("x\n", encoding="utf-8")

    rc = CloseoutCLI().run(_args(root, run_dir="tmp/fake-run", paths=["feature.py"]))

    assert rc == 1


def test_closeout_commit_uses_staged_index_without_paths(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    _make_run_dir(root)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    _git(root, "add", "feature.py")

    rc = CloseoutCLI().run(_args(root))

    assert rc == 0
    assert "closeout: task-x" in _git(root, "log", "-1", "--format=%B")


def _closeout_main(root: Path, *argv: str) -> int:
    return main(["closeout", "commit", "--root", str(root), "--task", "task-x", *argv])


def test_closeout_commit_no_run_makes_a_manual_commit(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _make_repo(tmp_path)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")

    rc = _closeout_main(root, "--no-run", "--reason", "Fixed by the supervisor; no subagent ran", "--paths", "feature.py")

    assert rc == 0, capsys.readouterr().out
    message = _git(root, "log", "-1", "--format=%B")
    assert message.splitlines()[0] == "closeout: task-x"
    assert "Task-Id: task-x" in message
    assert "Closeout-Mode: manual" in message
    assert "Closeout-Reason: Fixed by the supervisor; no subagent ran" in message
    assert "Run-Dir:" not in message
    trailers = _git(root, "log", "-1", "--format=%(trailers:key=Closeout-Mode,valueonly)")
    assert trailers == "manual", "Closeout-Mode must parse as a git trailer"

    commit = _git(root, "rev-parse", "HEAD")
    entry = json.loads((root / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert entry == {
        "task_id": "task-x",
        "run_id": None,
        "run_dir": None,
        "commit": None,
        "session_sha256": None,
        "mode": "manual",
    }
    assert _git(root, "log", "-1", "--format=%H", "--grep", "Task-Id: task-x") == commit
    assert _git(root, "show", "--name-only", "--format=", "HEAD").split() == [
        "feature.py",
        "runs/subagents/index.jsonl",
    ]


@pytest.mark.parametrize("reason", [None, "", "   "])
def test_closeout_commit_no_run_requires_a_reason(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], reason: str | None
) -> None:
    root = _make_repo(tmp_path)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    head = _git(root, "rev-parse", "HEAD")

    extra = [] if reason is None else ["--reason", reason]
    rc = _closeout_main(root, "--no-run", *extra, "--paths", "feature.py")

    assert rc == 1
    assert "--no-run needs a non-empty --reason" in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head
    assert not (root / "runs" / "subagents" / "index.jsonl").exists()


def test_closeout_commit_rejects_run_dir_and_no_run_together(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _make_run_dir(root)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    head = _git(root, "rev-parse", "HEAD")

    rc = _closeout_main(
        root, "--run-dir", "runs/subagents/20260729-120000-task-x",
        "--no-run", "--reason", "r", "--paths", "feature.py",
    )
    assert rc == 2
    assert "argument --no-run: not allowed with argument --run-dir" in capsys.readouterr().err

    # Direct callers that bypass argparse get the same refusal.
    rc = CloseoutCLI().run(_args(root, no_run=True, reason="r", paths=["feature.py"]))
    assert rc == 1
    assert "either --run-dir or --no-run, not both" in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head


def test_closeout_commit_without_a_route_names_both_routes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    head = _git(root, "rev-parse", "HEAD")

    rc = _closeout_main(root, "--paths", "feature.py")

    assert rc == 1
    out = capsys.readouterr().out
    assert "--run-dir" in out and "--no-run --reason" in out
    assert _git(root, "rev-parse", "HEAD") == head


@pytest.mark.parametrize(
    ("argv", "message"),
    [
        (["--no-run", "--reason", "r", "--run-id", "6046eaef"], "--run-id applies only to --run-dir"),
        (["--run-dir", "runs/subagents/20260729-120000-task-x", "--reason", "r"], "--reason applies only to --no-run"),
    ],
)
def test_closeout_commit_rejects_flags_from_the_other_route(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], argv: list[str], message: str
) -> None:
    root = _make_repo(tmp_path)
    _make_run_dir(root)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    head = _git(root, "rev-parse", "HEAD")

    rc = _closeout_main(root, *argv, "--paths", "feature.py")

    assert rc == 1
    assert message in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head


def test_closeout_commit_run_dir_through_main_is_unchanged(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    _make_run_dir(root)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")

    rc = _closeout_main(root, "--run-dir", "runs/subagents/20260729-120000-task-x", "--paths", "feature.py")

    assert rc == 0
    message = _git(root, "log", "-1", "--format=%B")
    assert message == (
        "closeout: task-x\n\n"
        "Task-Id: task-x\n"
        "Run-Dir: runs/subagents/20260729-120000-task-x"
    )
    entry = json.loads((root / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert set(entry) == {"task_id", "run_id", "run_dir", "commit", "session_sha256"}
    assert entry["run_dir"] == "runs/subagents/20260729-120000-task-x"
    assert entry["commit"] is None


@pytest.mark.parametrize("route", ["run-dir", "no-run"])
def test_closeout_commit_keeps_an_ignored_run_index_local(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], route: str
) -> None:
    """A project that ignores runs/subagents/index.jsonl gets the closing commit without it and
    without an error; the entry is still written to the local index."""
    root = _make_repo(tmp_path)
    (root / ".gitignore").write_text(".deskops.log\nruns/subagents/index.jsonl\n", encoding="utf-8")
    _git(root, "commit", "-q", "-am", "ignore the run index")
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")

    if route == "run-dir":
        _make_run_dir(root)
        rc = _closeout_main(root, "--run-dir", "runs/subagents/20260729-120000-task-x", "--paths", "feature.py")
    else:
        rc = _closeout_main(root, "--no-run", "--reason", "no subagent ran", "--paths", "feature.py")

    out = capsys.readouterr()
    assert rc == 0, out.out + out.err
    assert "ignored" not in (out.out + out.err).lower()
    assert _git(root, "ls-files", "runs/subagents/index.jsonl") == ""
    assert "runs/subagents/index.jsonl" not in _git(root, "show", "--name-only", "--format=", "HEAD").splitlines()
    assert _git(root, "show", "--name-only", "--format=", "HEAD").splitlines()[0] == "feature.py"
    assert "Task-Id: task-x" in _git(root, "log", "-1", "--format=%B")
    entry = json.loads((root / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert entry["task_id"] == "task-x" and entry["commit"] is None
    assert _git(root, "status", "--porcelain", "--untracked-files=all", "--", "feature.py") == ""


@pytest.mark.parametrize("route", ["run-dir", "no-run"])
def test_closeout_commit_leaves_the_working_tree_clean(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], route: str
) -> None:
    root = _make_repo(tmp_path)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")

    if route == "run-dir":
        _make_run_dir(root)
        rc = _closeout_main(root, "--run-dir", "runs/subagents/20260729-120000-task-x", "--paths", "feature.py")
    else:
        rc = _closeout_main(root, "--no-run", "--reason", "no subagent ran", "--paths", "feature.py")

    assert rc == 0, capsys.readouterr().out
    assert _git(root, "status", "--porcelain") == ""
    assert _git(root, "ls-files", "runs/subagents/index.jsonl") == "runs/subagents/index.jsonl"
    entry = json.loads((root / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert entry["task_id"] == "task-x"
    assert entry["commit"] is None
    head = _git(root, "rev-parse", "HEAD")
    assert _git(root, "log", "-1", "--format=%H", "--grep", "Task-Id: task-x") == head


def test_closeout_verify_passes_with_complete_evidence(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _make_repo(tmp_path)
    commit = _git(root, "rev-parse", "HEAD")
    _write_atom(root)
    _write_task(
        root,
        references=[
            "pytest tests/test_feature.py::test_feature",
            "desk/atoms/atom-evidence.md",
            commit,
        ],
        files=["desk/atoms/atom-evidence.md"],
    )
    _write(root / "tests" / "test_feature.py", "def test_feature():\n    assert True\n")

    rc = main(["closeout", "verify", "--root", str(root), "--task", "task-x"])
    out = capsys.readouterr()

    assert rc == 0
    report = json.loads(out.out)
    assert report["ok"] is True
    assert report["gates"]["tests"]["ok"] is True
    assert report["gates"]["atom_or_materialization_link"]["ok"] is True
    assert report["gates"]["commit"]["ok"] is True


def test_closeout_verify_rejects_loose_commit_and_test_references(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    ancestor = _git(root, "rev-parse", "HEAD")
    _git(root, "commit", "--allow-empty", "-q", "-m", "later")
    _write_atom(root)
    _write(root / "deskops" / "x.py", "x = 1\n")
    _write(root / "tests" / "test_x.py", "def test_y():\n    assert True\n")
    _write_task(
        root,
        references=[
            "HEAD",
            "main",
            "deskops/x.py",
            str(root / "tests" / "test_x.py"),
            "tests/../deskops/x.py",
            ancestor,
        ],
        files=["desk/atoms/atom-evidence.md"],
    )

    rc = main(["closeout", "verify", "--root", str(root), "--task", "task-x"])
    out = capsys.readouterr()

    assert rc == 1
    report = json.loads(out.out)
    assert report["gates"]["tests"]["evidence"] == []
    assert report["gates"]["commit"]["evidence"] == [ancestor]


def test_closeout_verify_accepts_ancestor_commit_and_test_node(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    ancestor = _git(root, "rev-parse", "HEAD")
    _git(root, "commit", "--allow-empty", "-q", "-m", "later")
    _write_atom(root)
    _write(root / "tests" / "test_x.py", "def test_y():\n    assert True\n")
    _write_task(
        root,
        references=[
            "pytest tests/test_x.py::test_y",
            ancestor,
        ],
        files=["desk/atoms/atom-evidence.md"],
    )

    rc = main(["closeout", "verify", "--root", str(root), "--task", "task-x"])
    out = capsys.readouterr()

    assert rc == 0
    report = json.loads(out.out)
    assert report["gates"]["tests"]["evidence"] == ["pytest tests/test_x.py::test_y"]
    assert report["gates"]["commit"]["evidence"] == [ancestor]
    assert report["ok"] is True


def test_closeout_verify_fails_non_zero_when_required_gate_is_missing(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _make_repo(tmp_path)
    _write_atom(root)
    _write_task(
        root,
        references=[
            "pytest tests/test_feature.py::test_feature",
            "desk/atoms/atom-evidence.md",
        ],
        files=["desk/atoms/atom-evidence.md"],
    )
    _write(root / "tests" / "test_feature.py", "def test_feature():\n    assert True\n")

    rc = main(["closeout", "verify", "--root", str(root), "--task", "task-x"])
    out = capsys.readouterr()

    assert rc == 1
    report = json.loads(out.out)
    assert report["ok"] is False
    assert report["gates"]["commit"]["ok"] is False
    assert report["findings"][0]["code"] == "missing_commit_evidence"


def test_closeout_verify_reports_structured_generated_artifact_findings(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _make_repo(tmp_path)
    commit = _git(root, "rev-parse", "HEAD")
    _write_task(
        root,
        references=[
            "pytest tests/test_diagram.py::test_diagram",
            commit,
            "task:task-follow-up",
        ],
        files=["docs/diagrams/example.md"],
    )
    _write(
        root / "desk" / "tasks" / "task-follow-up.md",
        """---
id: task-follow-up
status: active
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
checklists: []
tags: []
---

# Task Follow Up

## Rationale

Not provided.

## Goal

Follow up.

## Scope

Scoped.

## Implementation Path

Route follow-up.

## Validation

- pytest

## Done When

Done.
""",
    )
    _write(root / "tests" / "test_diagram.py", "def test_diagram():\n    assert True\n")
    _write(root / "docs" / "diagrams" / "example.mmd", "flowchart TD\n    A-->B\n")
    _write(root / "docs" / "diagrams" / "example.md", "# Example\n")

    rc = main(["closeout", "verify", "--root", str(root), "--task", "task-x"])
    out = capsys.readouterr()

    assert rc == 1
    report = json.loads(out.out)
    assert set(report["gates"].keys()) == {"tests", "atom_or_materialization_link", "commit"}
    assert report["gates"]["tests"]["ok"] is True
    assert report["gates"]["commit"]["ok"] is True
    assert report["gates"]["atom_or_materialization_link"]["ok"] is False
    assert any(item["code"] == "generated_artifact_missing_declared_sources" for item in report["findings"])
    assert any("follow-up:task:task-follow-up -> docs/diagrams/example.md" == item for item in report["gates"]["atom_or_materialization_link"]["evidence"])


def test_closeout_verify_tolerates_multi_document_yaml(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    commit = _git(root, "rev-parse", "HEAD")
    _write_atom(root)
    _write_task(
        root,
        references=[
            "pytest tests/test_feature.py::test_feature",
            "desk/atoms/atom-evidence.md",
            commit,
        ],
        files=["desk/atoms/atom-evidence.md"],
    )
    _write(root / "tests" / "test_feature.py", "def test_feature():\n    assert True\n")
    # Graph extraction scans docs/ Markdown for fenced YAML blocks and spec/
    # YAML files for metadata. A block or file that holds several documents is
    # not evidence of atom declarations; verify must skip it, not abort.
    _write(
        root / "docs" / "vocabulario.md",
        "# Vocabulario\n\n```yaml\nname: uml-clases\n---\nname: glyph-interfaz\n```\n",
    )
    _write(root / "spec" / "vocabulario.yaml", "name: a\n---\nname: b\n")

    result = subprocess.run(
        [sys.executable, "-m", "deskops", "closeout", "verify", "--root", str(root), "--task", "task-x"],
        cwd=root,
        capture_output=True,
        text=True,
    )

    assert "Unexpected" not in result.stderr
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["ok"] is True


@pytest.mark.parametrize("committed", [False, True], ids=["new-task", "committed-task"])
def test_closeout_commit_accepts_a_directory_holding_the_task(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], committed: bool
) -> None:
    root = _make_repo(tmp_path)
    _write_task(root, references=[], files=[])
    if committed:
        _git(root, "add", "desk/tasks/task-x.md")
        _git(root, "commit", "-q", "-m", "add task")
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")

    rc = _closeout_main(root, "--no-run", "--reason", "no subagent ran", "--paths", "desk/tasks", "feature.py")

    assert rc == 0, capsys.readouterr().out
    assert not (root / "desk" / "tasks" / "task-x.md").exists()
    assert _git(root, "status", "--porcelain") == ""
    assert "feature.py" in _git(root, "show", "--name-only", "--format=", "HEAD").splitlines()


def test_closeout_records_a_never_committed_task_before_the_closing_commit(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _write_task(root, references=[], files=[])
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    before = _git(root, "rev-parse", "HEAD")

    rc = _closeout_main(root, "--no-run", "--reason", "no subagent ran", "--paths", "desk/tasks", "feature.py")

    assert rc == 0, capsys.readouterr().out
    assert _git(root, "status", "--porcelain") == ""
    assert _git(root, "log", "--format=%s", f"{before}..HEAD").splitlines() == [
        "closeout: task-x",
        "desk: registra task-x",
    ]
    record = _git(root, "log", "-1", "--format=%B", "HEAD~1")
    assert record.splitlines()[0] == "desk: registra task-x"
    assert "Task-Id: task-x" in record
    assert _git(root, "log", "-1", "--format=%(trailers:key=Closeout-Mode,valueonly)", "HEAD~1") == "record"
    body = _git(root, "show", "HEAD~1:desk/tasks/task-x.md")
    assert "# Task X" in body
    assert "Verify closeout." in body
    assert not (root / "desk" / "tasks" / "task-x.md").exists()


def test_closeout_committed_task_keeps_a_single_closing_commit(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _write_task(root, references=[], files=[])
    _git(root, "add", "desk/tasks/task-x.md")
    _git(root, "commit", "-q", "-m", "add task")
    before = _git(root, "rev-parse", "HEAD")
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")

    rc = _closeout_main(root, "--no-run", "--reason", "no subagent ran", "--paths", "desk/tasks", "feature.py")

    assert rc == 0, capsys.readouterr().out
    assert _git(root, "status", "--porcelain") == ""
    assert _git(root, "log", "--format=%s", f"{before}..HEAD").splitlines() == ["closeout: task-x"]
    assert not (root / "desk" / "tasks" / "task-x.md").exists()


def _write_board(root: Path, task_id: str = "task-x") -> None:
    _write(
        root / "desk" / "tasks" / "Board.md",
        f"""---
id: board-tasks
scope: desk
tasks:
- desk/tasks/{task_id}.md
pills: []
rituals: []
tags: []
---

# Repo Board

## Purpose

Route the active task.

## Notes

No additional notes.

## Task Details
""",
    )


def _write_lifecycle_task(root: Path, task_id: str = "task-x") -> None:
    _write(
        root / "desk" / "tasks" / f"{task_id}.md",
        f"""---
id: {task_id}
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Task X

## Rationale

The subject was removed.

## Goal

Close it honestly.

## Scope

Stay scoped.

## Implementation Path

Supersede it.

## Validation

- pytest

## Done When

Closed.
""",
    )


def _commit_task_on_board(root: Path, task_id: str = "task-x") -> None:
    _write_lifecycle_task(root, task_id)
    _write_board(root, task_id)
    _git(root, "add", "desk/tasks")
    _git(root, "commit", "-q", "-m", "add task and board")


def _supersede_main(root: Path, *argv: str) -> int:
    return main(["closeout", "supersede", "--root", str(root), "--task", "task-x", *argv])


def test_closeout_supersede_closes_a_task_with_a_reason_and_commit_ref(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)
    ref = _git(root, "rev-parse", "HEAD")

    rc = _supersede_main(root, "--reason", "The owner removed the subject", "--ref", ref)

    assert rc == 0, capsys.readouterr().out
    message = _git(root, "log", "-1", "--format=%B")
    assert message.splitlines()[0] == "closeout: task-x"
    assert "Task-Id: task-x" in message
    assert "Closeout-Mode: superseded" in message
    assert "Closeout-Reason: The owner removed the subject" in message
    assert f"Closeout-Ref: {ref}" in message
    assert _git(root, "log", "-1", "--format=%(trailers:key=Closeout-Mode,valueonly)") == "superseded"

    assert not (root / "desk" / "tasks" / "task-x.md").exists()
    assert "desk/tasks/task-x.md" not in (root / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert _git(root, "status", "--porcelain") == ""

    entry = json.loads((root / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert entry == {
        "task_id": "task-x",
        "run_id": None,
        "run_dir": None,
        "commit": None,
        "session_sha256": None,
        "mode": "superseded",
    }
    assert _git(root, "log", "-1", "--format=%H", "--grep", "Task-Id: task-x") == _git(root, "rev-parse", "HEAD")
    assert sorted(_git(root, "show", "--name-only", "--format=", "HEAD").splitlines()) == [
        "desk/tasks/Board.md",
        "desk/tasks/task-x.md",
        "runs/subagents/index.jsonl",
    ]


def test_closeout_supersede_closes_a_task_whose_lifecycle_the_model_rejects(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A draft after task_hands_to_closeout (shared_llm-gateway, no migration decides it): supersede
    reads its frontmatter instead of the model and closes it with the same commit and trailers."""
    from deskops.models.task_lifecycle import lifecycle_errors

    root = _make_repo(tmp_path)
    _write_lifecycle_task(root)
    path = root / "desk" / "tasks" / "task-x.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("status: active\n", "status: draft\n").replace("current_node: ritual-testing\n", "current_node: ritual-closeout\n")
    text = text.replace("history:\n- task_activates\n", "history:\n- task_activates\n- task_hands_to_closeout\n")
    path.write_text(text, encoding="utf-8")
    assert lifecycle_errors("draft", "ritual-closeout", ["task_activates", "task_hands_to_closeout"])
    _write_board(root, "task-x")
    _git(root, "add", "desk/tasks")
    _git(root, "commit", "-q", "-m", "add incoherent task and board")
    ref = _git(root, "rev-parse", "HEAD")

    rc = _supersede_main(root, "--reason", "The owner replaced it", "--ref", ref)

    assert rc == 0, capsys.readouterr().out
    message = _git(root, "log", "-1", "--format=%B")
    assert message.splitlines()[0] == "closeout: task-x"
    assert "Task-Id: task-x" in message
    assert "Closeout-Mode: superseded" in message
    assert "Closeout-Reason: The owner replaced it" in message
    assert f"Closeout-Ref: {ref}" in message
    assert not path.exists()
    assert "desk/tasks/task-x.md" not in (root / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert _git(root, "status", "--porcelain") == ""
    assert sorted(_git(root, "show", "--name-only", "--format=", "HEAD").splitlines()) == [
        "desk/tasks/Board.md",
        "desk/tasks/task-x.md",
        "runs/subagents/index.jsonl",
    ]


def test_closeout_supersede_accepts_an_existing_path_ref(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)

    rc = _supersede_main(root, "--reason", "subject path was deleted", "--ref", "desk/tasks/Board.md")

    assert rc == 0, capsys.readouterr().out
    assert not (root / "desk" / "tasks" / "task-x.md").exists()
    assert "Closeout-Ref: desk/tasks/Board.md" in _git(root, "log", "-1", "--format=%B")


@pytest.mark.parametrize("reason", ["", "   "])
def test_closeout_supersede_requires_a_reason(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], reason: str
) -> None:
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)
    head = _git(root, "rev-parse", "HEAD")
    ref = "desk/tasks/Board.md"

    rc = _supersede_main(root, "--reason", reason, "--ref", ref)

    assert rc == 1
    assert "Supersede needs a non-empty --reason" in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head
    assert _git(root, "status", "--porcelain") == ""
    assert (root / "desk" / "tasks" / "task-x.md").exists()
    assert not (root / "runs" / "subagents" / "index.jsonl").exists()


@pytest.mark.parametrize("ref", ["does-not-exist.txt", "deadbeef", "0" * 40])
def test_closeout_supersede_refuses_an_unresolvable_ref_and_leaves_the_tree_unchanged(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], ref: str
) -> None:
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)
    head = _git(root, "rev-parse", "HEAD")

    rc = _supersede_main(root, "--reason", "subject removed", "--ref", ref)

    assert rc == 1
    assert "Unresolvable --ref" in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head
    assert _git(root, "status", "--porcelain") == ""
    assert (root / "desk" / "tasks" / "task-x.md").read_text(encoding="utf-8").count("status: active") == 1
    assert not (root / "runs" / "subagents" / "index.jsonl").exists()


def test_closeout_supersede_requires_at_least_one_ref(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)
    head = _git(root, "rev-parse", "HEAD")

    rc = main(["closeout", "supersede", "--root", str(root), "--task", "task-x", "--reason", "subject removed"])

    assert rc == 2
    assert "--ref" in capsys.readouterr().err
    assert _git(root, "rev-parse", "HEAD") == head


def test_closeout_supersede_requires_the_reason_flag(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)
    head = _git(root, "rev-parse", "HEAD")

    rc = _supersede_main(root, "--ref", "desk/tasks/Board.md")

    assert rc == 2
    assert "--reason" in capsys.readouterr().err
    assert _git(root, "rev-parse", "HEAD") == head


def _write_legacy_task(
    root: Path,
    task_id: str = "task-x",
    status: str = "resolved",
    filename: str | None = None,
) -> None:
    _write(
        root / "desk" / "tasks" / (filename or f"{task_id}.md"),
        f"""---
id: "{task_id}"
status: {status}
summary: ''
tags: []
references:
- 3900ad4
depends_on: []
pills: []
files: []
task_type: implementation
atoms: []
---

# Task X

## Rationale

Resolved before the ritual lifecycle existed.

## Goal

Remove the resolved task.

## Scope

Stay scoped.

## Implementation Path

Retire it.

## Validation

- pytest

## Done When

Retired.
""",
    )


def _commit_legacy_task_on_board(
    root: Path,
    task_id: str = "task-x",
    status: str = "resolved",
    filename: str | None = None,
) -> None:
    _write_legacy_task(root, task_id, status, filename)
    _write_board(root, task_id)
    _git(root, "add", "desk/tasks")
    _git(root, "commit", "-q", "-m", "add legacy task and board")


def _retire_main(root: Path, *argv: str) -> int:
    return main(["closeout", "retire", "--root", str(root), "--task", "task-x", *argv])


@pytest.mark.parametrize("status", ["resolved", "closed", "done", "complete", "cancelled"])
def test_closeout_retire_removes_a_legacy_resolved_task(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], status: str
) -> None:
    root = _make_repo(tmp_path)
    _commit_legacy_task_on_board(root, status=status)
    ref = _git(root, "rev-parse", "HEAD")
    before = (root / "desk" / "tasks" / "task-x.md").read_text(encoding="utf-8")

    rc = _retire_main(root, "--reason", "Resolved before the ritual lifecycle existed", "--ref", ref)

    assert rc == 0, capsys.readouterr().out
    message = _git(root, "log", "-1", "--format=%B")
    assert message.splitlines()[0] == "closeout: task-x"
    assert "Task-Id: task-x" in message
    assert "Closeout-Mode: legacy-resolved" in message
    assert "Closeout-Reason: Resolved before the ritual lifecycle existed" in message
    assert f"Closeout-Ref: {ref}" in message
    assert _git(root, "log", "-1", "--format=%(trailers:key=Closeout-Mode,valueonly)") == "legacy-resolved"

    assert not (root / "desk" / "tasks" / "task-x.md").exists()
    assert f"status: {status}" in before
    assert "desk/tasks/task-x.md" not in (root / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert _git(root, "status", "--porcelain") == ""

    entry = json.loads((root / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert entry == {
        "task_id": "task-x",
        "run_id": None,
        "run_dir": None,
        "commit": None,
        "session_sha256": None,
        "mode": "legacy-resolved",
    }
    assert _git(root, "log", "-1", "--format=%H", "--grep", "Task-Id: task-x") == _git(root, "rev-parse", "HEAD")
    assert sorted(_git(root, "show", "--name-only", "--format=", "HEAD").splitlines()) == [
        "desk/tasks/Board.md",
        "desk/tasks/task-x.md",
        "runs/subagents/index.jsonl",
    ]


def _commit_pre_cc31_task_on_board(root: Path, status: str) -> None:
    """A task as a desk migrated before CC31 left it: a terminal or drawer status with an empty
    history at the entry node, which TaskDoc's validator rejects."""
    _write_legacy_task(root, status=status)
    path = root / "desk" / "tasks" / "task-x.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("atoms: []\n", "atoms: []\ncurrent_node: ritual-execution\nhistory: []\n", 1), encoding="utf-8")
    _write_board(root, "task-x")
    _git(root, "add", "desk/tasks")
    _git(root, "commit", "-q", "-m", "add pre-CC31 task and board")


@pytest.mark.parametrize("status", ["superseded", "cancelled", "deferred", "candidate"])
def test_closeout_retire_removes_a_pre_cc31_task_the_model_rejects(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], status: str
) -> None:
    """d3: retire reads the frontmatter, so the model's rejection of the legacy state does not stop it."""
    from deskops.models.task_lifecycle import lifecycle_errors

    assert lifecycle_errors(status, "ritual-execution", [])
    root = _make_repo(tmp_path)
    _commit_pre_cc31_task_on_board(root, status)
    ref = _git(root, "rev-parse", "HEAD")

    rc = _retire_main(root, "--reason", "Left by the pre-CC31 migration", "--ref", ref)

    assert rc == 0, capsys.readouterr().out
    message = _git(root, "log", "-1", "--format=%B")
    assert "Task-Id: task-x" in message
    assert "Closeout-Mode: legacy-resolved" in message
    assert not (root / "desk" / "tasks" / "task-x.md").exists()
    assert "desk/tasks/task-x.md" not in (root / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert _git(root, "status", "--porcelain") == ""


@pytest.mark.parametrize("status", ["superseded", "deferred", "candidate"])
def test_closeout_retire_refuses_a_terminal_or_drawer_status_with_a_history(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], status: str
) -> None:
    """Only the pre-CC31 shape (empty history) is retired; a task closed through the lifecycle is not."""
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)
    path = root / "desk" / "tasks" / "task-x.md"
    path.write_text(path.read_text(encoding="utf-8").replace("status: active", f"status: {status}"), encoding="utf-8")
    _git(root, "commit", "-qam", "status by hand")
    head = _git(root, "rev-parse", "HEAD")

    assert _retire_main(root, "--reason", "not legacy", "--ref", head) == 1
    assert "can be retired" in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head
    assert path.exists()


def test_closeout_retire_refuses_a_coherent_task_at_ritual_execution(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_pre_cc31_task_on_board(root, "draft")
    head = _git(root, "rev-parse", "HEAD")

    assert _retire_main(root, "--reason", "still to do", "--ref", head) == 1
    assert "has status 'draft'" in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head
    assert (root / "desk" / "tasks" / "task-x.md").exists()


def test_closeout_retire_default_subject_names_the_task_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_legacy_task_on_board(root, task_id="001", filename="001-some-title.md")
    ref = _git(root, "rev-parse", "HEAD")

    rc = main(
        [
            "closeout",
            "retire",
            "--root",
            str(root),
            "--task",
            "001",
            "--reason",
            "Resolved before the ritual lifecycle existed",
            "--ref",
            ref,
        ]
    )

    assert rc == 0, capsys.readouterr().out
    message = _git(root, "log", "-1", "--format=%B")
    assert message.splitlines()[0] == "closeout: 001-some-title"
    assert "Task-Id: 001" in message
    assert not (root / "desk" / "tasks" / "001-some-title.md").exists()


def test_closeout_retire_default_subject_is_unchanged_when_the_stem_matches_the_id(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_legacy_task_on_board(root)
    ref = _git(root, "rev-parse", "HEAD")

    rc = _retire_main(root, "--reason", "Resolved before the ritual lifecycle existed", "--ref", ref)

    assert rc == 0, capsys.readouterr().out
    message = _git(root, "log", "-1", "--format=%B")
    assert message.splitlines()[0] == "closeout: task-x"
    assert "Task-Id: task-x" in message


def test_closeout_retire_refuses_a_task_that_is_not_resolved(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)
    head = _git(root, "rev-parse", "HEAD")
    ref = _git(root, "rev-parse", "HEAD")

    rc = _retire_main(root, "--reason", "not resolved yet", "--ref", ref)

    assert rc == 1
    assert (
        "only resolved, closed, done, complete or cancelled tasks, or superseded, deferred or "
        "candidate tasks with an empty history, can be retired"
    ) in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head
    assert _git(root, "status", "--porcelain") == ""
    assert (root / "desk" / "tasks" / "task-x.md").read_text(encoding="utf-8").count("status: active") == 1
    assert "desk/tasks/task-x.md" in (root / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert not (root / "runs" / "subagents" / "index.jsonl").exists()


@pytest.mark.parametrize("ref", ["does-not-exist.txt", "deadbeef", "0" * 40, "desk/tasks/Board.md"])
def test_closeout_retire_refuses_a_ref_that_is_not_an_ancestor_commit_and_leaves_the_tree_unchanged(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], ref: str
) -> None:
    root = _make_repo(tmp_path)
    _commit_legacy_task_on_board(root)
    head = _git(root, "rev-parse", "HEAD")

    rc = _retire_main(root, "--reason", "resolved long ago", "--ref", ref)

    assert rc == 1
    printed = capsys.readouterr().out
    assert "Unresolvable --ref" in printed
    assert "need a commit that is HEAD or an ancestor" in printed
    assert _git(root, "rev-parse", "HEAD") == head
    assert _git(root, "status", "--porcelain") == ""
    assert (root / "desk" / "tasks" / "task-x.md").read_text(encoding="utf-8").count("status: resolved") == 1
    assert not (root / "runs" / "subagents" / "index.jsonl").exists()


def test_closeout_retire_requires_at_least_one_ref(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_legacy_task_on_board(root)
    head = _git(root, "rev-parse", "HEAD")

    rc = main(["closeout", "retire", "--root", str(root), "--task", "task-x", "--reason", "resolved"])

    assert rc == 2
    assert "--ref" in capsys.readouterr().err
    assert _git(root, "rev-parse", "HEAD") == head


def test_closeout_retire_requires_a_reason(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_legacy_task_on_board(root)
    head = _git(root, "rev-parse", "HEAD")
    ref = _git(root, "rev-parse", "HEAD")

    rc = _retire_main(root, "--reason", "   ", "--ref", ref)

    assert rc == 1
    assert "Retire needs a non-empty --reason" in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head
    assert _git(root, "status", "--porcelain") == ""
    assert (root / "desk" / "tasks" / "task-x.md").exists()
    assert not (root / "runs" / "subagents" / "index.jsonl").exists()


def _commit_code_with_task_trailer(root: Path) -> str:
    """A code commit carrying the task's Task-Id trailer, on top of a committed task."""
    _write_task(root, references=["seed.txt"], files=["feature.py"])
    _git(root, "add", "desk/tasks/task-x.md")
    _git(root, "commit", "-q", "-m", "add task")
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    _git(root, "add", "feature.py")
    _git(root, "commit", "-q", "-m", "feature\n\nTask-Id: task-x")
    return _git(root, "rev-parse", "HEAD")


def _write_commit_receipt(root: Path, sha: str, verdict: str = "accepted") -> None:
    _write(
        root / "desk" / "reviews" / "task-x" / "evidence-commit-1.md",
        f"""---
id: review-task-x-evidence-commit-1
kind: evidence
fact: commit
value: {sha}
subject: doc:TaskDoc:task-x
subject_ref: ''
engine: deskops-closeout
actor: deskops
run_dir: ''
input_sha256: ''
output_sha256: ''
verdict: {verdict}
reason: 'verified: commit {sha}'
created_at: '2026-11-16T00:00:00+00:00'
disposed_at: '2026-11-16T00:00:00+00:00'
disposed_by: deskops
tags:
- workspace:desk
---

# Closeout evidence commit of task-x

## Summary

closeout verify checked commit: {sha}

## Disposition

Verdict {verdict}: verified: commit {sha}
""",
    )


@pytest.mark.parametrize("citation", ["reference", "receipt"])
def test_closeout_commit_does_not_amend_a_head_the_task_cites_as_commit_evidence(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], citation: str
) -> None:
    """A HEAD with the task's Task-Id that the task cites as commit evidence (its short sha in
    references, or the value of an accepted evidence-commit receipt) survives with its sha;
    the close is a separate commit on top of it."""
    root = _make_repo(tmp_path)
    code = _commit_code_with_task_trailer(root)
    if citation == "reference":
        _write_task(root, references=["seed.txt", code[:8]], files=["feature.py"])
    else:
        _write_commit_receipt(root, code)
    capsys.readouterr()

    assert main(["closeout", "verify", "--root", str(root), "--task", "task-x"]) in (0, 1)
    report = json.loads(capsys.readouterr().out)
    if citation == "reference":
        assert report["gates"]["commit"]["evidence"] == [code[:8]]

    paths = ["desk/tasks"] if citation == "reference" else ["desk/tasks", "desk/reviews"]
    rc = _closeout_main(root, "--no-run", "--reason", "no subagent ran", "--paths", *paths)

    assert rc == 0, capsys.readouterr().out
    head = _git(root, "rev-parse", "HEAD")
    assert head != code
    assert _git(root, "rev-parse", "HEAD^") == code
    assert _git(root, "log", "-1", "--format=%s") == "closeout: task-x"
    assert subprocess.run(["git", "merge-base", "--is-ancestor", code, head], cwd=root).returncode == 0
    assert _git(root, "show", "--name-only", "--format=", code).splitlines() == ["feature.py"]
    assert not (root / "desk" / "tasks" / "task-x.md").exists()


def test_closeout_commit_still_amends_an_uncited_head_with_the_task_id(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A HEAD with the task's Task-Id that the task does not cite (no reference, only a
    rejected receipt) is folded into the close as before."""
    root = _make_repo(tmp_path)
    code = _commit_code_with_task_trailer(root)
    before = _git(root, "rev-parse", "HEAD^")
    _write_commit_receipt(root, code, verdict="rejected")

    rc = _closeout_main(root, "--no-run", "--reason", "no subagent ran", "--paths", "desk/tasks", "desk/reviews")

    assert rc == 0, capsys.readouterr().out
    head = _git(root, "rev-parse", "HEAD")
    assert head != code
    assert _git(root, "rev-parse", "HEAD^") == before
    assert subprocess.run(["git", "merge-base", "--is-ancestor", code, head], cwd=root).returncode != 0
    assert "feature.py" in _git(root, "show", "--name-only", "--format=", "HEAD").splitlines()
    assert "Task-Id: task-x" in _git(root, "log", "-1", "--format=%B")


# --- braces in --reason and the desk/reviews projection (task-valores-con-llaves-...) ------------


@pytest.mark.parametrize(
    "reason",
    [
        "cierre {a}",
        "cierre {{a}} docker {{.State}}",
        "cierre {{{a}}}",
        "cierre a}",
        "cierre a}}",
        "cierre a}}}",
        "cierre {commit} literal",
    ],
)
def test_closeout_commit_keeps_braces_in_the_reason_byte_for_byte(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], reason: str
) -> None:
    """The reason is text: the commit trailer and the printed line carry it unchanged, rc 0."""
    root = _make_repo(tmp_path)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")

    rc = _closeout_main(root, "--no-run", "--reason", reason, "--paths", "feature.py")

    out = capsys.readouterr().out
    assert rc == 0, out
    assert _git(root, "log", "-1", "--format=%(trailers:key=Closeout-Reason,valueonly)") == reason
    commit = _git(root, "rev-parse", "HEAD")[:12]
    assert out.splitlines()[0] == f"Closing commit {commit} made manually (no run): {reason}"


def test_closeout_commit_folds_the_verify_receipt_projection_into_the_closing_commit(
    lifecycle_desk: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """verify writes its receipts without committing them; the close commits their
    desk/reviews/<task> projection with the rest and leaves no file behind."""
    from closeout_desk import store_repo
    from deskops.operations import DeskopsOperations

    root = store_repo(lifecycle_desk)
    task_id = DeskopsOperations(root).create_task_bundle(
        {
            "title": "Llaves",
            "goal": "g",
            "scope": "s",
            "implementation_path": "i",
            "done_when": "d",
            "validation": ["echo ok"],
            "task_type": "task.external",
        }
    ).task_id
    assert main(["edit", "task", task_id, "references", '["https://example.com/e"]', "--root", str(root)]) == 0
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "task")

    assert main(["closeout", "verify", "--task", task_id, "--root", str(root)]) == 0
    projection = f"desk/reviews/{task_id}/evidence-external-1.md"
    assert "?? desk/reviews/" in _git(root, "status", "--porcelain", "--untracked-files=normal")
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    capsys.readouterr()

    rc = main(
        ["closeout", "commit", "--root", str(root), "--task", task_id,
         "--no-run", "--reason", "cierre {a}", "--paths", "feature.py"]
    )

    assert rc == 0, capsys.readouterr().out
    assert _git(root, "status", "--porcelain") == ""
    committed = _git(root, "show", "--name-only", "--format=", "HEAD").split()
    assert projection in committed
    assert "feature.py" in committed


@pytest.mark.parametrize("mode", ["run-dir", "no-run"])
def test_closeout_commit_includes_the_run_md_of_every_registered_run_doc_git_lacks(
    lifecycle_desk: Path, capsys: pytest.CaptureFixture[str], mode: str
) -> None:
    """Another run's RunDoc reached the store (here an earlier commit published it) while
    its run.md stayed untracked; the next close carries that run.md, so every RunDoc path
    .sldb/store.yaml registers is in HEAD and a clean clone can build the store."""
    from closeout_desk import store_repo
    from deskops.runtime.scion import record_scion_run

    root = store_repo(lifecycle_desk)
    other_rel = "runs/subagents/exec-other/run.md"
    record_scion_run(
        root, task_id="task-other", role_id="role-deskops-executor", kind="claude",
        agent_slug="other", run_dir="runs/subagents/exec-other",
    )
    # An unrelated close published the store with the other run's registration only.
    _git(root, "add", "-A", "--", ".sldb")
    _git(root, "commit", "-q", "-m", "publishes the store", "--", ".sldb")
    own_dir = "runs/subagents/exec-own"
    record_scion_run(
        root, task_id="task-x", role_id="role-deskops-executor", kind="claude",
        agent_slug="own", run_dir=own_dir,
    )
    for fname in ["board.txt", "task.txt", "git-status.txt", "result-summary.md"]:
        (root / own_dir / fname).write_text(f"{fname}\n", encoding="utf-8")
    # A registered RunDoc without a run.md on disk is not the close's concern.
    manifest_path = root / ".sldb" / "store.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    run_item = next(item for item in manifest["include"] if item.get("model") == "RunDoc")
    registered = [entry["path"] for entry in run_item["paths"]]
    assert {other_rel, f"{own_dir}/run.md"} <= set(registered)
    assert subprocess.run(
        ["git", "cat-file", "-e", f"HEAD:{other_rel}"], cwd=root, capture_output=True
    ).returncode != 0
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    capsys.readouterr()

    route = ["--run-dir", own_dir] if mode == "run-dir" else ["--no-run", "--reason", "sin corrida"]
    rc = _closeout_main(root, *route, "--paths", "feature.py")

    assert rc == 0, capsys.readouterr().out
    committed = _git(root, "show", "--name-only", "--format=", "HEAD").split()
    assert other_rel in committed
    assert "feature.py" in committed
    head_manifest = yaml.safe_load(_git(root, "show", "HEAD:.sldb/store.yaml"))
    head_paths = [
        entry["path"]
        for item in head_manifest["include"]
        if item.get("model") == "RunDoc"
        for entry in item["paths"]
    ]
    assert f"{own_dir}/run.md" in head_paths
    for path in head_paths:
        assert subprocess.run(
            ["git", "cat-file", "-e", f"HEAD:{path}"], cwd=root, capture_output=True
        ).returncode == 0, f"{path} is registered but not in HEAD"


def test_closeout_commit_skips_a_registered_run_doc_without_a_run_md(
    lifecycle_desk: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from closeout_desk import store_repo
    from deskops.runtime.scion import record_scion_run

    root = store_repo(lifecycle_desk)
    record_scion_run(
        root, task_id="task-other", role_id="role-deskops-executor", kind="claude",
        agent_slug="gone", run_dir="runs/subagents/exec-gone",
    )
    (root / "runs" / "subagents" / "exec-gone" / "run.md").unlink()
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    capsys.readouterr()

    rc = _closeout_main(root, "--no-run", "--reason", "sin corrida", "--paths", "feature.py")

    assert rc == 0, capsys.readouterr().out
    committed = _git(root, "show", "--name-only", "--format=", "HEAD").split()
    assert "feature.py" in committed
    assert not any(path.startswith("runs/subagents/exec-gone") for path in committed)

FILE:instruccion
Cold-bundle de la tarea task-rundoc-por-intento-identidad-propia-intencion-y-confirmacion-de-dispatch-separadas-y-el-closeout-act: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_scion_runtime.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_model_contract_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

