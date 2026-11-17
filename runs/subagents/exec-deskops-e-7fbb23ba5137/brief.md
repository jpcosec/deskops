# Encargo del ejecutor deskops-e-7fbb23ba5137 (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-closeout-verify-escribe-un-recibo-nuevo-cuando-el-veredicto-cambia-aunque-el-input-sea-el-mismo`

Contrato: `deskops show task task-closeout-verify-escribe-un-recibo-nuevo-cuando-el-veredicto-cambia-aunque-el-input-sea-el-mismo --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las precisiones del coordinador de abajo son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`. El PYTHONPATH es obligatorio: el venv tiene deskops editable desde /mnt/ssd/herramientas/deskops y los tests que lanzan `python -m deskops` en subproceso probarían ese checkout y no este.
- Si la tarea agrega o cambia un comando del CLI, corre también tests/test_command_registry.py (pedido del integrador wA:p1): un comando que escribe desk, store o git se declara mutates=True en el registro y en MUTATING_COMMANDS del test.
- NO corras la suite completa ni `stores build --check` (orden del integrador wA:p1: los corre él una vez por integración en una copia limpia; el lock /dev/shm/sldb1-tests.lock es el cuello de botella). Tu validación son los tests de la Validation de la tarea, de a un archivo y sin lock. Si un comando de la Validation pide la suite completa, no lo corras: anótalo en result-summary.md como "para el integrador".
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-7fbb23ba5137/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Precisiones del coordinador (recibos preflight-1 y bundle-1)

Precisiones del coordinador (preflight 1): (1) Intacto es lo que ya usa el codigo: el review_id no esta en self._not_intact_documents(). Con varios recibos del mismo fact e input, se salta solo si alguno intacto tiene el mismo verdict que el nuevo; si no, se escribe uno nuevo. (2) El test puede ir al nivel del servicio: dos llamadas a la escritura de recibos con el mismo fact e items y verdicts distintos (rejected y luego accepted), mas una comprobacion de que la regla de closeout ve el accepted. (3) verdict es el campo verdict del payload del ReviewDoc. (4) Un commit real en el desk sandbox es valido (otros tests de closeout lo hacen).
Precisiones del coordinador (bundle 1), ademas de las del preflight 1: (1) Intacto como en el preflight 1. (2) Ver la precision 2 del preflight 1. (3) Simetrico: cualquier cambio de verdict con el mismo input escribe un recibo nuevo.

## Notas del coordinador

- URGENTE (pedido del supervisor). Mutaciones de desk y git en tests: solo sandbox (tmp_path).
- closure.py acaba de cambiar en 0181c530 (no amendar un HEAD citado): parte de HEAD actual.
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
