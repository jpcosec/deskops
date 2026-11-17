# Encargo del ejecutor deskops-e-519848b776fc (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-deskops-view-task-entrega-holds-true-en-un-gate-cuya-regla-de-activacion-da-un-finding-de-error`

Contrato: `deskops show task task-deskops-view-task-entrega-holds-true-en-un-gate-cuya-regla-de-activacion-da-un-finding-de-error --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las "Precisiones del preflight 1" del scope y las precisiones del coordinador de abajo son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`. El PYTHONPATH es obligatorio: el venv tiene deskops editable desde /mnt/ssd/herramientas/deskops y los tests que lanzan `python -m deskops` en subproceso probarían ese checkout y no este.
- Si la tarea agrega o cambia un comando del CLI, corre también tests/test_command_registry.py (pedido del integrador wA:p1): un comando que escribe desk, store o git se declara mutates=True en el registro y en MUTATING_COMMANDS del test.
- NO corras la suite completa ni `stores build --check` (orden del integrador wA:p1: los corre él una vez por integración en una copia limpia; el lock /dev/shm/sldb1-tests.lock es el cuello de botella). Tu validación son los tests de la Validation de la tarea, de a un archivo y sin lock. Si un comando de la Validation pide la suite completa, no lo corras: anótalo en result-summary.md como "para el integrador".
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-519848b776fc/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Precisiones del coordinador (recibos preflight-1 y bundle-1)

Precisiones del coordinador (preflight 1 y bundle 1): (1) Atribucion a sldb si el frame mas interno de codigo propio esta en el paquete sldb; si nace en deskops se arregla en deskops. La nota a sldb lleva la reproduccion minima y el reason del xfail(strict=True) es el nombre de archivo que imprime message send. (2) La reproduccion se registra con deskops review record <tarea> --kind reproduction --evidence <logs en runs/subagents/repro-holds-<AAAAMMDD>/> --reason '...' --root . (3) El escenario es un desk sandbox (fixture lifecycle_desk) con una tarea task.code sin recibos de preflight; la tarea de este arreglo es task.debug, la del escenario es task.code. (4) Fuente de verdad: holds es false cuando el gate tiene al menos un finding de nivel error; los findings se siguen mostrando igual. (5) El test nuevo usa tmp_path/sandbox. (6) La regla vive en desk/lifecycle/rule-activation-task-code.md y el gate es la transicion task_activates hacia ritual-testing del ciclo de vida. Esta tarea va en dos fases: primero la reproduccion y su recibo; el arreglo despues de que el coordinador acepte la reproduccion.

## Notas del coordinador: FASE 1 (solo reproducción)

- Esta tarea es task.debug y va en dos fases. En ESTA fase solo reproduces: NO toques código de deskops/ ni sldb/ todavía.
- Construye el escenario en un sandbox (precisión 3) y deja en runs/subagents/repro-holds-20261117/ los logs. Deben mostrar `deskops view task <tarea del sandbox> --format json` con un gate `holds: true` y un finding de nivel error, más el traceback o la ubicación del código que calcula holds. Agrega tu atribución (deskops o sldb, precisión 1) con el frame y el archivo:línea.
- Registra el recibo con `deskops review record <esta tarea> --kind reproduction --evidence <ruta de los logs> --reason '<resumen de la reproducción y la atribución>' --root .` (precisión 2). No lo dispongas: lo acepta el coordinador.
- Escribe result-summary.md (fase 1) y git-status.txt, y termina con `REPRODUCCION LISTA` (o `BLOQUEADO: <motivo>`). Después espera: cuando el coordinador acepte el recibo te dirá "sigue" en esta misma conversación y harás el arreglo con su test. Al terminar el arreglo, reescribe result-summary.md y git-status.txt, y termina con `ENTREGA LISTA`.
- Mutaciones de desk en tests: solo sandbox (tmp_path). Lista cada archivo tocado y explica cualquiera fuera de files.
