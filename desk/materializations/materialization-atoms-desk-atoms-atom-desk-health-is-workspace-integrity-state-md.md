---
sldb:
  by: agent
  at: '2026-11-22T21:15:27Z'
  authority: generated
  via: create_document
id: materialization-atoms-desk-atoms-atom-desk-health-is-workspace-integrity-state-md
title: atoms desk-atoms-atom-desk-health-is-workspace-integrity-state-md
source_atoms:
- atom-los-4-atomos-de-salud-del-desk-dejan-de-dar-ruido-estructural-en-sldb-stores-check
target_kind: docs
target_identity: desk/atoms/atom-desk-health-is-workspace-integrity-state.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_atom_tags.py tests/test_atoms_cli.py
tags:
- system:deskops
- topic:atoms
---

# atoms desk-atoms-atom-desk-health-is-workspace-integrity-state-md

## Intent

materializa en desk/atoms/atom-desk-health-is-workspace-integrity-state.md el atom atom-los-4-atomos-de-salud-del-desk-dejan-de-dar-ruido-estructural-en-sldb-stores-check
