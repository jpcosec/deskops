FILE:desk/tasks/task-huecos-de-atomos-de-la-auditoria-de-chatbot-infra-renombrar-id-retire-de-atomos-validate-all-y-edita.md
---
sldb:
  by: agent
  at: '2026-11-16T04:02:10Z'
  authority: generated
  via: save_document_payload
id: task-huecos-de-atomos-de-la-auditoria-de-chatbot-infra-renombrar-id-retire-de-atomos-validate-all-y-edita
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/tasks/task-chatbot-infra-indexar-las-citas-c-digo-atom-de-los-docstrings-en-el-grafo-y-huecos-de-atoms-vistos-en-la-auditor-a.md
depends_on: []
pills:
- desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md
files:
- deskops/services/atoms.py
- deskops/cli/registry.py
- deskops/cli/commands/doctor.py
- tests/test_atom_materialization.py
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# Huecos de atomos de la auditoria de Chatbot_Infra: renombrar id, retire de atomos, validate --all y editar contexts/pills.md

## Rationale

_Explain why this task exists or the business driver behind it._

Mismo item del drawer (Chatbot_Infra, 2026-10-21), huecos 1, 3, 4, 5 y 6. Verificado el 2026-11-16: no hay verbo para renombrar el id de un atomo (el id sale del titulo y retitular rompe citas y tareas); `deskops closeout retire` no acepta atomos (deskops/cli/registry.py:964). Sin verificar: 'atoms validate --all' marca toda la provenance como no resoluble (falso positivo masivo); no hay verbo para editar desk/contexts/pills.md; rutas relativas en .sldb/core/store_index.yaml y RelationDoc al store de deskops rompen doctor ('linked store is missing') al mover el workspace. El hueco 2 (atoms merge no reescribe tasks) se resolvio en CC35c (8c583005) y el 7 (remitente no registrado) en fd89078f.

## Goal

_Describe the concrete result this task must produce._

Para cada hueco 1, 3, 4, 5 y 6: un recibo de reproduccion (o la constancia de que no se reproduce, con el comando y la salida) y, si se reproduce, la correccion con test: (1) `deskops atoms rename <id> <nuevo-id>` que reescribe referrers con la API de sldb; (3) retire acepta atomos o hay un verbo de retiro de atomos; (4) validate --all sin falsos positivos; (5) contexts/pills.md editable por un verbo de deskops; (6) doctor resuelve el store enlazado de deskops aunque se mueva el workspace.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/atoms.py, deskops/cli/registry.py, deskops/cli/commands/doctor.py y tests. Un desk sandbox por hueco. No entra: citas codigo->atomo (otra tarea), repos de AntonIA.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reproducir cada hueco en un sandbox y registrar `deskops review record <tarea> --kind reproduction`. 2) Corregir los que se reproducen, uno por commit. 3) Tests por hueco.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_atom_materialization.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_help_examples.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

Cada hueco tiene su reproduccion registrada y, si se reprodujo, su test verde.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-huecos-de-atomos-de-la-auditoria-de-chatbot-infra-renombrar-id-retire-de-atomos-validate-all-y-edita: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

