---
sldb:
  by: agent
  at: '2026-11-16T23:13:16Z'
  authority: generated
  via: create_document
id: materialization-registro-de-comandos-declara-atoms-citations-como-mutante
title: Registro de comandos declara atoms citations como mutante
source_atoms:
- atom-un-archivo-de-codigo-cita-los-atomos-que-implementa-y-deskops-atoms-citations-lo-comprueba
target_kind: test
target_identity: tests/test_command_registry.py
validation:
- pytest -q tests/test_command_registry.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-un-archivo-de-codigo-cita-los-atomos-que-implementa-y-deskops-atoms-citations-lo-comprueba.md
---

# Registro de comandos declara atoms citations como mutante

## Intent

el conjunto MUTATING_COMMANDS del test lista atoms citations, que con --write escribe en el desk
