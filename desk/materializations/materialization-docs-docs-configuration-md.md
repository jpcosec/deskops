---
sldb:
  by: agent
  at: '2026-11-20T13:43:46Z'
  authority: generated
  via: create_document
id: materialization-docs-docs-configuration-md
title: docs docs-configuration-md
source_atoms:
- atom-docs-configuration-md-explica-que-es-configuracion-en-deskops-y-como-se-declara-un-tipo-de-tarea
target_kind: docs
target_identity: docs/configuration.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_docs_recipes.py
tags:
- system:deskops
- topic:docs
---

# docs docs-configuration-md

## Intent

materializa en docs/configuration.md el atom atom-docs-configuration-md-explica-que-es-configuracion-en-deskops-y-como-se-declara-un-tipo-de-tarea
