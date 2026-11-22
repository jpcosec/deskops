---
sldb:
  by: agent
  at: '2026-11-22T01:47:38Z'
  authority: generated
  via: save_document_payload
id: task-doctor-la-alerta-lost-restante-dice-como-repararla-sin-nombrar-desk-update-apply-y-su-test-cierra-co
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- deskops/doctor_findings.py
- tests/test_doctor_lost_receipts.py
- 0b00985e1389d3b9440b3cf05b674e1f8bbb9bce
depends_on: []
pills: []
files:
- CHANGELOG.md
- deskops/doctor_findings.py
- tests/test_doctor_lost_receipts.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-la-alerta-lost-de-doctor-nombra-el-remedio-real
---

# doctor: la alerta lost restante dice cómo repararla sin nombrar desk update --apply, y su test cierra con closeout commit real

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-22: la tarea 'doctor no alerta como lost los recibos de una tarea cerrada' agotó sus dos intentos de tester. El intento 2 (91f44d0d) arregla lo central: closed_task_ids reconoce el asunto 'closeout: <task-id>', y en IR las alertas lost bajan de 83 a 0. El tester deskops-t-ce3a6e33bbbc-a2 dejó dos criterios sin cumplir. (1) La sección de recibos lost sigue imprimiendo "deskops desk update --apply does not repair these. Restore the task, or close it with deskops closeout commit ...", y el test fija 'does not repair these'. El Done When pide no nombrar desk update --apply salvo que ese comando repare la alerta. (2) Los tests usan commits sintéticos (git commit --allow-empty) en vez de cerrar una tarea con deskops closeout commit.

## Goal

_Describe the concrete result this task must produce._

La alerta lost restante (tarea borrada sin closeout) dice: 'the task was deleted without closeout: restore it from git or close it with deskops closeout resolved-by', sin mencionar desk update --apply. El pie 'register ... with: deskops desk update --apply' solo se imprime si queda alguna alerta que ese comando sí registre. Un test cierra una tarea real con deskops closeout commit en un desk temporal y comprueba que doctor no da alertas lost de sus recibos. Los tests de tests/test_doctor_lost_receipts.py dejan de fijar el texto viejo.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/cli/commands/doctor.py, deskops/doctor_findings.py, tests/test_doctor_lost_receipts.py y CHANGELOG. Fuera: closed_task_ids (ya correcto).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: cambiar el texto de la sección lost y condicionar el pie de desk update --apply. p2: test con closeout real en desk temporal (deskops init, add task, closeout commit) y doctor sin lost. p3: actualizar los asserts del texto viejo. p4: correr tests/test_doctor_*.py, y deskops doctor --root /mnt/ssd/proyectos/SLDB_1/IR (solo lectura) sin lost; anotarlo en el run dir. p5: suite completa con -n 4 (instalar pytest-xdist si falta). p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_doctor_lost_receipts.py tests/test_doctor_alerts.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_doctor_*.py pasan, el texto de la alerta lost ya no nombra desk update --apply y hay un test con closeout commit real.
