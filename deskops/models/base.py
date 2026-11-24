from pydantic import Field, field_validator

from sldb import StructuredNLDoc


class PrimitiveDoc(StructuredNLDoc):
    __template__ = """---
# primitive-xxx
id: ⸢rev•id⸥
# draft | active | archived
status: ⸢rev•status⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

⸢rev•summary⸥
""".strip()

    title: str = Field(description="Short primitive title.")
    id: str = Field(description="Stable primitive identifier.")
    status: str = Field(default="", description="Primitive lifecycle status.")
    summary: str = Field(
        default="",
        description="Short semantic summary for the primitive.",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end using namespaced forms.",
    )

    @field_validator("tags", mode="before")
    @classmethod
    def _one_tag_vocabulary(cls, tags: object) -> object:
        # The model's own tags (``__semantics__``) are canonical: no repeats, class names or
        # flat restatements of them are written (deskops.tag_vocabulary).
        if not isinstance(tags, (list, tuple)):
            return tags
        from deskops.tag_vocabulary import canonical_tags

        return canonical_tags(tags, cls)


class OperationalArtifactDoc(PrimitiveDoc):
    current_node: str = Field(
        default="",
        description="Current node of the artifact in its lifecycle graph (a ritual id, or 'complete').",
    )
    history: list[str] = Field(
        default_factory=list,
        description="Lifecycle transitions the artifact went through, by relation type.",
    )
