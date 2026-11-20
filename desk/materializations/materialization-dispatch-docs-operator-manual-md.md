---
sldb:
  by: agent
  at: '2026-11-20T18:17:55Z'
  authority: generated
  via: create_document
id: materialization-dispatch-docs-operator-manual-md
title: dispatch docs-operator-manual-md
source_atoms:
- atom-cada-ejecutor-de-dispatch-trabaja-en-su-propio-git-worktree-y-reap-integra-su-rama
target_kind: docs
target_identity: docs/operator-manual.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py
tags:
- system:deskops
- topic:dispatch
---

# dispatch docs-operator-manual-md

## Intent

materializa en docs/operator-manual.md el atom atom-cada-ejecutor-de-dispatch-trabaja-en-su-propio-git-worktree-y-reap-integra-su-rama
