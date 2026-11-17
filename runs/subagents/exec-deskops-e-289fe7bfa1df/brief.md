# Encargo del ejecutor deskops-e-289fe7bfa1df (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-review-status-compara-el-contrato-del-taskdoc-y-no-su-texto-entero-igual-que-el-anchor-state-de-la-r`

Contrato: `deskops show task task-review-status-compara-el-contrato-del-taskdoc-y-no-su-texto-entero-igual-que-el-anchor-state-de-la-r --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las precisiones del scope y las del coordinador de abajo son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`. El PYTHONPATH es obligatorio: el venv tiene deskops editable desde /mnt/ssd/herramientas/deskops y los tests que lanzan `python -m deskops` en subproceso probarían ese checkout y no este.
- Si la tarea agrega o cambia un comando del CLI, corre también tests/test_command_registry.py (pedido del integrador wA:p1): un comando que escribe desk, store o git se declara mutates=True en el registro y en MUTATING_COMMANDS del test.
- NO corras la suite completa ni `stores build --check` (orden del integrador wA:p1: los corre él una vez por integración en una copia limpia; el lock /dev/shm/sldb1-tests.lock es el cuello de botella). Tu validación son los tests de la Validation de la tarea, de a un archivo y sin lock. Si un comando de la Validation pide la suite completa, no lo corras: anótalo en result-summary.md como "para el integrador".
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-289fe7bfa1df/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Precisiones del coordinador (recibos preflight-3 y bundle-3)

Precisiones del coordinador (preflight 3 y bundle 3): (1) El digest existe: deskops/runtime/scion.py task_contract_sha256(markdown), que delega en sldb; se reutiliza, no se inventa algoritmo. (2) __contract__ esta en deskops/models/task.py:39: title, goal, scope, implementation_path, files, validation, done_when; el digest usa esa proyeccion. (3) Agregar un campo opcional contract_sha256 a ReviewDoc en deskops/models/review.py entra en alcance (vacio por defecto; los recibos viejos sin el campo siguen con la comparacion actual). (4) La agregacion del estado no cambia: es la prioridad actual accepted/rejected/pending/incomplete sobre los recibos vigentes; 'el mas reciente' del texto era impreciso. (5) En el hash del bundle se mantiene exactamente la serializacion de hoy y solo se reemplaza el texto del TaskDoc por su contract_sha256 en la misma posicion. (6) No hace falta probar equivalencia con el anchor_state de la regla de activacion: los tests son los de la Implementation Path (tags y status no cambian el estado; goal si).

## Notas del coordinador

- URGENTE (pedido del supervisor): editar tags o references de una tarea deja hoy stale sus recibos y obliga a re-correr revisiones pi con --force (notas 20261116-094650 y -094652 de sldb-ui y graph_ui).
- deskops/models/review.py cambió hace poco (ids de nodo con punto, otra tarea en curso con cambios sin commitear en ese archivo y en tests/test_review_doc.py y tests/test_review_command.py): coordina tus cambios sobre esos mismos archivos sin pisar los suyos; si chocan, dilo en result-summary.md.
- Mutaciones de desk en tests: solo sandbox (tmp_path) con fake_pi.
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
