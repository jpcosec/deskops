---
sldb:
  by: agent
  at: '2026-11-20T13:43:36Z'
  authority: generated
  via: create_document
id: materialization-docs-deskops-data-faq-md
title: docs deskops-data-faq-md
source_atoms:
- atom-docs-configuration-md-explica-que-es-configuracion-en-deskops-y-como-se-declara-un-tipo-de-tarea
target_kind: docs
target_identity: deskops/data/faq.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_docs_recipes.py
tags:
- system:deskops
- topic:docs
---

# docs deskops-data-faq-md

## Intent

materializa en deskops/data/faq.md el atom atom-docs-configuration-md-explica-que-es-configuracion-en-deskops-y-como-se-declara-un-tipo-de-tarea
