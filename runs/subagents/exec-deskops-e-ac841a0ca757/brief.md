# Encargo del ejecutor deskops-e-ac841a0ca757 (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-los-selectores-de-deskops-aceptan-una-ruta-desk-y-el-error-explica-que-formas-acepta`

Contrato: `deskops show task task-los-selectores-de-deskops-aceptan-una-ruta-desk-y-el-error-explica-que-formas-acepta --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las "Precisiones del preflight 1" son parte del contrato. Atomos ligados: los del campo atoms; pill ligada: pill-operational-cli-grammar-follows-spoken-workflow (desk/contexts/).

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`.
- La suite completa va UNA vez al final y bajo lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && flock /dev/shm/sldb1-tests.lock env TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests`. Si algo falla, aplica el criterio de la validation de la tarea (worktree limpio de origin/main en /dev/shm/wt-base, removerlo al terminar).
- Antes de correr la suite completa, `free -g`: si "available" es menor que 8, espera y vuelve a mirar.
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-ac841a0ca757/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.

## Notas del coordinador

- Las mutaciones de deskops en los tests van sobre desks sandbox (tmp_path), nunca sobre el desk real.
- El golden de ayuda tests/fixtures/golden/help/deskops_edit_task.txt está en el scope aunque no figure en files. Si tu cambio rompe otros goldens o tests por una razón legítima, actualízalos a propósito y explica por qué en result-summary.md.
- Lista en result-summary.md cada archivo que tocaste. Si alguno no está en el campo files de la tarea, explica por qué.
- Las 3 fallas de entorno conocidas de la suite (rc 127, sin python/pytest en el PATH: e2e first-task-to-closeout y 2 de test_ci_integration) se aceptan si fallan igual en origin/main.
- La máquina anda corta de RAM: antes de la suite completa mira free -g y espera si "available" está por debajo de 8.
