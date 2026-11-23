from typing import Optional

from pydantic import Field, field_validator

from sldb import StructuredNLDoc


class RepositoryDoc(StructuredNLDoc):
    # Artifact-level defaults `deskops add` applies (formerly one YAML spec per artifact):
    # the id built from the slug, the status a new document gets, and its default tags.
    __artifact__ = {
        "id_pattern": "repo-{slug}",
        "status_default": "active",
        "tags": ["workspace:desk", "artifact:repository"],
    }
    """Model for registering a repository/tool within the opsys ecosystem."""

    __semantics__ = {
        "type": ["desk", "repository"],
        "workspace": ["desk", "registry"],
    }
    __template__ = """---
# repo-xxx
id: ⸢rev•id⸥
# Relative path to repository
path: ⸢rev•path⸥
# active | maintenance | archived
status: ⸢rev•status⸥
# e.g., type:tool, layer:infra
tags: ⸢rev•tags⸥
# Globs relative to the ecosystem root that this repo owns
owns_paths: ⸢rev•owns_paths⸥
# Topics this repo owns
owns_topics: ⸢rev•owns_topics⸥
---

# Repository: ⸢rev•name⸥

## Description

_Describe the repository purpose, scope, and role in the ecosystem._

⸢rev,markdown•description⸥
"""

    name: str = Field(description="Short human-readable name of the repository.")
    id: Optional[str] = Field(
        default=None,
        description="Stable unique identifier for the repository."
    )
    path: Optional[str] = Field(
        default=None,
        description="Relative path to the repository root from the ecosystem root."
    )
    status: str = Field(
        default="active",
        description="Current status of the repository (e.g., active, maintenance, archived).",
    )
    description: str = Field(description="Markdown description of the repository's purpose and scope.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags for categorization (e.g., type:tool, layer:infra).",
    )
    owns_paths: list[str] = Field(
        default_factory=list,
        description="Globs relative to the ecosystem root of the paths this repository owns.",
    )
    owns_topics: list[str] = Field(
        default_factory=list,
        description="Topics this repository owns (answers `deskops owner <topic>`).",
    )

    @field_validator("owns_paths", "owns_topics", mode="before")
    @classmethod
    def _missing_owns_is_empty(cls, value: object) -> object:
        # Cards written before these fields existed leave the template placeholder empty.
        return [] if value is None else value
