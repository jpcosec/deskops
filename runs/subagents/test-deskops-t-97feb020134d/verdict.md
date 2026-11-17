# Veredicto del tester deskops-t-97feb020134d

Tarea: task-closeout-commit-incluye-el-run-md-de-cada-rundoc-que-el-store-trackea-y-git-todavia-no-tiene-para-qu
Entrega: deskops/services/closure.py y tests/test_closeout.py, sin commitear (ejecutor deskops-e-17c5ffaf7b3c)

VEREDICTO: APROBADO

## Hallazgos

1. Diff: se cumple el contrato y las precisiones (1)–(6) del preflight-1 y el bundle-1.
   - `_close` llama a `_unknown_registered_run_docs()` justo después del `git add -A .sldb` y antes de la proyección `desk/reviews/<tarea>`. Hace `git add` de cada ruta y la añade a `commit_paths`. Como ahí pasan todos los modos, todos lo heredan.
   - `_unknown_registered_run_docs()` lee los `include` con `model: RunDoc` de `.sldb/store.yaml` (`paths` como `{path, name}` o como cadena). Se queda con los archivos que existen en disco, están dentro de la raíz, no ignora git y git no conoce ni en el índice ni en HEAD. Si un RunDoc está registrado pero su run.md no está en disco, se salta sin avisar. Si store.yaml no se puede leer, devuelve [] y no bloquea.
   - Con `--paths` explícitos, el pathspec se filtra con `_git_knows`. Como el run.md ya está en el índice, pasa el filtro. Sin pathspec, el commit toma todo el índice, así que el run.md entra igual. Si el cierre falla, `_restore_index(commit_paths)` lo saca del índice.
   - No se cambia nada más. Solo entra run.md; los demás archivos del run dir quedan fuera (sale del alcance).
2. Riesgo de arrastrar el run.md de una corrida ajena en curso: es real, pero es justo lo que pide la tarea y es aceptable. El store ya publica ese registro, y sin el run.md un clon limpio no construye el store. Lo que entra es la intención (`outcome: in_progress`). Cuando esa corrida actualice su run.md más tarde, aparecerá como modificación de un archivo trackeado y la recogerá su propio cierre. No se pierde nada ni se rompe nada. Nota menor: el commit de cierre de la tarea X puede llevar el run.md de la corrida Y. Es ruido de atribución, no un fallo.
3. Validación (validation.log):
   - tests/test_closeout.py: 73 passed, rc=0
   - tests/test_closeout_declared_evidence.py: 25 passed, rc=0
4. Reproducción: copié closure.py de HEAD con `git archive` a /dev/shm y le puse el test de la entrega. Los dos parámetros del test nuevo (run-dir y no-run) FALLAN en `assert other_rel in committed` (tests/test_closeout.py:1429), que es la aserción que corresponde. La guarda negativa (un RunDoc sin run.md) pasa también con HEAD, como se espera de un test de no regresión. Ya borré la copia de /dev/shm.
5. No corrí la suite completa, como pide el encargo. Como dice la precisión (5), el test comprueba con `git cat-file -e` y no clona ni corre `sldb stores build`.
