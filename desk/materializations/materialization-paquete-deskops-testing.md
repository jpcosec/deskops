---
sldb:
  by: agent
  at: '2026-11-16T17:17:48Z'
  authority: generated
  via: create_document
id: materialization-paquete-deskops-testing
title: Paquete deskops.testing
source_atoms:
- atom-un-repo-con-tests-en-otro-lenguaje-declara-su-evidencia-de-closeout-con-un-test-py-que-corre-la-suit
target_kind: code
target_identity: deskops/testing/__init__.py
validation:
- pytest -q tests/test_foreign_suites.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-un-repo-con-tests-en-otro-lenguaje-declara-su-evidencia-de-closeout-con-un-test-py-que-corre-la-suit.md
---

# Paquete deskops.testing

## Intent

declara el paquete deskops.testing donde vive el puente de pytest
