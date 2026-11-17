---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T22:13:18'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Restos del retiro del alias deskops inbox

_Describe the incoming message with enough evidence to triage._

Seguimiento de task-retirar-el-alias-deskops-inbox (8667e8f1, closeout 49465a27): (1) deskops/cli/commands/message.py: _run_legacy y su docstring quedan como código muerto (solo los alcanza deskops message sin subcomando); retirarlos. (2) tests/e2e_agent/scenarios/inbox-to-task.yaml: la rama 'deskops inbox list --root .' ahora falla y cae al ||; cambiarla a 'deskops message list --root .'. (3) Docstrings históricos que nombran deskops inbox: tests/test_repo_identity.py y tests/test_inbox_promote_cli_gaps.py.
