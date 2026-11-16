---
sldb:
  by: agent
  at: '2026-11-16T17:16:50Z'
  authority: generated
  via: create_document
id: materialization-tests-del-puente-de-pytest
title: Tests del puente de pytest
source_atoms:
- atom-un-repo-con-tests-en-otro-lenguaje-declara-su-evidencia-de-closeout-con-un-test-py-que-corre-la-suit
target_kind: test
target_identity: tests/test_foreign_suites.py
validation:
- pytest -q tests/test_foreign_suites.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-un-repo-con-tests-en-otro-lenguaje-declara-su-evidencia-de-closeout-con-un-test-py-que-corre-la-suit.md
---

# Tests del puente de pytest

## Intent

verifica el contrato de run_foreign_suite y que closeout verify toma el .py del puente como evidencia de tests
