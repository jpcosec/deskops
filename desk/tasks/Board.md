---
sldb:
  by: agent
  at: '2026-11-16T02:03:50Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-deskops-status-deja-de-ser-solo-un-aviso-deprecated-y-entrega-el-estado-rapido-del-desk.md
- desk/tasks/task-doctor-dice-de-que-tarea-es-cada-cambio-sin-commitear-en-sldb-checkout-atrasado.md
- desk/tasks/task-supertareas-y-alta-en-lote-campo-parent-en-taskdoc-y-add-task-from-yaml-con-varias-tareas.md
- desk/tasks/task-rol-de-desk-hitl-about-faq-y-doctor-documentan-cada-carpeta-del-desk-y-doctor-avisa-si-hitl-tiene-ar.md
- desk/tasks/task-init-en-un-worktree-usa-el-nombre-del-repo-y-doctor-lee-el-pythonpath-del-store.md
- desk/tasks/task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada.md
- desk/tasks/task-board-no-refleja-deskops-edit-task-goal.md
- desk/tasks/task-advance-y-closeout-no-derraman-reglas-de-activacion-ni-runtimes-centrales-sin-trackear-en-el-desk-co.md
- desk/tasks/task-runtime-template-el-coordinador-lanza-hijos-con-el-harness-auth-del-template-default-oauth-token-no.md
# List of pill-xxx paths
pills:
- pill-001-task-closure-commit
- pill-005-subagent-execution
- pill-007-phase-gated-task-flow
- pill-durable-pill-knowledge-graduates-to-atoms-at-closeout
- pill-phase-closeout-reconciles-pills-and-surfaces-next-work
- pill-ready-phases-prove-dependencies-and-non-overlap
- pill-board-routed-pills-stay-minimal-and-reusable
# List of ritual-xxx paths
rituals:
- ritual-phase
- ritual-execution
- ritual-closeout
- ritual-testing
- context-review
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._

Route the active execution set for deskops.

## Notes

_Add short operational notes about the current routed set._

No active tasks routed.

## Task Details

_Generated from the task references above._

- deskops status deja de ser solo un aviso Deprecated y entrega el estado rapido del desk [draft] - deskops status imprime el estado rapido del desk (tareas activas, inbox abierto, alertas baratas) sin correr el doctor completo. La implementa V1 del frente velocidad-hooks (supervisor 15-11), no este desk por su cuenta; esta tarea la registra y se cierra con resolved-by cuando V1 entre.
- doctor dice de que tarea es cada cambio sin commitear en .sldb (checkout atrasado) [draft] - deskops doctor lista los cambios sin commitear bajo .sldb/ agrupados por la tarea (o el documento de desk) que los origino, y marca los que no tienen dueno.
- supertareas y alta en lote: campo parent en TaskDoc y add task --from-yaml con varias tareas [draft] - TaskDoc tiene un campo parent (id de otra tarea) que doctor y el tablero respetan, y deskops add task --from-yaml acepta una lista de tareas y las crea en una sola transaccion (todas o ninguna).
- rol de desk/hitl: about, faq y doctor documentan cada carpeta del desk y doctor avisa si hitl tiene archivos que no son para el humano [draft] - deskops about y deskops faq describen cada carpeta de desk/ (incluida hitl/), y doctor emite una alerta cuando desk/hitl contiene archivos que no son para el humano.
- init en un worktree usa el nombre del repo y doctor lee el pythonpath del store [draft] - deskops init en un worktree de git deriva project_identity del repo principal (git common dir o remoto), no de la carpeta; deskops doctor usa el pythonpath que declara el store.
- doctor no alerta como lost los recibos de una tarea cerrada [draft] - Un recibo cuya tarea se cerro (closeout registrado en git o en el store) no produce alerta lost en doctor: el closeout re-ancla los recibos al commit de cierre o los marca archivados; solo los recibos de tareas que desaparecieron sin cierre siguen alertando.
- Board no refleja deskops edit task goal [draft] - Reproducir en un desk real y corregir: tras deskops edit task <id> goal, la linea de la tarea en Task Details del Board muestra el goal nuevo, o hay un verbo de deskops que refresca el Board.
- advance y closeout no derraman reglas de activacion ni runtimes centrales sin trackear en el desk consumidor [draft] - Las semillas centrales (deskops/data/rules, runtime por defecto) se leen del paquete en tiempo de ejecucion, o se escriben solo por deskops desk update --apply y quedan trackeadas y declaradas; nunca como archivos sueltos sin trackear tras advance o closeout.
- runtime template: el coordinador lanza hijos con el harness-auth del template (default oauth-token), no api-key fijo [draft] - El auth de 'scion start' que arma deskops sale del template: scion_start_argv recibe harness_auth (validado contra HARNESS_AUTH_TYPES) y, sin valor, usa oauth-token, el mismo default que 'deskops runtime template' para claude (HARNESS_AUTH). El agents.md del coordinador escribe en los dos 'scion start' (executor y tester) el auth resuelto del template del coordinador (--harness-auth si se pasó; si no, el default del harness, oauth-token). RuntimeProfileDoc no tiene campo de auth: no se agrega en esta tarea.
