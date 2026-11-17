# Encargo del ejecutor deskops-e-3cd90f55821f (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-closeout-commit-no-amienda-un-commit-que-la-tarea-cita-como-evidencia-de-commit`

Contrato: `deskops show task task-closeout-commit-no-amienda-un-commit-que-la-tarea-cita-como-evidencia-de-commit --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las precisiones del coordinador de abajo son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`. El PYTHONPATH es obligatorio: el venv tiene deskops editable desde /mnt/ssd/herramientas/deskops y los tests que lanzan `python -m deskops` en subproceso probarían ese checkout y no este.
- Si la tarea agrega o cambia un comando del CLI, corre también tests/test_command_registry.py (pedido del integrador wA:p1): un comando que escribe desk, store o git se declara mutates=True en el registro y en MUTATING_COMMANDS del test.
- NO corras la suite completa ni `stores build --check` (orden del integrador wA:p1: los corre él una vez por integración en una copia limpia; el lock /dev/shm/sldb1-tests.lock es el cuello de botella). Tu validación son los tests de la Validation de la tarea, de a un archivo y sin lock. Si un comando de la Validation pide la suite completa, no lo corras: anótalo en result-summary.md como "para el integrador".
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-3cd90f55821f/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Precisiones del coordinador (recibos preflight-1 y bundle-1)

Precisiones del coordinador (preflight 1): (1) references guarda cada sha como un string suelto de la lista (por ejemplo '626db5e2'). El recibo es desk/reviews/<tarea>/evidence-commit-<n>.md (ReviewDoc con kind evidence, fact commit, value = sha completo y verdict accepted). Aceptado = verdict accepted. (2) Coincidencia: un item de references cuenta si es hex en minusculas de 7 o mas caracteres y el sha completo del HEAD empieza con el; el value del recibo se compara entero. (3) El test sigue el estilo de tests/test_closeout.py (desk sandbox en tmp_path y la misma forma de invocar verify y commit que usan sus tests de closeout commit).
Precisiones del coordinador (bundle 1), ademas de las del preflight 1: (3) tests/test_closeout_declared_evidence.py ya existe; solo se corre. (4) resolved-by existe (closure.py, Closeout-Mode: resolved-by); fuera de alcance quiere decir que no cambia. (5) El sha se busca solo en references y en los recibos evidence-commit; no en history ni en el cuerpo.

## Notas del coordinador

- URGENTE (pedido del supervisor). Mutaciones de desk y git en tests: solo sandbox (tmp_path).
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
