# Veredicto del tester deskops-t-59a02e2fac60

Tarea: task-closeout-verify-escribe-un-recibo-nuevo-cuando-el-veredicto-cambia-aunque-el-input-sea-el-mismo
Entrega: diff sin commitear en deskops/services/closure.py y tests/test_closeout_declared_evidence.py (ejecutor deskops-e-7fbb23ba5137).

## 1. Diff contra el contrato
- closure.py: único cambio funcional, `same_input` exige `input_sha256` igual **y** `payload["verdict"] == verdict`
  (campo verdict del payload, precisión 3). La comprobación de intacto sigue siendo `review_id not in _not_intact_documents()`
  (precisión 1): se salta solo si algún recibo intacto del mismo fact tiene mismo input y mismo verdict.
- Cualquier cambio de verdict con el mismo input escribe uno nuevo (simétrico, bundle 3): el filtro no distingue dirección.
- Sin cambios en `_evidence_input_sha256`, en el nombrado `review-<task>-evidence-<fact>-<n>` ni en la regla de closeout.
- Docstring actualizado. Archivos tocados = `files` de la tarea.

## 2. Validación (validation.log)
- tests/test_closeout_declared_evidence.py: 25 passed, rc=0
- tests/test_closeout.py: 62 passed, rc=0
(de a un archivo, sin lock, PYTHONPATH al checkout, TMPDIR=/dev/shm). Suite completa no corrida por encargo.

## 3. Reproducción con closure.py de HEAD (copia en /dev/shm, ya borrada)
- test_a_changed_verdict_...: FALLA con `assert ['rejected'] == ['rejected', 'accepted']` (línea 422): exactamente el bug.
- test_two_green_verifies_do_not_duplicate_receipts: pasa en HEAD y con el fix (guarda de no regresión, esperado).

## 4. Juicio del test
- Uso del método privado: correcto y acotado a la precisión 2. Los gates son los reales de `verify_task_closeout`
  (write_receipts=False, no escribe recibos), copiados y con solo `tests.ok=False` + finding; los items no cambian,
  así que el input es el mismo (lo asserta: input_sha256 iguales). Luego el verde va por el CLI real (`_verify`)
  y el cierre por `closeout commit --no-run` (rc 0, sin `[rules/rule-closeout-task-code]`). Cubre además la simetría
  (vuelta a rejected escribe el recibo 3) y la no duplicación de dos verify verdes.
- Caso real de la nota (sldb-ui, fact `atom` rejected y luego accepted con los mismos 4 atoms): el test usa el fact
  `tests`, no `atom`. La dedup es agnóstica al fact (mismo bucle para todos), por lo que el mecanismo del caso real
  queda cubierto; no hay test literal con `atom`.

## Riesgos / hallazgos menores (no bloquean)
- Sin test literal del fact `atom`/link gate; cobertura por mecanismo compartido.
- Un vaivén de verdict con el mismo input acumula recibos (uno por cambio), por diseño del contrato.
- El test escribe un recibo vía método privado; si `_write_evidence_receipts` se renombra, el test se rompe ruidosamente (aceptable).

VEREDICTO: APROBADO
