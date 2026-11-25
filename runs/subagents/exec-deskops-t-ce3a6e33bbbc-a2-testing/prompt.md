Task: task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada
Title: doctor no alerta como lost los recibos de una tarea cerrada
Status: active
Current node: ritual-testing
Task type: task.code
From drawer: desk/drawer/tasks/task-doctor-los-recibos-de-una-tarea-cerrada-quedan-como-alerta-lost.md
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-21T23:57:34Z'
  authority: generated
  via: save_document_payload
id: task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
history:
- task_activates
- 'task_returns_to_execution: Tester deskops-t-ce3a6e33bbbc FALLA sobre c0df7045.
  closed_task_ids() en deskops/doctor_findings.py solo considera cerrada una tarea
  si hay un commit con Task-Id y además el trailer Closeout-Mode o Run-Id. No reconoce
  el cierre por el asunto canónico ''closeout: <task-id>'' que escribe deskops closeout
  commit. Sobre los desks reales, IR sigue con 83 alertas ''lost'', 81 de ellas de
  tareas con un commit de asunto exacto ''closeout: <task-id>'' (ejemplo: task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents,
  commit 89404705). Intento 2: closed_task_ids también cuenta como cerrada una tarea
  con un commit cuyo asunto es exactamente ''closeout: <task-id>'' (git log --format=%s,
  comparando el id completo, sin prefijos). Agregar un test con un repo temporal donde
  el cierre solo está en el asunto. Verificar sobre /mnt/ssd/proyectos/SLDB_1/IR (solo
  lectura): deskops doctor --root /mnt/ssd/proyectos/SLDB_1/IR no da alertas lost
  de tareas con commit ''closeout:''; anotar el conteo antes y después en el run dir.
  Correr tests/test_doctor_*.py. Commit desde tu worktree con ''git commit -- <rutas>''
  y el trailer Task-Id.'
- task_activates
references:
- desk/inbox/20261121-032540-unclear-doctor-alertas-subject-lost-de-revisiones-de-tareas-cerradas-que-desk-update-no-repara.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-doctor-los-recibos-de-una-tarea-cerrada-quedan-como-alerta-lost.md
---

# doctor no alerta como lost los recibos de una tarea cerrada

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de ftcourier (14-11, inbox 20261114-022915): al cerrar con closeout commit o resolved-by se borra la tarea y sus ReviewDoc quedan con sujeto 'lost'; doctor muestra una alerta por recibo para siempre (10 en FTC-25 y FTC-27). Los recibos son auditoria y no se borran.

## Goal

_Describe the concrete result this task must produce._

Un recibo cuya tarea se cerro (closeout registrado en git o en el store) no produce alerta lost en doctor: el closeout re-ancla los recibos al commit de cierre o los marca archivados; solo los recibos de tareas que desaparecieron sin cierre siguen alertando. Los recibos lost ya existentes de tareas cerradas (p. ej. ~107 en el desk de IR, inbox 20261121-032540) dejan de alertar sin intervencion manual, y el texto de la alerta de doctor nombra un comando que de verdad la resuelve: hoy sugiere deskops desk update --apply, que responde 'Desk is up to date' sin reparar nada.

## Scope

_State what is in scope and what is out of scope._

deskops/services/closure.py (closeout commit y resolved-by), deskops doctor, deskops/models/review.py; el estado del ancla lo da sldb, deskops no recalcula anclas.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- test nuevo de deskops (nombre a fijar al promover) con closeout real y doctor

## Done When

_Name the observable condition that makes the task complete._

test: cerrar una tarea con recibos preflight/bundle y correr doctor no da alertas lost; borrar una tarea sin cierre si las da; un recibo lost preexistente de una tarea con closeout en git no alerta; el mensaje de la alerta restante no menciona desk update --apply salvo que ese comando la repare.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.
