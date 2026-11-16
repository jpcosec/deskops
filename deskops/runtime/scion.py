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
    if role_name not in {"executor", "tester"}:
        raise ValueError(f"role must be executor or tester, got '{role}'")
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
    prefix = "deskops-e" if role_name == "executor" else "deskops-t"
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
    return list(build_agent_spec_args(role_doc, stripped))


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
    verification) or ``coordinator`` (owns a desk); by default the selected
    role's own name/id decides, and an explicit mode always wins.

    ``context`` is the optional five-key Scion runtime context. Omitted, the
    CLI and path/environment behavior is preserved; the generated prompt text is
    corrected intentionally rather than kept byte-identical. Supplied, it adds
    the DESKOPS_* environment, a workspace volume and concrete command paths.
    """
    if mode not in (None, "executor", "coordinator", "tester"):
        raise ValueError(f"mode must be executor, coordinator or tester, got '{mode}'")
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
        "6. **Test independently.** When activity=completed, inspect the executor handoff before testing. Dispatch a\n"
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
