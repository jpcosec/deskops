---
sldb:
  by: agent
  at: '2026-11-20T18:18:04Z'
  authority: generated
  via: create_document
id: materialization-dispatch-tests-test-dispatch-py
title: dispatch tests-test_dispatch-py
source_atoms:
- atom-cada-ejecutor-de-dispatch-trabaja-en-su-propio-git-worktree-y-reap-integra-su-rama
target_kind: test
target_identity: tests/test_dispatch.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py
tags:
- system:deskops
- topic:dispatch
---

# dispatch tests-test_dispatch-py

## Intent

materializa en tests/test_dispatch.py el atom atom-cada-ejecutor-de-dispatch-trabaja-en-su-propio-git-worktree-y-reap-integra-su-rama
