---
sldb:
  by: agent
  at: '2026-11-23T19:18:33Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-23T16:13:32'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T16:18:21'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'aplicada: se separo en tres tareas con dependencia: task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase
  (Board con fases) -> task-integrate-por-lote-una-sola-integracion-por-desk-con-todo-lo-cerrado-pendiente-un-tip-una-suite-un-g
  (integrate por fase, ajustada) -> task-el-skill-deskops-workflow-y-vocabulary-md-explican-que-la-suite-completa-y-el-push-son-de-la-fase-y
  (skill y vocabulary)'
# conversation thread/message the note came from, e.g. #hilo/1234
---

# JP: el lote de integración es la fase del DAG declarada en el Board; falta en la herramienta y en el skill

_Describe the incoming message with enough evidence to triage._

Precisión de JP (2026-11-23) a la nota 20261123-160333 y a la tarea task-integrate-por-lote-...: 'eso de las integraciones en lote debería ser parte de lo que está considerado en el board al crear las fases del DAG'. Es decir, el lote no es 'todo lo cerrado que haya pendiente' sino la fase: la capa de dependencias que se declara al descomponer el DAG. Lo que hay hoy (verificado por el supervisor): (a) el ritual ritual-phase ya lo dice: cada tarea cierra con su validación dirigida, y al cerrar todas las de la fase se corre la validación de integración de la capa combinada y un commit de cierre de fase; (b) la herramienta lo contradice: el trabajo de cola 'integrate' de desk/config.json corre 'deskops integrate --task-from-env', una integración con suite completa por tarea; (c) el Board no registra fases: solo lista rituales y pills (ritual-phase, pill-007-phase-gated-task-flow), no qué tareas forman cada fase ni cuál es su integración; (d) el skill deskops-workflow (.claude/skills/deskops-workflow) no lo explica: SKILL.md no menciona integración por fase y references/vocabulary.md define fase solo como capa de dependencias. Pedido: 1) que las fases del DAG queden declaradas en el Board al crearlas (qué tareas, y que la integración es de la fase); 2) que integrate tome como unidad la fase del Board, no la tarea; 3) actualizar SKILL.md y vocabulary.md para que un agente sepa que la suite completa y el push son de la fase y cada tarea solo corre su validación dirigida. Ajustar la tarea de integrate por lote a esto antes de despacharla.
