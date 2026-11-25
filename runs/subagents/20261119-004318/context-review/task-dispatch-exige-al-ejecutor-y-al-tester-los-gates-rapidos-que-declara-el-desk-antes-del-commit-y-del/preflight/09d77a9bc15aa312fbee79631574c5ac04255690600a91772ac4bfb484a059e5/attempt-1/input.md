FILE:desk/tasks/task-dispatch-exige-al-ejecutor-y-al-tester-los-gates-rapidos-que-declara-el-desk-antes-del-commit-y-del.md
---
sldb:
  by: agent
  at: '2026-11-19T00:42:56Z'
  authority: generated
  via: create_document
id: task-dispatch-exige-al-ejecutor-y-al-tester-los-gates-rapidos-que-declara-el-desk-antes-del-commit-y-del
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# dispatch exige al ejecutor y al tester los gates rápidos que declara el desk antes del commit y del veredicto

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261118-210137-suggestion-dispatch-el-ejecutor-y-el-tester-no-corren-los-gates-estructurales-del-proyecto-y-integrate-es-el-primero-en-verlos. Dos veces (sldb e7cc3761 el 17-11 y 73df19ec el 18-11) el ejecutor y el tester dieron por buena una entrega que la suite completa de integrate rechazó por gates estructurales (tests/test_clean_code_rules.py: funciones de más de 10 líneas de lógica, archivos de más de 80 líneas efectivas), porque solo corren los tests de los archivos tocados. El coordinador tuvo que arreglarlo a mano después del cierre.

## Goal

_Describe the concrete result this task must produce._

Un desk puede declarar en desk/config.json, bloque dispatch, un campo opcional quick_gates (argv). Si lo declara, el prompt.md que escribe dispatch start para el ejecutor exige correrlo con rc 0 antes del commit, y el del tester antes del veredicto (un FALLA si da distinto de 0). Sin el campo, el prompt no cambia.

## Scope

_State what is in scope and what is out of scope._

Dentro: DispatchConfig (deskops/config.py) con quick_gates opcional; los textos de prompt.md por rol en deskops/dispatch.py; tests en tests/test_dispatch.py; docs/operator-manual.md (sección de dispatch); CHANGELOG. Los quick_gates corren con el python del venv del contenedor (/tmp/ws-venv, del paso 'Python environment (run first)' de b6f8e0f5). Fuera: el config real de los desks; el integrador declara después quick_gates en sldb (bash tools/check.sh --fast) y en deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: con quick_gates en el config de un desk de prueba, el prompt.md del executor y el del tester contienen el comando y la regla (rc 0 antes del commit / FALLA si no). Sin el campo, el prompt no lo menciona. p2: implementar en DispatchConfig y en el armado de prompt.md. p3: docs y CHANGELOG. p4: commit con rutas nombradas y Task-Id, sin push.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan y la suite completa de deskops pasa (la corre integrate).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-dispatch-exige-al-ejecutor-y-al-tester-los-gates-rapidos-que-declara-el-desk-antes-del-commit-y-del: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

