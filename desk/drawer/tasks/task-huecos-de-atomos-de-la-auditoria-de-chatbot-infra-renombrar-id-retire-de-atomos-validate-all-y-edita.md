---
sldb:
  by: agent
  at: '2026-11-24T18:28:53Z'
  authority: generated
  via: save_document_payload
id: task-huecos-de-atomos-de-la-auditoria-de-chatbot-infra-renombrar-id-retire-de-atomos-validate-all-y-edita
status: deferred
summary: ''
tags:
- host:robocop2
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

Entra: deskops/services/atoms.py, deskops/cli/registry.py, deskops/cli/commands/doctor.py y tests. Un desk sandbox por hueco. No entra: citas codigo->atomo (otra tarea), repos de AntonIA. Precisiones del preflight 1: contrato de rename: deskops atoms rename <id> <nuevo-id> --root . reescribe con sldb rewrite_references todas las referencias entrantes (campos atoms y references de tareas, source_atoms de materializations, menciones atom-* en prosa que sldb trate como MentionPattern) y renombra el archivo, en una transaccion; si <nuevo-id> existe, error sin escribir; el nuevo id cumple ^atom-[a-z0-9-]+$. Retiro: verbo nuevo deskops atoms retire <id> --reason <texto> --root . que falla si el atomo tiene referencias entrantes (no se toca closeout retire). Reproducciones: (4) deskops atoms validate --all --root . en el desk de deskops y contar los hallazgos de provenance; (5) intentar editar desk/contexts/pills.md con deskops (no hay verbo) y registrarlo; (6) copiar un desk con store enlazado a deskops a otra profundidad de directorio en /dev/shm y correr deskops doctor. Desk sandbox = directorio en /dev/shm con git init y deskops init, borrado al terminar. Cada hueco corregido suma su test en el archivo de tests que corresponda (test_atom_materialization.py para rename y retire, test_doctor*.py para el 6).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Reproducir cada hueco en un sandbox y registrar `deskops review record <tarea> --kind reproduction`. 2) Corregir los que se reproducen, uno por commit. 3) Tests por hueco.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_atom_materialization.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_help_examples.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Cada hueco tiene su reproduccion registrada y, si se reprodujo, su test verde.
