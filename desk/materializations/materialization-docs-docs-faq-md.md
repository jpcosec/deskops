---
sldb:
  by: agent
  at: '2026-11-20T13:43:55Z'
  authority: generated
  via: create_document
id: materialization-docs-docs-faq-md
title: docs docs-faq-md
source_atoms:
- atom-docs-configuration-md-explica-que-es-configuracion-en-deskops-y-como-se-declara-un-tipo-de-tarea
target_kind: docs
target_identity: docs/faq.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_docs_recipes.py
tags:
- system:deskops
- topic:docs
---

# docs docs-faq-md

## Intent

materializa en docs/faq.md el atom atom-docs-configuration-md-explica-que-es-configuracion-en-deskops-y-como-se-declara-un-tipo-de-tarea
