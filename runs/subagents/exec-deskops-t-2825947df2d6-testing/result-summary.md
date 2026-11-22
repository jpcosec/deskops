PASA

# Verificación

Tarea: `task-reap-dice-integrado-0-commits-y-borra-la-rama-del-ejecutor-aunque-tenga-un-commit-fuera-de-main-se-p`
Commit del ejecutor (último): `43b17685326610719574807f78044110330af4b9` — "fix(dispatch): reap waits for live executors and dirty worktrees, no --force"
Commit base del arreglo del reap: `67f55538ddc6ce8bb025ab49f928e3aa9eaeb91c` — "fix(dispatch): reap counts base..branch and never deletes a branch whose tip is not in base"

Ambos commits llevan el trailer `Task-Id` de esta tarea y tocan solo el alcance previsto:
`CHANGELOG.md`, `deskops/dispatch.py`, `tests/test_dispatch.py`.

## Código

- `_integrate_branch` calcula los commits con `git rev-list --reverse --no-merges <base>..<branch>` (sin `--cherry-pick`, que era lo que descartaba el commit del ejecutor por equivalencia de parche).
- Si el conteo da 0 pero la punta de la rama no es ancestro de base, no borra worktree ni rama y devuelve 8 con un mensaje que nombra la rama y la punta.
- El cherry-pick usa `--keep-redundant-commits`, de modo que un parche ya presente en main no hace perder el commit del ejecutor.
- El segundo commit agrega esperas para ejecutores vivos o worktrees con cambios sin commitear y quita `--force` de `git worktree remove`; también está cubierto por tests y no rompe la validación.

## Tests

Entorno: el `.venv` del repo está roto en este contenedor (el shebang de `pytest` apunta a una ruta inexistente y no hay Python 3.12); usé el venv funcional `/dev/shm/t311` (Python 3.11, pytest 9.2.0), como en verificaciones anteriores.

- Validación pedida, locale por defecto (equivalente al caso en_US):
  `TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`
  → `44 passed, 1 warning in 463.91s`.
- Misma suite con entorno es_ES:
  `LOCPATH=/tmp/locales TMPDIR=/tmp LANG=es_ES.UTF-8 LC_ALL=es_ES.UTF-8 LANGUAGE=es /dev/shm/t311/bin/python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`
  → `44 passed, 1 warning in 463.95s`.
  Nota: el contenedor no trae datos de locale es_ES/en_US; para poder fijar `LC_ALL=es_ES.UTF-8` usé un `LOCPATH` temporal con un directorio copiado de `C.utf8` bajo el nombre `es_ES.UTF-8`. El test propio del repo `test_reap_names_the_files_under_a_spanish_locale` también pasa.
- Reproducción del caso del commit `run:`: en un worktree temporal del commit padre `67f55538^`, con el test nuevo de `67f55538`, el test falla exactamente con `integrado 0 commit(s)` (el bug); en el árbol actual los tests nuevos pasan:
  - pre-fix: `1 failed, 41 deselected` (`test_reap_brings_the_commit_made_on_top_of_a_run_commit_made_in_main`).
  - post-fix: `4 passed, 40 deselected` (reproducción + guarda de punta + esperas por ejecutor vivo/worktree sucio).

No corrí la suite completa. No modifiqué código, tests ni el store.

## Done When

- El test de reproducción del commit `run:` pasa en el árbol actual y falla en el commit padre: verificado.
- `tests/test_dispatch.py` pasa completo en el entorno por defecto (en_US) y en es_ES: verificado, 44 passed en cada uno.

## Observaciones no bloqueantes

- `--keep-redundant-commits` puede dejar un commit vacío cuando el parche del ejecutor ya estaba en main. Es intencional para conservar el commit (y su `Task-Id`); el test lo comprueba.
- El segundo commit incluye la protección extra de la carrera `reap`/commit del ejecutor (ejecutor vivo o worktree sucio). Está dentro de `deskops/dispatch.py`, `tests/test_dispatch.py` y `CHANGELOG.md`, y la validación pasa; no es un bloqueo.

Sin hallazgos bloqueantes.
