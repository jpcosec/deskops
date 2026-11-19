---
sldb:
  by: agent
  at: '2026-11-19T14:54:45Z'
  authority: generated
  via: create_document
id: materialization-verify-directorio-nodo-closure
title: verify directorio nodo closure
source_atoms:
- atom-closeout-verify-cubre-los-archivos-bajo-un-directorio-target-sea-nodo-del-grafo-o-missing
target_kind: code
target_identity: deskops/services/closure.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_materialization_targets_outside_package.py
tags:
- system:deskops
- topic:closeout
---

# verify directorio nodo closure

## Intent

materializa en deskops/services/closure.py el atom atom-closeout-verify-cubre-los-archivos-bajo-un-directorio-target-sea-nodo-del-grafo-o-missing
