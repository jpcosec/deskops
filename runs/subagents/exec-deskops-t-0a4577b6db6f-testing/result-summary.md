PASA

Task: task-reap-nombra-los-archivos-que-bloquean-el-cherry-pick-sin-depender-del-idioma-de-git-falla-con-lang-e
Commit del ejecutor: cdca5251242ab0951e1847769049ff36ea3627e5
Archivos: CHANGELOG.md, deskops/dispatch.py, tests/test_dispatch.py

- Alcance del commit: PASS - solo los tres archivos previstos; `_git` ahora corre con
  `LC_ALL=C` y `LANGUAGE=`, y se agrega
  `test_reap_names_the_files_under_a_spanish_locale` que actualiza el entorno del
  subproceso a `LANG=es_ES.UTF-8 LC_ALL=es_ES.UTF-8 LANGUAGE=es`.
- Tests en ingles: PASS - `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider
  tests/test_dispatch.py` -> 36 passed, 1 warning (346 s). Se uso
  `/workspace/sldb/.venv/bin/python` porque el `.venv` del repo apunta a una ruta
  inexistente y no hay `python` en PATH.
- Tests con locale espanol: PASS - la misma suite con
  `TMPDIR=/tmp LANG=es_ES.UTF-8 LC_ALL=es_ES.UTF-8 LANGUAGE=es` -> 36 passed,
  1 warning (351 s). El test puntual tambien paso (20 s).
- Regresion real: PASS - este contenedor no traia locales es_* ni catalogo git es.
  Para no dar un PASS vacio se creo temporalmente un locale es_ES.utf8 y un
  catalogo `git.mo` con las traducciones reales de `po/es.po` (la de cherry-pick
  dice "tus cambios locales seran sobreescritos por cherry-pick."). Con eso el
  mismo test en el commit padre (cdca5251^) falla (1 failed: rc 8 pero sin
  `shared.txt` ni `commitea`) y en cdca5251 pasa. Luego se eliminaron el locale,
  los catalogos y el worktree temporales.
- CHANGELOG: PASS - entrada agregada bajo `Fixed`, menciona `LC_ALL=C`,
  `LANGUAGE=`, el timer con `LANG=es_ES.UTF-8`, el rc 8 y el test.

No se corrio la suite completa. No se modifico codigo, desk ni .sldb desde el tester.
