# Encargo del ejecutor deskops-e-bae0befe2582 (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-desk-update-deja-de-exigir-desk-reviews-vacio-y-en-un-clon-limpio-el-dry-run-da-rc-0`

Contrato: `deskops show task task-desk-update-deja-de-exigir-desk-reviews-vacio-y-en-un-clon-limpio-el-dry-run-da-rc-0 --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las "Precisiones del preflight 1" son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`.
- La suite completa va UNA vez al final y bajo lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && flock /dev/shm/sldb1-tests.lock env TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests`. Si algo falla, aplica el criterio de la validation de la tarea (worktree limpio de origin/main en /dev/shm/wt-base, removerlo al terminar).
- Antes de correr la suite completa, `free -g`: si "available" es menor que 8, espera y vuelve a mirar.
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-bae0befe2582/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.

## Notas del coordinador

- El test del clon limpio usa tmp_path y subprocess, nunca el repo real. Las mutaciones de deskops van sobre desks sandbox.
- Si tu cambio rompe goldens u otros tests existentes por una razón legítima, actualízalos a propósito y explica en result-summary.md por qué.
- Lista en result-summary.md cada archivo que tocaste. Si alguno no está en el campo files de la tarea, explica por qué.
- La suite completa corre con el venv del repo. Sus 3 fallas conocidas de entorno (rc 127: python o pytest no están en el PATH; están en e2e first-task-to-closeout y en test_ci_integration) se aceptan si fallan igual en origin/main.
