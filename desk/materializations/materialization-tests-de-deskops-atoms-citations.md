---
sldb:
  by: agent
  at: '2026-11-16T22:30:30Z'
  authority: generated
  via: create_document
id: materialization-tests-de-deskops-atoms-citations
title: Tests de deskops atoms citations
source_atoms:
- atom-un-archivo-de-codigo-cita-los-atomos-que-implementa-y-deskops-atoms-citations-lo-comprueba
target_kind: test
target_identity: tests/test_atom_citations.py
validation:
- pytest -q tests/test_atom_citations.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-un-archivo-de-codigo-cita-los-atomos-que-implementa-y-deskops-atoms-citations-lo-comprueba.md
---

# Tests de deskops atoms citations

## Intent

verifica la gramatica de citas, --check, --write idempotente y Cited by: en desks sandbox
