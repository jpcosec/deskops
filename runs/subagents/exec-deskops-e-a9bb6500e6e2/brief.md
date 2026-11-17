# Encargo del ejecutor deskops-e-a9bb6500e6e2 (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-valores-con-llaves-rompen-edit-task-message-send-y-closeout-reason-y-closeout-verify-escribe-recibos`

Contrato: `deskops show task task-valores-con-llaves-rompen-edit-task-message-send-y-closeout-reason-y-closeout-verify-escribe-recibos --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las precisiones del coordinador de abajo son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`. El PYTHONPATH es obligatorio: el venv tiene deskops editable desde /mnt/ssd/herramientas/deskops y los tests que lanzan `python -m deskops` en subproceso probarían ese checkout y no este.
- Si la tarea agrega o cambia un comando del CLI, corre también tests/test_command_registry.py (pedido del integrador wA:p1): un comando que escribe desk, store o git se declara mutates=True en el registro y en MUTATING_COMMANDS del test.
- NO corras la suite completa ni `stores build --check` (orden del integrador wA:p1: los corre él una vez por integración en una copia limpia; el lock /dev/shm/sldb1-tests.lock es el cuello de botella). Tu validación son los tests de la Validation de la tarea, de a un archivo y sin lock. Si un comando de la Validation pide la suite completa, no lo corras: anótalo en result-summary.md como "para el integrador".
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-a9bb6500e6e2/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Precisiones del coordinador (recibo preflight-3)

Precisiones del coordinador (preflight 3): (1) <run> es runs/subagents/repro-llaves-<AAAAMMDD>/ y los logs van ahi como repro-<caso>.log. (2) El origen es sldb si el frame mas interno de la excepcion es un archivo del paquete sldb (ruta que contiene /sldb/ bajo src o site-packages); si no, es deskops. (3) Se prueban una, dos y tres llaves de apertura seguidas, y las de cierre equivalentes. (4) En (b) la proyeccion desk/reviews/<tarea>/evidence-*.md entra en el mismo commit de cierre: el cierre no deja archivos sin commitear. (5) Primero se manda la nota con deskops message send --to sldb; message send imprime el nombre de archivo de la nota y ese nombre es el reason de un xfail(strict=True). (6) La raiz es el checkout /mnt/ssd/proyectos/SLDB_1/deskops (--root .); la reproduccion corre en su propio desk sandbox con su --root. (7) tests/test_output_goldens.py solo se corre, como regresion de las salidas.

## Notas del coordinador: tarea task.debug en DOS FASES

- URGENTE (pedido del supervisor; nota 20261116-165008 de sldb-ui: TemplateSyntaxError con '{{').
- FASE 1 (ahora): reproduce (a), (b) y (c) en un desk sandbox, guarda los logs en runs/subagents/repro-llaves-<AAAAMMDD>/ y registra el recibo con `deskops review record <tarea> --kind reproduction --evidence <logs> --reason "..." --root .` (en el checkout real: es el único write a desk/ que se te permite). Escribe en tu result-summary.md la reproducción y el origen (sldb o deskops) de cada caso, y termina tu turno con `REPRODUCCION LISTA`. NO toques código todavía: la regla de activación de task.debug pide que el coordinador acepte la reproducción antes del arreglo.
- FASE 2 (cuando el coordinador te diga "sigue"): el arreglo y los tests según el contrato; al final ENTREGA LISTA.
- Mutaciones de desk en tests: solo sandbox (tmp_path).
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
