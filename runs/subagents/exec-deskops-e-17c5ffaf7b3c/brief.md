# Encargo del ejecutor deskops-e-17c5ffaf7b3c (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-closeout-commit-incluye-el-run-md-de-cada-rundoc-que-el-store-trackea-y-git-todavia-no-tiene-para-qu`

Contrato: `deskops show task task-closeout-commit-incluye-el-run-md-de-cada-rundoc-que-el-store-trackea-y-git-todavia-no-tiene-para-qu --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las precisiones del coordinador de abajo son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`. El PYTHONPATH es obligatorio: el venv tiene deskops editable desde /mnt/ssd/herramientas/deskops y los tests que lanzan `python -m deskops` en subproceso probarían ese checkout y no este.
- Si la tarea agrega o cambia un comando del CLI, corre también tests/test_command_registry.py (pedido del integrador wA:p1): un comando que escribe desk, store o git se declara mutates=True en el registro y en MUTATING_COMMANDS del test.
- NO corras la suite completa ni `stores build --check` (orden del integrador wA:p1: los corre él una vez por integración en una copia limpia; el lock /dev/shm/sldb1-tests.lock es el cuello de botella). Tu validación son los tests de la Validation de la tarea, de a un archivo y sin lock. Si un comando de la Validation pide la suite completa, no lo corras: anótalo en result-summary.md como "para el integrador".
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-17c5ffaf7b3c/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Precisiones del coordinador (recibos preflight-1 y bundle-1)

Precisiones del coordinador (preflight 1 y bundle 1): (1) 'Cualquier modo' son los que pasan por _close en closure.py (run-dir, --no-run, manual, supersede, resolved-by, legacy-resolved y retire): el armado de rutas es comun, asi que basta hacerlo ahi; el test cubre run-dir y --no-run. (2) Lo de hoy se lee en _close: commit_paths, el git add -A de .sldb y la proyeccion desk/reviews/<tarea>/. (3) En .sldb/store.yaml los RunDoc estan bajo include: un item con model: RunDoc y paths: una lista de {path: runs/subagents/<run>/run.md, name: run-<id>}; el path es relativo a la raiz del repo. (4) Un RunDoc registrado sin run.md en disco se ignora en silencio (no es asunto del cierre). (5) El test no clona ni corre el CLI de sldb: comprueba con git (git ls-files o git cat-file -e HEAD:<path>) que despues del cierre todo path de RunDoc de store.yaml esta en HEAD; el done_when sobre stores build se lee asi. (6) El sandbox es un repo git con commit base: la fixture repo/lifecycle_desk de los tests de closeout ya lo da.

## Notas del coordinador

- Afecta la CI de graph_ui (nota 20261117-021713). closure.py cambió hace poco (63b519b2: el cierre ya incluye desk/reviews/<tarea>/): parte de HEAD.
- Mutaciones de desk y git en tests: solo sandbox (tmp_path).
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
