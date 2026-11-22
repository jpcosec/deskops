---
sldb:
  by: agent
  at: '2026-11-22T21:15:16Z'
  authority: generated
  via: create_document
id: materialization-atoms-sk-atoms-atom-desk-health-is-measured-by-cli-diagnostics-md
title: atoms sk-atoms-atom-desk-health-is-measured-by-cli-diagnostics-md
source_atoms:
- atom-los-4-atomos-de-salud-del-desk-dejan-de-dar-ruido-estructural-en-sldb-stores-check
target_kind: docs
target_identity: desk/atoms/atom-desk-health-is-measured-by-cli-diagnostics.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_atom_tags.py tests/test_atoms_cli.py
tags:
- system:deskops
- topic:atoms
---

# atoms sk-atoms-atom-desk-health-is-measured-by-cli-diagnostics-md

## Intent

materializa en desk/atoms/atom-desk-health-is-measured-by-cli-diagnostics.md el atom atom-los-4-atomos-de-salud-del-desk-dejan-de-dar-ruido-estructural-en-sldb-stores-check
