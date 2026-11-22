---
sldb:
  by: agent
  at: '2026-11-22T21:15:05Z'
  authority: generated
  via: create_document
id: materialization-atoms-oms-atom-desk-health-delegates-store-diagnostics-to-sldb-md
title: atoms oms-atom-desk-health-delegates-store-diagnostics-to-sldb-md
source_atoms:
- atom-los-4-atomos-de-salud-del-desk-dejan-de-dar-ruido-estructural-en-sldb-stores-check
target_kind: docs
target_identity: desk/atoms/atom-desk-health-delegates-store-diagnostics-to-sldb.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_atom_tags.py tests/test_atoms_cli.py
tags:
- system:deskops
- topic:atoms
---

# atoms oms-atom-desk-health-delegates-store-diagnostics-to-sldb-md

## Intent

materializa en desk/atoms/atom-desk-health-delegates-store-diagnostics-to-sldb.md el atom atom-los-4-atomos-de-salud-del-desk-dejan-de-dar-ruido-estructural-en-sldb-stores-check
