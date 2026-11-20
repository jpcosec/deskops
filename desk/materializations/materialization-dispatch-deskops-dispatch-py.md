---
sldb:
  by: agent
  at: '2026-11-20T18:17:46Z'
  authority: generated
  via: create_document
id: materialization-dispatch-deskops-dispatch-py
title: dispatch deskops-dispatch-py
source_atoms:
- atom-cada-ejecutor-de-dispatch-trabaja-en-su-propio-git-worktree-y-reap-integra-su-rama
target_kind: code
target_identity: deskops/dispatch.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py
tags:
- system:deskops
- topic:dispatch
---

# dispatch deskops-dispatch-py

## Intent

materializa en deskops/dispatch.py el atom atom-cada-ejecutor-de-dispatch-trabaja-en-su-propio-git-worktree-y-reap-integra-su-rama
