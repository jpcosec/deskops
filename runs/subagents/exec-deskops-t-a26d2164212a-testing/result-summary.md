PASA

# Veredicto del tester

El commit del ejecutor cumple el Goal y la Validation: al arrancar, dispatch commitea el `run.md`
del run dir del agente junto con los archivos de store del RunDoc, y el gate de store de
`integrate` pasa sobre ese commit.

## Commit evaluado

- Commit: `fe2f3a3ff445373763f08fbfb240dde78ae83dd6`
- Mensaje: `dispatch commitea el run.md del run dir junto con su RunDoc`
- Trailer: `Task-Id: task-dispatch-commitea-tambien-el-run-md-del-run-dir-junto-con-su-rundoc-integrate-fallaba-en-store-con-u`
- Archivos:
  - `deskops/dispatch.py`
  - `tests/test_dispatch.py`
  - `CHANGELOG.md`

El HEAD del worktree (`76e9f84a`, commit de arranque del tester) difiere del commit del ejecutor
solo en los archivos de store del run del tester; `git diff fe2f3a3f HEAD -- deskops/dispatch.py
tests/test_dispatch.py CHANGELOG.md` está vacío, así que los tests corren sobre el código exacto
del commit evaluado.

## Cambios verificados

- `_run_store_paths` añade `runs/subagents/exec-<nombre>/run.md` para executor y `-testing` para
  tester, filtrado por existencia, junto a los paths de store ya presentes.
- `_commit_run_store` sigue commiteando con pathspec los paths devueltos, de modo que `run.md` entra
  en el mismo commit `run: <agente>` que el shard del RunDoc. El closeout posterior no se rompe
  porque `run.md` ya queda trackeado.
- Test nuevo: `test_start_commits_the_run_md_with_the_rundoc_and_the_store_gate_passes` comprueba
  que el commit incluye `run.md` y el shard, y que todos los paths no externos de
  `.sldb/store.yaml` existen en `HEAD` usando `_collect_paths` (el mismo chequeo que corre integrate).

## Tests ejecutados

Nota de entorno: `/workspace/.venv/bin/python` no tiene pytest (el symlink apunta a
`/usr/bin/python3`, Python 3.11, mientras site-packages es 3.12), así que usé el venv funcional
`/dev/shm/t311` (Python 3.11 + pytest 9.2.0). Todo con
`TMPDIR=/tmp LANG=es_ES.UTF-8 LC_ALL=es_ES.UTF-8 LANGUAGE=es`.

- `python -m pytest -q -p no:cacheprovider tests/test_dispatch.py` → **37 passed**, 403.44s.
- `python -m pytest -q -p no:cacheprovider tests/test_integrate.py` → **25 passed**, 296.57s.
- Test nuevo aislado: `tests/test_dispatch.py::test_start_commits_the_run_md_with_the_rundoc_and_the_store_gate_passes` → **1 passed**, 18.02s.

Las únicas advertencias son `PytestConfigWarning: Unknown config option:
asyncio_default_fixture_loop_scope` (config del proyecto, no relacionada con el cambio).

## Done When

Los tests nuevos, `tests/test_dispatch.py` y `tests/test_integrate.py` pasan. Verificado.
