PASA

# Veredicto del tester deskops-t-1bdc9d47c4ad

- task: task-integrate-puede-terminar-en-un-pr-a-la-rama-base-declarada-modo-pr-en-vez-de-un-push-directo-con-el
- Commit revisado: `ca7ecfc518fa8955e2d51e99caa72449fe5b5e1c` (integrate: modo pr (task/<id>, push de la rama y gh pr create)), con trailer `Task-Id` de la tarea.
- Archivos del commit: `deskops/config.py`, `deskops/dispatch.py`, `deskops/integrate.py`, `tests/test_dispatch.py`, `tests/test_integrate.py`, `docs/operator-manual.md`, `CHANGELOG.md`.

## Tests ejecutados (de a uno, TMPDIR=/tmp)

| Archivo | Resultado |
|---|---|
| `tests/test_config.py` (modulo tocado: config) | 5 passed |
| `tests/test_dispatch.py` (modulo tocado: dispatch; incluye `test_reap_in_pr_mode_brings_commits_to_the_task_branch_not_the_base`) | 45 passed |
| `tests/test_integrate.py` (modulo tocado: integrate; incluye los 3 tests nuevos de modo pr con dev protegida y gh falso) | 28 passed |

Sin fallos de regresion en modo push.

## Comprobaciones funcionales

- `IntegrateConfig.mode` es `Literal["push", "pr"]` con default `"push"`.
- En modo pr, `dispatch reap` crea/usa `task/<task-id>` desde la base, deja esa rama en el checkout principal y no mueve la base local (verificado por test).
- `integrate` en modo pr corre las mismas compuertas sobre la punta, empuja `task/<task-id>` al remoto y llama `gh pr create --base <integrate.branch> --head task/<task-id>` con el id de tarea en el cuerpo; si el PR ya existe solo empuja; imprime `PR: <url>`. El remoto `dev` no se toca.
- El modo push conserva el comportamiento previo.
- La documentacion separa config versionado (`config.json`) de config por maquina (`config.local.json`, no versionado) y no agrega rutas de maquina nuevas.

## Nota de entorno

El `.venv` compartido tiene enlaces rotos (`/usr/bin/python3.12` no existe en esta sesion). Los tests se corrieron con `uv run --no-project --python 3.12` (CPython 3.12.16), `PYTHONPATH=/workspace/deskops:/workspace/sldb/src` y las dependencias de runtime de sldb (`pydantic`, `pyyaml`, `networkx`, `jinja2`, `markdown-it-py`, `mdit-py-plugins`, `linkify-it-py`). Detalle en `validation.log`.
