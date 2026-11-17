---
sldb:
  by: agent
  at: '2026-11-17T11:57:04Z'
  authority: generated
  via: create_document
id: materialization-tests-de-robustez-del-registro-de-repos
title: Tests de robustez del registro de repos
source_atoms:
- atom-repo-register-accepts-explicit-path-and-registry-errors-name-the-fix
target_kind: test
target_identity: tests/test_registry_robustness.py
validation:
- pytest -q tests/test_registry_robustness.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-repo-register-accepts-explicit-path-and-registry-errors-name-the-fix.md
---

# Tests de robustez del registro de repos

## Intent

verifica rutas relativas en repo register, entradas viejas y alertas de doctor por entradas que no resuelven
