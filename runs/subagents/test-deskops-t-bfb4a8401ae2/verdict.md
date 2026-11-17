# Veredicto del tester deskops-t-bfb4a8401ae2
Tarea: task-deskops-message-ack-acepta-reason-y-la-nota-guarda-el-porque-en-un-campo-ack-reason

VEREDICTO: APROBADO

## Contrato frente al diff
- `ack --reason` guarda `ack_reason` (con strip) junto a acknowledged_by/at. Sin --reason queda `''`. Una nota vieja sin el campo se lee como `''` (lo cubren dos cosas: el validator before en el modelo y `_read_payload`). `message read` en texto pone `Ack reason: <texto>` justo después de acknowledged_at, solo si no está vacío. En json y yaml la clave `ack_reason` va siempre. Cumple las precisiones 1 a 5 del coordinador.
- Goldens: 10 archivos (2 de help y 7 de output, más model_contract_hashes.json), todos atribuibles al campo nuevo. `deskops_add_inbox-note.txt` cambia porque add deriva sus flags del modelo. No queda ningún golden ajeno reescrito ni borrado. test_output_goldens pasa sin `--update-golden`.

## Validación (validation.log)
- test_message_cli: 12 passed. Los 4 FAILED son XPASS(strict) de los tests de llaves: sldb d49f6ddc ya arregló la inyección Jinja y el xfail strict quedó viejo. Es ajeno a esta tarea, pero bloquea la suite verde. **Hay que quitar ese xfail** en una tarea aparte o al integrar, y eso pasa con o sin este cambio.
- test_command_registry 3 passed, test_model_contract_snapshot 2 passed, test_message_delivery 5 passed, test_message_ecosystem_registry 6 passed, test_output_goldens 7 passed.
- Reproducción: los 3 tests nuevos fallan con el código de HEAD.

## Riesgo de modelo compartido (sandbox.md)
No bloquea. Un desk con el InboxNoteDoc viejo en su .sldb recibe, lee y ackea notas viejas y nuevas (con y sin --reason) bajo el código nuevo. `sldb stores check` da PASS con alertas `store/contract-moved` y `store/contract-mutation` ("safe to run: sldb stores update"), y `deskops doctor` dice "healthy, with 2 alert(s)". La primera escritura tracked (send o ack) o un `sldb stores update` deja el store limpio. El código viejo también lee notas con ack_reason sin problema. Acción por desk: correr `sldb stores update` tras desplegar en herramientas/deskops; en este repo, además, actualizar `.sldb/core/models/InboxNoteDoc.yaml` al cerrar, como ya está previsto.

## Hallazgos menores (no bloquean)
- `show_inbox-note.text` agrega `ack_reason: ` con espacio final cuando está vacío. Es cosmético y coherente con el renderer genérico.
- El ejecutor informa que `--update-golden` borra 5 goldens `.text` que ya no se generan. Los restauró y no están en la entrega. Conviene que alguien lo mire fuera de esta tarea.
