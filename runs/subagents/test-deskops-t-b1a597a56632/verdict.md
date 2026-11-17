# Veredicto del tester deskops-t-b1a597a56632

Tarea: task-closeout-commit-no-amienda-un-commit-que-la-tarea-cita-como-evidencia-de-commit
Entrega: deskops/services/closure.py y tests/test_closeout.py sin commitear (ejecutor deskops-e-3cd90f55821f).

## 1. Diff contra el contrato

- `deskops/services/closure.py:730-733`: las citas se leen antes de que el cierre borre la tarea (`task_bytes is not None`); sin tarea, no hay citas → comportamiento anterior.
- `deskops/services/closure.py:801-805`: la única rama que cambia es la decisión amend/commit nuevo; se añade `not self._head_is_cited(...)`. El amend del index.jsonl (`:849`), los trailers y los otros modos (record, resolved-by, supersede, retire) no se tocan.
- `deskops/services/closure.py:1255-1287` `_cited_commit_evidence`: references = items hex minúsculas de 7+ (precisión preflight (2)); recibos = `evidence-commit-*.md` con kind evidence, fact commit y `verdict: accepted` (vía `_evidence_receipts`, ya existente). No mira history ni cuerpo (precisión bundle (5)). `_head_is_cited`: `rev-parse HEAD` (completo, stripped) empieza con un ref o es igual a un value.
- Decisión `splitlines` sobre el value: correcta. `closure.py:1106` escribe `value = "\n".join(items)`; con un solo commit equivale a comparar el value entero (lo que pide preflight (2)) y con varios commits cada línea es un sha completo comparado entero, sin coincidencias por prefijo. No relaja la regla; la mantiene coherente con el formato que el propio verify produce.

## 2. Tests (de a un archivo, PYTHONPATH al checkout, TMPDIR=/dev/shm)

- tests/test_closeout.py: 62 passed, rc=0
- tests/test_closeout_declared_evidence.py: 23 passed, rc=0
- tests/test_closeout_resolved_by.py: 25 passed, rc=0

## 3. Reproducción con closure.py de HEAD (git archive HEAD + test nuevo)

- `...cites_as_commit_evidence[reference]` FAILED, `[receipt]` FAILED; `...still_amends_an_uncited_head...` passed. Los tests nuevos capturan exactamente el defecto.

## 4. Caso real en sandbox (/dev/shm, git init + deskops init, PYTHONPATH al checkout)

- task.code; commit de código `8a3967ae…` con `Task-Id: task-feature-x`; `8a3967ae` en references (+ un test para el gate tests).
- `closeout verify`: rc=0, gate commit ok con evidencia `8a3967ae`; recibo evidence-commit-1 accepted con value = sha completo.
- `closeout commit --no-run`: rc=0, cierre `b20d4ac5…` (Closeout-Mode: manual) con HEAD^ = `8a3967ae14f7…`; el commit de código es ancestro de HEAD, conserva su sha y solo contiene feature.py.
- Contraste mismo guion con closure.py de HEAD: el commit de código NO es ancestro (amendado). Confirma el arreglo.

## Hallazgos menores (no bloqueantes)

- tests/test_closeout.py (test parametrizado): `assert main([... "closeout", "verify" ...]) in (0, 1)` es laxo; el test no depende del rc de verify sino del commit, así que no afecta lo que prueba.
- Referencias calificadas `<repo>:<sha>` no cuentan como cita: conforme a la precisión preflight (2), pero queda como hueco conocido si en el futuro se citan así commits locales.
- Suite completa no corrida (por encargo).

## Riesgos

- `_head_is_cited` usa `check=False`: si `rev-parse HEAD` falla (repo sin commits) cae al amend/commit previo, igual que antes.

VEREDICTO: APROBADO
