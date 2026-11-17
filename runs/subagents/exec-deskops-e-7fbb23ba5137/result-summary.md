# result-summary — deskops-e-7fbb23ba5137

- run_id: run-deskops-e-7fbb23ba5137
- task: task-closeout-verify-escribe-un-recibo-nuevo-cuando-el-veredicto-cambia-aunque-el-input-sea-el-mismo
- session: scion://agent/deskops-e-7fbb23ba5137 (agente claude); session_sha256: no disponible desde dentro de la sesión

## Cambios (todos dentro de `files` de la tarea)

- `deskops/services/closure.py` (`_write_evidence_receipts`): `same_input` ahora solo cuenta los recibos del mismo
  fact con el mismo `input_sha256` **y el mismo `verdict`** (campo `verdict` del payload del ReviewDoc). Se salta
  únicamente si alguno de esos tiene el anchor intacto (no está en `_not_intact_documents()`), como antes. Cualquier
  cambio de verdict con el mismo input (rejected→accepted o accepted→rejected) escribe un recibo nuevo. Docstring
  actualizado. Sin cambios en el cálculo de input_sha256, los nombres de recibos ni la regla de closeout.
- `tests/test_closeout_declared_evidence.py`: dos tests nuevos (desk sandbox vía fixture `repo`/tmp_path):
  - `test_a_changed_verdict_on_the_same_input_writes_a_new_receipt_and_unblocks_closeout`: con los gates reales de
    verify, a nivel de servicio se escribe un recibo `tests` rejected (gate en rojo con los mismos items); luego
    `closeout verify` (CLI) en verde escribe el accepted (mismo input_sha256) y `closeout commit --no-run` cierra
    (rc 0, sin bloqueo de rule-closeout-task-code). Además comprueba la simetría: volver a rejected escribe un 3.º recibo.
  - `test_two_green_verifies_do_not_duplicate_receipts`: dos verify en verde dejan el mismo conjunto de recibos.

## Validación

- `pytest -q tests/test_closeout_declared_evidence.py`: 25 passed, rc=0
- `pytest -q tests/test_closeout.py`: 62 passed, rc=0
- Prueba de regresión: sin el fix, el test nuevo falla (solo existe el recibo rejected). Ver validation.log.
- Suite completa: no corrida por orden del integrador (para el integrador).

## Riesgos

- Un ida y vuelta de verdict con el mismo input acumula recibos (uno por cambio); los verify repetidos con el mismo
  verdict siguen sin duplicar. El test nuevo usa el método privado `_write_evidence_receipts` para simular el gate en
  rojo, tal como permite la precisión 2 del coordinador.
