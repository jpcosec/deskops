from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

from typing import Literal

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
    retry_exit_codes: list[int] = Field(
        default_factory=list,
        description="Exit codes that leave the job pending for the next run instead of failing it",
    )


DEFAULT_WAKE_COMMAND = ["scion", "message", "--wake", "@{agent}", "--project", "{project}", "nota nueva: {note}"]


class IdentityConfig(BaseModel):
    scion_project: str = Field(min_length=1, description="Scion project of the desk's identity agent")
    agent: str = Field(min_length=1, description="Scion agent name of the desk's identity")
    wake: bool = Field(default=False, description="Wake the identity when a note reaches the inbox")
    command: list[str] = Field(
        default_factory=lambda: list(DEFAULT_WAKE_COMMAND),
        min_length=1,
        description="argv (no shell) with the markers {agent}, {project} and {note}",
    )


class IntegrateConfig(BaseModel):
    remote_url: str = Field(min_length=1, description="URL or path of the remote that receives the push")
    branch: str = Field(min_length=1, description="Remote branch that receives the code commit and the tip")
    suite: list[str] = Field(min_length=1, description="argv of the full suite, run in the clean copy")
    suite_timeout: int = Field(default=5400, gt=0, description="Seconds before the suite is killed")
    tests_lock: str | None = Field(default=None, description="Lock file taken exclusively around the suite")
    tools_checkout: str | None = Field(default=None, description="Tools checkout updated after the push")
    push_env: dict[str, str] = Field(default_factory=dict, description="Environment added to the git push and gh commands")
    mode: Literal["push", "pr"] = Field(
        default="push",
        description="'push' pushes the tip to the branch; 'pr' pushes task/<id> and opens a PR to the branch",
    )


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
    roles_root: str | None = Field(
        default=None,
        description="Repo whose desk/roles holds the RoleDocs; default is the task root. Relative paths resolve against the task root.",
    )
    quick_gates: list[str] | None = Field(
        default=None,
        description="Optional argv of the fast gates the executor and the tester must run (rc 0) before the commit and the verdict.",
    )


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
    identity: IdentityConfig | None = Field(
        default=None,
        description="Scion identity of the desk, woken by deskops when a note reaches the inbox (usually in config.local.json).",
    )
    integrate: IntegrateConfig | None = Field(
        default=None,
        description="deskops integrate: remote, branch, suite and tools checkout of the integration.",
    )
    unowned_target: str | None = Field(
        default=None,
        description="Registered repo id that receives `message send --to unowned` (what no repo owns).",
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
