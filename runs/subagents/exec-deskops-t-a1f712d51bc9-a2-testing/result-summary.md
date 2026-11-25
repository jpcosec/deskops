PASA

# Resultado del tester

Tarea: task-closeout-commit-stagea-solo-lo-que-escribio-el-cierre-sin-git-add-a-sobre-sldb-y-sin-nothing-staged
Run: run-deskops-t-a1f712d51bc9-a2
Commit evaluado: f629463d95dff106aca307f623e3df9b2d9c448d — "closeout commit: no stagear .sldb previo ajeno (hash) y commit con pathspec sin --paths".
Trailer verificado: `Task-Id: task-closeout-commit-stagea-solo-lo-que-escribio-el-cierre-sin-git-add-a-sobre-sldb-y-sin-nothing-staged`.

Archivos del commit:
- `deskops/services/closure.py`: la foto de `.sldb` pasa a `(porcelain, sha256)`; solo se stagea una ruta nueva o cuyo estado/hash cambió respecto de la foto previa. La proyección de cierre queda limitada a `ReviewDoc`/`AtomDoc` del task o stems de `--paths` (y su modelo). Sin `--paths`, el pathspec del commit son siempre las rutas que el cierre stageó, y el chequeo de "Nothing staged" mira el índice restringido a esas rutas.
- `tests/test_closeout.py`: nuevos casos `supersede`, `retire` y `closeout commit` sin `--paths` con estado ajeno (trackeado modificado, untracked, untracked que nombra la tarea, y staged) que no debe viajar en el commit.
- `tests/test_closeout_resolved_by.py`: nuevo caso de `resolved-by` que deja intacto un `.sldb` untracked ajeno.

## Pruebas ejecutadas

Entorno: el `.venv` del repo apunta a `/home/robocop/...` y a un Python 3.12 inexistente en este host, así que usé un venv propio en `/dev/shm/deskops-test-venv` (CPython 3.12.16) con instalación editable de `/mnt/ssd/proyectos/SLDB_1/deskops` y `/mnt/ssd/proyectos/SLDB_1/sldb`, más pytest 9.2.0.

- `TMPDIR=/tmp /dev/shm/deskops-test-venv/bin/python -m pytest -q tests/test_closeout.py` -> **82 passed**, exit 0 (94.20 s).
- `TMPDIR=/tmp /dev/shm/deskops-test-venv/bin/python -m pytest -q tests/test_closeout_resolved_by.py` -> **26 passed**, exit 0 (17.78 s).
- `TMPDIR=/tmp /dev/shm/deskops-test-venv/bin/python -m pytest -q tests/test_closeout_atomless.py` -> **15 passed**, exit 0 (47.96 s).
- Los 4 tests nuevos, apuntados por nombre -> **4 passed**, exit 0 (22.20 s):
  - `test_closeout_commit_without_paths_leaves_foreign_sldb_and_staged_changes_out`
  - `test_closeout_supersede_leaves_a_foreign_untracked_sldb_file_untracked`
  - `test_closeout_retire_leaves_a_foreign_untracked_sldb_file_untracked`
  - `test_resolved_by_leaves_a_foreign_untracked_sldb_file_untracked`

No existe `tests/test_closure.py` para el módulo tocado. No se corrió la suite completa (la corre el integrador).

## Control negativo

En un árbol temporal con el código previo (`e7049f1f`, padre de f629463d) y copiando solo los tests nuevos de f629463d:

- `test_closeout_commit_without_paths_leaves_foreign_sldb_and_staged_changes_out` **falla**: el commit arrastra `.sldb/core/models/UnusedDoc.yaml` (trackeado modificado antes del cierre), `.sldb/core/documents/foreign-other.yaml`, `.sldb/core/models/ForeignModelDoc.yaml` y `unrelated.txt` staged.
- Los otros 3 casos pasan ya en el baseline (2fe1b60e había cubierto el untracked por código de estado); el caso de commit sin `--paths` es el que captura la regresión de este segundo commit.

Esto confirma que el test principal falla antes y pasa después. El árbol temporal se eliminó; no se modificó el repo.

## Cobertura del Done When

- Test (a): `untracked_model`/`untracked_doc` siguen `??` y no aparecen en `git show --name-only HEAD`; además supersede/retire/resolved-by dejan `foreign.yaml` untracked.
- Test (b): `.sldb` trackeados modificados antes del cierre siguen en `git diff` y no en `git diff --cached`.
- Test (c): `closeout commit` sin `--paths` cierra (rc 0) y el commit incluye el TaskDoc; el Board queda cubierto por `test_closeout_commit_without_paths_commits_the_task_and_the_board` (pre-existente), que pasa en la corrida del archivo.
- El error "Nothing staged" con lista de rutas modificadas y sugerencia `--paths` sigue cubierto por `test_closeout_commit_without_paths_and_nothing_to_stage_lists_modified_paths`, que pasa.

## Observaciones no bloqueantes

- `test_closeout_commit_includes_the_run_md_of_every_registered_run_doc_git_lacks` fue ajustado en el commit: ya no exige que `store.yaml` registre la corrida propia, porque ese `store.yaml` ya estaba modificado antes del cierre y la nueva política no lo stagea. Es coherente con la precisión de autoría por foto de git, pero reduce la verificación de "clone limpio reconstruye el store" a lo que quedó registrado en HEAD. No afecta los tests de esta tarea.
- Los tests nuevos de supersede/retire/resolved-by pasan también en el baseline; sirven como cobertura de que esas rutas usan el mismo helper, no como detección de la regresión principal.
