---
sldb:
  by: agent
  at: '2026-11-20T13:44:05Z'
  authority: generated
  via: create_document
id: materialization-docs-docs-workflow-policy-reference-md
title: docs docs-workflow-policy-reference-md
source_atoms:
- atom-docs-configuration-md-explica-que-es-configuracion-en-deskops-y-como-se-declara-un-tipo-de-tarea
target_kind: docs
target_identity: docs/workflow-policy-reference.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_docs_recipes.py
tags:
- system:deskops
- topic:docs
---

# docs docs-workflow-policy-reference-md

## Intent

materializa en docs/workflow-policy-reference.md el atom atom-docs-configuration-md-explica-que-es-configuracion-en-deskops-y-como-se-declara-un-tipo-de-tarea
