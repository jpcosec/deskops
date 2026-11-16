---
sldb:
  by: agent
  at: '2026-11-16T17:17:42Z'
  authority: generated
  via: save_document_payload
id: materialization-puente-de-pytest-deskops-testing
title: Puente de pytest deskops.testing
source_atoms:
- atom-un-repo-con-tests-en-otro-lenguaje-declara-su-evidencia-de-closeout-con-un-test-py-que-corre-la-suit
target_kind: code
target_identity: deskops/testing/foreign_suites.py
validation:
- pytest -q tests/test_foreign_suites.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-un-repo-con-tests-en-otro-lenguaje-declara-su-evidencia-de-closeout-con-un-test-py-que-corre-la-suit.md
---

# Puente de pytest deskops.testing

## Intent

materializa atom-un-repo-con-tests-en-otro-lenguaje-declara-su-evidencia-de-closeout-con-un-test-py-que-corre-la-suit en el paquete deskops/testing (run_foreign_suite, VITEST, GO_TEST)
