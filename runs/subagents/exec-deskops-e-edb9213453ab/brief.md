# Encargo del ejecutor deskops-e-edb9213453ab (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-puente-de-pytest-en-deskops-para-que-un-test-py-corra-una-suite-de-otro-lenguaje-vitest-go-test-y-fa`

Contrato: `deskops show task task-puente-de-pytest-en-deskops-para-que-un-test-py-corra-una-suite-de-otro-lenguaje-vitest-go-test-y-fa --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las "Precisiones del preflight 1" son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`.
- La suite completa va UNA vez al final y bajo lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && flock /dev/shm/sldb1-tests.lock env TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests`. Si algo falla, aplica el criterio de la validation de la tarea (worktree limpio de origin/main en /dev/shm/wt-base, removerlo al terminar).
- Antes de correr la suite completa, `free -g`: si "available" es menor que 8, espera y vuelve a mirar.
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-edb9213453ab/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.

## Precisiones del coordinador (forman parte del contrato; están en los recibos preflight-1 y bundle-1)

Precisiones del coordinador (preflight-1): (1) 200 lineas por flujo: primero las ultimas 200 de stdout y despues las ultimas 200 de stderr, cada bloque con su rotulo. (2) Encontrar el comando para correr el .py desde un repo sin venv propio es parte de la tarea: debe usar la instalacion de deskops de la maquina, la forma de partida es uv run --no-project --with pytest --with-editable /mnt/ssd/herramientas/deskops python -m pytest -q tests/test_vitest_suite.py, y se documenta el que se compruebe a mano en una copia en /dev/shm de un repo sin Python (si ese no funciona, el que si funcione, con la salida en el informe). (3) Empaquetado: deskops/testing/__init__.py basta si setuptools packages.find ya lo incluye; pyproject.toml se toca solo si una instalacion de prueba muestra que el paquete no entra; pytest no pasa a dependencia de runtime (el modulo solo se usa bajo pytest). (4) El desk sandbox y la llamada a closeout verify se arman con los fixtures y helpers que ya usa tests/test_closeout_gates.py (bare_desk / store_desk).
Precisiones del coordinador (bundle-1): (1), (3) y (4) como en el preflight-1: 200 lineas por flujo (stdout y despues stderr, rotulados); el comando sin venv propio se encuentra, se comprueba a mano y se documenta; pyproject.toml solo si una instalacion de prueba muestra que hace falta. (2) La suite vitest de sldb-ui estaba verde segun su tester (34 archivos, 219 tests). Si el smoke falla, se registran el rc y la salida y se informa como bloqueo con la causa: no se busca otra suite ni se da por pasado. (5) env provisto reemplaza el entorno entero, como en subprocess; quien llama mezcla os.environ si lo necesita.

## Notas del coordinador

- PRIORIDAD 1: desbloquea el cierre de sldb-ui, marcado-ui y scion. Decisión de JP: NO se toca deskops/services/closeout_gates.py ni ningún gate; el diff no puede tocarlo.
- Contexto: un intento anterior que cambiaba el gate se abortó (runs/subagents/exec-deskops-e-e75ce6f704e3/aborted-diff.patch). No lo uses como base.
- El smoke contra UIs/sldb-ui solo lee ese repo: no escribas en él (vitest puede dejar caché en node_modules, eso se acepta). Su archivo de test va en /dev/shm, no en sldb-ui.
- Mutaciones de deskops en tests: solo desks sandbox (tmp_path).
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
- Las 3 fallas de entorno conocidas de la suite (rc 127: e2e first-task-to-closeout y 2 de test_ci_integration) se aceptan si fallan igual en origin/main. Antes de la suite mira free -g y espera si "available" está por debajo de 8.
