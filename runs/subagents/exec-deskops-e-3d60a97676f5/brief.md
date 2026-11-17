# Encargo del ejecutor deskops-e-3d60a97676f5 (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo`

Contrato: `deskops show task task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las precisiones del coordinador de abajo son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`. El PYTHONPATH es obligatorio: el venv tiene deskops editable desde /mnt/ssd/herramientas/deskops y los tests que lanzan `python -m deskops` en subproceso probarían ese checkout y no este.
- Si la tarea agrega o cambia un comando del CLI, corre también tests/test_command_registry.py (pedido del integrador wA:p1): un comando que escribe desk, store o git se declara mutates=True en el registro y en MUTATING_COMMANDS del test.
- NO corras la suite completa ni `stores build --check` (orden del integrador wA:p1: los corre él una vez por integración en una copia limpia; el lock /dev/shm/sldb1-tests.lock es el cuello de botella). Tu validación son los tests de la Validation de la tarea, de a un archivo y sin lock. Si un comando de la Validation pide la suite completa, no lo corras: anótalo en result-summary.md como "para el integrador".
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-3d60a97676f5/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Precisiones del coordinador (recibos preflight-1 y bundle-1)

Precisiones del coordinador (preflight 1): (1) El patron vive solo en deskops/models/review.py (SUBJECT_REF_PATTERN, usado como pattern del campo subject_ref de ReviewDoc); .sldb/core/models/ReviewDoc.yaml no declara pattern, asi que no hay nada que tocar ahi. (2) REVIEW_ID_PATTERN ya admite cualquier caracter en el medio (review-.+-node-N) y el review_id se arma con node_id.lower() en deskops/services/review.py, asi que el punto no choca; si el ejecutor ve que choca, lo dice en result-summary.md, sin cambiar el formato. (3) El pi falso es la fixture fake_pi de tests/test_review_command.py (linea 74) y el desk sandbox es la fixture lifecycle_desk de tests/conftest.py; el test de review node existente (test_node_writes_one_review_doc_per_node) muestra como se usan. (4) El dag.yaml de prueba se escribe dentro del sandbox en desk/drawer/plans/<nombre>/dag.yaml con la estructura minima que acepta review node (ROOT con children y un nodo con id con punto); el ejecutor la toma del plan gates-por-tipo.
Precisiones del coordinador (bundle 1), ademas de las del preflight 1: (1) Ver la precision 1 del preflight. (2) Casos rechazados del test: un id con espacio ('#node:WS 13') y un segundo '#' ('#node:WS13#x'). (3) Ver la precision 2 del preflight: el resultado es result-summary.md del ejecutor.

## Notas del coordinador

- No corras deskops review node sobre los planes reales del drawer (lo hace el coordinador después, bajo /dev/shm/pi-review.lock). Solo sandbox con fake_pi.
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
