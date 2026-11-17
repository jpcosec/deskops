# Veredicto del tester deskops-t-908138de7331

Tarea: task-review-status-compara-el-contrato-del-taskdoc-y-no-su-texto-entero-igual-que-el-anchor-state-de-la-r
Entrega: diff sin commitear sobre HEAD f41ce57d (deskops/services/review.py, deskops/models/review.py, tests/test_review_command.py, tests/fixtures/model_contract_hashes.json).

## Contrato y precisiones (preflight-3 / bundle-3)
1. Reutiliza `task_contract_sha256` (deskops/runtime/scion.py:211) vía `_task_contract_text` (deskops/services/review.py:113); no hay algoritmo nuevo. OK.
2. ReviewDoc gana `contract_sha256` opcional, vacío por defecto, validado 64-hex (deskops/models/review.py:142, :179) y tratado como ausente en recibos viejos (:106). OK.
3. Estado: `_state_for_key` (review.py:881) usa `contract_sha256` si el recibo lo tiene, si no `input_sha256` como hoy. El digest es el sha del mismo `Bundle` con el texto del TaskDoc sustituido por su digest en la misma posición (`_add_task`, `_contract_sha` review.py:869); en bundle pills/átomos/rituales/files siguen entrando. Tags/status/current_node/history/references/cabecera sldb no lo mueven (verificado en sandbox). OK.
4. input.md e input_sha256: `run_task` llama al builder sin `task_text`, el input es byte a byte el de hoy. OK.
5. Agregación accepted > rejected > pending > incomplete sin cambios. OK.
6. Nodos de plan y recibos `record` dejan el campo vacío → comparación de siempre. OK.

## Fixture fuera de `files`
`tests/fixtures/model_contract_hashes.json` era necesario: con el modelo nuevo y el fixture viejo `test_model_contract_snapshot.py` falla y el hash computado es exactamente `f16882ab…606759`, el valor entregado.

## Validación (validation.log)
test_review_command 29 passed; test_review_doc 22 passed 1 xfailed; test_review_record 21 passed; test_model_contract_snapshot 2 passed; test_activation_rules 10 passed; test_closeout_evidence_receipts 5 passed. Todos rc=0.
Reproducción: los dos tests nuevos de contrato fallan en HEAD (stale != accepted), pasan con la entrega.
Sandbox real (sandbox.log): accepted tras tags y advance; stale tras goal; recibo viejo sin campo conserva el comportamiento de hoy.

## Riesgos para el integrador (no bloquean)
- Cambio de contrato de ReviewDoc: el store real `.sldb` no tiene el modelo actualizado (no se tocó; .sldb/core/models/ReviewDoc.yaml sin cambios). Hay que registrar/migrar el modelo con el CLI de sldb al integrar (como CC33a) y correr la suite completa, que no corrí por orden del brief.
- Done When "en el desk de deskops": los recibos existentes no tienen el campo; el comportamiento nuevo se ve con recibos escritos tras integrar.
- Si el TaskDoc no parsea, `_contract_sha` devuelve "" y los recibos nuevos quedan stale (fallback conservador, aceptable).
- El atajo "unchanged" de review preflight|bundle sigue usando input_sha256 (fuera de alcance).
- La columna de hash de `review status` sigue mostrando el input_sha256 actual, no el contrato (cosmético).

VEREDICTO: APROBADO
