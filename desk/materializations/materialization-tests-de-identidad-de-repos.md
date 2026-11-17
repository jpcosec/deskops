---
sldb:
  by: agent
  at: '2026-11-17T11:57:13Z'
  authority: generated
  via: create_document
id: materialization-tests-de-identidad-de-repos
title: Tests de identidad de repos
source_atoms:
- atom-repo-register-accepts-explicit-path-and-registry-errors-name-the-fix
target_kind: test
target_identity: tests/test_repo_identity.py
validation:
- pytest -q tests/test_repo_identity.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-repo-register-accepts-explicit-path-and-registry-errors-name-the-fix.md
---

# Tests de identidad de repos

## Intent

verifica la identidad de repos y su resolución por el registro
