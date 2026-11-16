# Encargo del ejecutor deskops-e-312954356a7f (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc`

Contrato: `deskops show task task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las "Precisiones del preflight 1" son parte del contrato. Atomos ligados: los del campo atoms; pill ligada: pill-materialization-contracts-declare-source-intent-and-target (desk/contexts/).

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`.
- La suite completa va UNA vez al final y bajo lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && flock /dev/shm/sldb1-tests.lock env TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests`. Si algo falla, aplica el criterio de la validation de la tarea (worktree limpio de origin/main en /dev/shm/wt-base, removerlo al terminar).
- Antes de correr la suite completa, `free -g`: si "available" es menor que 8, espera y vuelve a mirar.
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-312954356a7f/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.

## Notas del coordinador

- El paso 4 (nota a sldb) es parte del contrato: si graph missing en el desk sandbox reporta missing_declared_target para un target directorio, mándala con `deskops message send --to sldb ...` con el título y el cuerpo que fija la precisión del preflight, y anota en result-summary.md el id de la nota que te devuelva el comando. Si no falla, dilo con la salida.
- Si tu cambio rompe goldens u otros tests existentes por una razón legítima, actualízalos a propósito y explica en result-summary.md por qué.
- Lista en result-summary.md cada archivo que tocaste. Si alguno no está en el campo files de la tarea, explica por qué.
