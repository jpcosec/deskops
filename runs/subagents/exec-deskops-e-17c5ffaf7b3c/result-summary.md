# Resultado: task-closeout-commit-incluye-el-run-md-de-cada-rundoc-que-el-store-trackea-y-git-todavia-no-tiene-para-qu

- run_id: run-deskops-e-17c5ffaf7b3c
- session: scion://agent/deskops-e-17c5ffaf7b3c (sesión claude; sin archivo de transcript local)
- session_sha256: (no disponible)

## Cambios

- `deskops/services/closure.py` (en files):
  - `_close`: después del `git add -A .sldb` y antes de la proyección `desk/reviews/<tarea>/`, hace `git add` de cada path devuelto por el nuevo `_unknown_registered_run_docs()` y lo suma a `commit_paths` (así entra también en el pathspec explícito y `_restore_index` lo desindexa si el cierre falla). Corre siempre, no solo si `.sldb` está sucio: cubre el caso real de un registro que ya está en HEAD con su run.md sin commitear. Como todos los modos (run-dir, --no-run/manual, supersede, resolved-by, legacy-resolved, retire, legacy) pasan por `_close`, todos lo heredan.
  - `_unknown_registered_run_docs()`: lee `.sldb/store.yaml`, toma los `include` con `model: RunDoc`, y devuelve los `path` (relativos a la raíz) que existen como archivo en disco, están dentro del repo, no están ignorados por git y git no conoce (ni índice ni HEAD, vía `_git_knows`). Un RunDoc registrado sin run.md en disco se ignora en silencio (precisión 4). Un store.yaml ilegible devuelve [] (no bloquea el cierre).
- `tests/test_closeout.py` (en files):
  - `test_closeout_commit_includes_the_run_md_of_every_registered_run_doc_git_lacks[run-dir|no-run]`: sandbox `lifecycle_desk` + `store_repo`; registra con `record_scion_run` el RunDoc de otra corrida y publica solo `.sldb` (como el closeout 9dbcfc7c), luego el RunDoc propio; tras `closeout commit` el run.md de la otra corrida está en el commit y todo path RunDoc del `store.yaml` de HEAD existe en HEAD (`git cat-file -e`), lectura del done_when según precisión 5 (sin clon ni CLI de sldb).
  - `test_closeout_commit_skips_a_registered_run_doc_without_a_run_md`: registro sin run.md en disco → cierre rc 0 y no se toca.
- Comprobado que el test nuevo FALLA con el bucle desactivado (run.md de la otra corrida ausente del commit) y pasa con el arreglo.

Ningún archivo fuera de `files`. Los cambios en `.sldb/` del árbol (RunDoc.yaml, store_index.yaml, store.yaml, run-deskops-e-17c5ffaf7b3c.yaml) son previos a esta sesión (registro del RunDoc de intención de esta corrida), no míos.

## Validación

- `pytest -q tests/test_closeout.py`: 73 passed, rc=0 (ver validation.log).
- Suite completa / `stores build --check`: no corridos, para el integrador.

## Riesgos

- El cierre ahora puede arrastrar run.md de corridas ajenas en curso (intención `in_progress`). Es lo pedido: el store ya las publica; sin el run.md el clon no construye.
- Solo run.md; los demás archivos de esos run dirs quedan fuera (scope).
