FILE:desk/tasks/task-deskops-atoms-citations-queda-declarado-como-comando-que-modifica-en-el-test-del-registro-de-comando.md
---
sldb:
  by: agent
  at: '2026-11-16T23:00:31Z'
  authority: generated
  via: create_document
id: task-deskops-atoms-citations-queda-declarado-como-comando-que-modifica-en-el-test-del-registro-de-comando
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
- tests/test_command_registry.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-un-archivo-de-codigo-cita-los-atomos-que-implementa-y-deskops-atoms-citations-lo-comprueba
---

# deskops atoms citations queda declarado como comando que modifica en el test del registro de comandos

## Rationale

_Explain why this task exists or the business driver behind it._

La integracion de wA:p1 sobre 12c5c2ce dio 1113 passed y 1 failed: tests/test_command_registry.py::test_mutating_commands_are_declared_explicitly. La tarea de atoms citations (996becef, closeout 8b0aae02) agrego el comando deskops atoms citations, que con --write crea y borra RelationDoc en el desk; su entrada en deskops/cli/registry.py ya lleva mutates=True, pero el conjunto esperado MUTATING_COMMANDS del test no lo lista, y el test compara igualdad exacta.

## Goal

_Describe the concrete result this task must produce._

tests/test_command_registry.py pasa: ('atoms', 'citations') esta en MUTATING_COMMANDS junto a los demas subcomandos de atoms que modifican, y la entrada del registro sigue declarando mutates=True.

## Scope

_State what is in scope and what is out of scope._

Entra: agregar la tupla ('atoms', 'citations') al conjunto MUTATING_COMMANDS de tests/test_command_registry.py, en el bloque de los subcomandos de atoms. Sale: deskops/cli/registry.py (ya declara mutates=True; solo se lee para confirmarlo), el comportamiento del comando y cualquier otro test.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr tests/test_command_registry.py y confirmar que la unica falla es ('atoms', 'citations'). 2) Confirmar en deskops/cli/registry.py que la entrada path=('atoms', 'citations') tiene mutates=True. 3) Agregar la tupla a MUTATING_COMMANDS. 4) Correr la Validation.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_command_registry.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_atom_citations.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_command_registry.py y tests/test_atom_citations.py pasan y git diff solo toca tests/test_command_registry.py.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-atoms-citations-queda-declarado-como-comando-que-modifica-en-el-test-del-registro-de-comando: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

