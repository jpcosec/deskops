---
sldb:
  by: agent
  at: '2026-11-20T13:44:14Z'
  authority: generated
  via: create_document
id: materialization-docs-tests-test-docs-recipes-py
title: docs tests-test_docs_recipes-py
source_atoms:
- atom-docs-configuration-md-explica-que-es-configuracion-en-deskops-y-como-se-declara-un-tipo-de-tarea
target_kind: test
target_identity: tests/test_docs_recipes.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_docs_recipes.py
tags:
- system:deskops
- topic:docs
---

# docs tests-test_docs_recipes-py

## Intent

materializa en tests/test_docs_recipes.py el atom atom-docs-configuration-md-explica-que-es-configuracion-en-deskops-y-como-se-declara-un-tipo-de-tarea
