# Encargo del ejecutor deskops-e-2ea9647a5250 (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-deskops-review-puede-correr-con-un-runtimeprofiledoc-de-claude-cuando-pi-no-esta-disponible`

Contrato: `deskops show task task-deskops-review-puede-correr-con-un-runtimeprofiledoc-de-claude-cuando-pi-no-esta-disponible --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las "Precisiones del preflight 1" del scope son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`. El PYTHONPATH es obligatorio: el venv tiene deskops editable desde /mnt/ssd/herramientas/deskops y los tests que lanzan `python -m deskops` en subproceso probarían ese checkout y no este.
- Si la tarea agrega o cambia un comando del CLI, corre también tests/test_command_registry.py (pedido del integrador wA:p1): un comando que escribe desk, store o git se declara mutates=True en el registro y en MUTATING_COMMANDS del test.
- NO corras la suite completa ni `stores build --check` (orden del integrador wA:p1: los corre él una vez por integración en una copia limpia; el lock /dev/shm/sldb1-tests.lock es el cuello de botella). Tu validación son los tests de la Validation de la tarea, de a un archivo y sin lock. Si un comando de la Validation pide la suite completa, no lo corras: anótalo en result-summary.md como "para el integrador".
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-2ea9647a5250/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Notas del coordinador

- Lee el pill ligado (campo pills) si lo hay.
- No lances un modelo real (ni pi ni claude) desde los tests: usa los dobles de prueba que ya usa tests/test_review_command.py (fake_pi y similares). Las revisiones reales de pi del coordinador corren bajo /dev/shm/pi-review.lock: no lo tomes.
- Mutaciones de desk en tests: solo desks sandbox (tmp_path).
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
