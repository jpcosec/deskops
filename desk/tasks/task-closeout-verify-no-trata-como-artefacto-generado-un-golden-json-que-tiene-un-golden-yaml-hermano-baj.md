---
sldb:
  by: agent
  at: '2026-11-17T13:34:18Z'
  authority: generated
  via: create_document
id: task-closeout-verify-no-trata-como-artefacto-generado-un-golden-json-que-tiene-un-golden-yaml-hermano-baj
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/services/closure.py
- tests/test_closeout_declared_evidence.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# closeout verify no trata como artefacto generado un golden json que tiene un golden yaml hermano bajo tests/fixtures

## Rationale

_Explain why this task exists or the business driver behind it._

Al cerrar la tarea de ack --reason (97649c61), closeout verify dio generated_artifact_missing_declared_sources para tests/fixtures/golden/output/message_ack.json y message_read.json: _generated_artifact_source_finding en deskops/services/closure.py (alrededor de la linea 1583) trata un .json o .md con un .yaml, .yml o .mmd hermano como proyeccion renderizada que debe declarar source_atoms o provenance. Bajo tests/fixtures/golden/output/ el json y el yaml son dos goldens independientes (la misma salida en dos formatos), no uno generado del otro, y un golden no puede llevar provenance sin cambiar su contenido. El hallazgo bloquea el gate atom|materialization del cierre.

## Goal

_Describe the concrete result this task must produce._

closeout verify no da generated_artifact_missing_declared_sources para archivos bajo tests/fixtures/ (goldens y fixtures de test); fuera de tests/fixtures/ el chequeo sigue igual.

## Scope

_State what is in scope and what is out of scope._

Entra: _generated_artifact_source_finding (o _find_generated_artifact_source_sibling) en deskops/services/closure.py y tests en tests/test_closeout_declared_evidence.py. Sale: la regla para docs, diagramas y artefactos fuera de tests/fixtures/.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer _generated_artifact_source_finding y donde se llama. 2) Excluir las rutas bajo tests/fixtures/. 3) Tests en desk sandbox (tmp_path): un par json/yaml bajo tests/fixtures/golden/output/ en files de la tarea no da el hallazgo; un .md con un .yaml hermano fuera de tests/fixtures/ lo sigue dando.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos pasan (golden bajo tests/fixtures sin hallazgo; artefacto fuera de tests/fixtures con hallazgo) y los dos archivos de la Validation pasan.
