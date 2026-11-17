---
sldb:
  by: agent
  at: '2026-11-17T00:04:55Z'
  authority: generated
  via: create_document
# runtime-xxx
id: runtime-claude-haiku-reviewer
# draft | active | archived
status: ''
# Runtime binary identifier matching RoleDoc.kind values, e.g. pi, claude, codex
kind: claude
binary: claude
# Empty means this runtime does not support that capability
model_flag: ''
fallback_models_flag: ''
# comma | space | repeat
fallback_models_join: comma
tools_flag: ''
# comma | space | repeat
tools_join: comma
system_prompt_flag: ''
# inline | file
system_prompt_delivery: inline
# Optional fixed system prompt text; empty means role-provided
system_prompt: ⸢rev•system_prompt⸥
session_flag: ''
extra_args:
- --print
- --model
- haiku
# RoleDoc fields this runtime cannot honor
unsupported_role_fields:
- fallback_models
# e.g. system:deskops
tags:
- system:deskops
---

# runtime-claude-haiku-reviewer

## Summary

_Summarize what this runtime is and when to use it._



## Notes

_Operational notes such as authentication requirements or version pins._
