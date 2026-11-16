---
sldb:
  by: agent
  at: '2026-11-16T04:15:07Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: scion
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:51:44'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T01:15:04'
---

# closeout: el gate de tests solo acepta .py y el de commit solo el repo del desk; tareas Go/bash o con código en otro repo no pueden cerrar

_Describe the incoming message with enough evidence to triage._

Triaje del desk de scion (2026-11-16). Tres tareas de la fase 0 del piloto scion están hechas y verificadas (reports/scion-piloto-ir-20261115.md) pero closeout commit --no-run las bloquea: (1) task-fase-0-ir-scion-build-pasa-el-contexto-por-stdin-el-docker-snap-no-lee-scion: el código y su test son Go (cmd/build_context_test.go, commit f6e623c69 en scion); reference_points_to_test en deskops/services/closeout_gates.py exige sufijo .py, así que missing_tests_evidence aunque el test esté en files y references. (2) task-fase-0-ir-hook-pre-start-deskops-tools-instala-sldb-y-deskops-editables-desde-workspace: script bash (hooks/pre-start-deskops.sh), validado con docker run; no hay forma de declarar ese test. (3) task-fase-0-ir-template-del-ejecutor-de-ir-con-tmp-en-ram-lock-de-tests-compartido-y-tope-de-memoria: vive en el desk de scion pero su código entró en deskops (4a7707a5, 4c745c18, 881e177a) e IR (5b8ce32); reference_points_to_commit solo resuelve ancestros del repo del desk y los tests están en deskops/tests, fuera del root. resolved-by también exige .py. Pedido: que el gate de tests acepte tests de otros lenguajes (al menos _test.go y un comando de validación con log en runs/) y evidencia de commit de otro repo registrado (repo:sha). Las tres quedan en draft con references cargadas hasta entonces. Detalles menores del mismo triaje: (a) closeout verify escribe recibos evidence (ReviewDoc y desk/reviews) aunque su ayuda dice que solo chequea; (b) un --reason con llaves en closeout commit imprime Missing required field (parece str.format) después de hacer el commit y deja sin commitear la proyección desk/reviews/<tarea>/evidence-external-2.md; (c) deskops edit task y deskops message send fallan con TemplateSyntaxError si el valor trae dos llaves de apertura seguidas (por ejemplo un docker inspect --format de Go) o ciertas comillas cerca de ellas: el texto se pasa por Jinja.
