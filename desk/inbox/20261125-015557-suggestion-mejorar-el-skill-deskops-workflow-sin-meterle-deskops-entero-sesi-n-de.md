---
sldb:
  by: agent
  at: '2026-11-25T16:53:53Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-25T01:55:57'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-25T13:53:45'
# why the note was acknowledged; empty when no reason was given
ack_reason: triada en task-el-skill-deskops-workflow-pasa-a-un-nucleo-corto...
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Mejorar el skill deskops-workflow sin meterle deskops entero (sesión de

_Describe the incoming message with enough evidence to triage._

Mejorar el skill deskops-workflow sin meterle deskops entero (sesión de MEPU, 24/25-11). Evidencia: con el skill cargado igual se despachó con briefs a mano, se ofreció 'arreglar deskops' en vez de anotarlo en su inbox, se editó el repo de deskops desde MEPU (PR #12) y los preflight salían 'ambiguos' porque el contexto vivía en el prompt y no en la tarea. Faltas del skill: no menciona el ciclo (dispatch start executor/tester, queue, integrate, review preflight/bundle/dispose, closeout verify); para faltas de OTRA herramienta no dice --to <repo> (y en MEPU el destino deskops no está registrado: las notas quedaron 'PARA DESKOPS' en el inbox de MEPU); no dice 'no edites el repo de la herramienta'; nada de varias sesiones (modo pr toma el checkout compartido; quién puede disponer un review; motor de reviews sin saldo); desactualizado ('deskops status' es alias de doctor; dice jpcosec/opsys). Propuestas: (1) que el CLI mande: el skill dice 'en cada paso corre deskops next <tarea> y haz lo que diga', y cada error de gate trae el comando que lo resuelve; (2) skill núcleo de ~30 líneas + references/ cargadas por situación (dispatch, varias-sesiones, falta-en-una-herramienta, gates-y-reviews); (3) lo de cada repo (máquinas, CI, motores) en 'deskops faq --root .' o AGENTS.md, y el skill solo dice 'lee el faq del desk'; (4) el mapa de comandos generado desde --help/selfdoc con un test que lo compare con el CLI; (5) evals con los casos de hoy (falta en herramienta → inbox; despacha T → dispatch; gate pide preflight → correrlo, no aceptar sin leer). Y una pedida concreta de JP: 'deskops dispatch start <rol> --task <id> --only-prompt' que escriba el prompt.md (tarea + contexto + reglas de entrega del RoleDoc) sin lanzar scion, para que una sesión interactiva despache con sus propios subagentes pasándoles ese prompt en vez de un brief hecho a mano; el resto del ciclo (preflight, closeout, integrate) igual.
