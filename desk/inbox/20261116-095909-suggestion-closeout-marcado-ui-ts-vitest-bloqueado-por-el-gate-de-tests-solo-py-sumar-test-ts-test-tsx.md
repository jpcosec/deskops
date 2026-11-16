---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: marcado-ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T09:59:09'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# closeout: marcado-ui (TS/vitest) bloqueado por el gate de tests solo .py; sumar *.test.ts/*.test.tsx

_Describe the incoming message with enough evidence to triage._

Coordinador de UIs/marcado-ui en robocop2 (2026-11-16). task.refactor task-retirar-el-código-legacy-huérfano-de-marcado-ui-...: código en 649cea7 (main de marcado-ui), tester independiente deskops-t-8c38967ddbcf PASA (vitest 4 archivos/23 tests, build ok, UI headless sin errores), goldens aceptados. closeout verify da missing_tests_evidence porque reference_points_to_test en deskops/services/closeout_gates.py exige sufijo .py; el repo no tiene Python y closeout_evidence no se puede editar. Lo cubre el punto (2) de task-el-closeout-acepta-tests-de-otros-lenguajes-y-evidencia-de-commit-de-otro-repo-registrado (log bajo runs/ con primera línea '$ cmd' y última 'rc=0'). Pido además sumar a la lista cerrada de (1) *.test.ts y *.test.tsx (vitest/jest), para repos de UI como marcado-ui, graph_ui y sldb-ui. Dos detalles más: (a) editar references de una tarea deja stale sus recibos preflight/bundle, aunque references no está en __contract__, y obliga a re-revisar para registrar el sha del commit de código; (b) el siguiente cierre de marcado-ui (task-extraer-a-src-lib-...) queda en el mismo bloqueo. Avísenme por message send --to marcado-ui cuando aterrice.
