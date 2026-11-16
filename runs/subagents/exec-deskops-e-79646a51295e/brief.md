# Encargo del ejecutor deskops-e-79646a51295e (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-desk-update-migra-las-claves-legacy-checklists-y-routine-del-frontmatter-de-las-tareas-para-que-supe`

Contrato: `deskops show task task-desk-update-migra-las-claves-legacy-checklists-y-routine-del-frontmatter-de-las-tareas-para-que-supe --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las "Precisiones del preflight 1" del scope y las precisiones del coordinador de abajo son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`.
- La suite completa va UNA vez al final y bajo lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && flock /dev/shm/sldb1-tests.lock env TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests`. Si algo falla, aplica el criterio de la validation de la tarea (worktree limpio de origin/main en /dev/shm/wt-base, removerlo al terminar).
- Antes de correr la suite completa, `free -g`: si "available" es menor que 8, espera y vuelve a mirar.
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-79646a51295e/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Precisiones del coordinador (forman parte del contrato; están en los recibos preflight-2 y bundle-2)

Precisiones del coordinador (preflight-2): (1) dry-run: una linea por clave pendiente, '<ruta relativa a la raiz>: legacy frontmatter key <clave>', dentro del bloque de reporte de desk update. (2) Orden: archivos en orden de ruta y, dentro de cada archivo, checklists antes que routine. (3) El valor anterior se serializa con json.dumps(valor, ensure_ascii=False, default=str, separators=(',', ':')). (4) Un TaskDoc ilegible o con frontmatter malformado no se toca y se reporta como hoy los invalid_tasks de desk update; no aborta el resto de la migracion.

## Notas del coordinador

- PRIORIDAD 1: desbloquea a marcado, donde closeout supersede se niega a reescribir 3 tareas legacy con las claves checklists y routine (nota 20261116-103216 en desk/inbox/).
- No migres el desk real de deskops: las mutaciones de desk en tests van solo en desks sandbox (tmp_path). Reproduce el caso de marcado (TaskDoc con checklists y routine en el frontmatter) en un desk sandbox.
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
- Las 3 fallas de entorno conocidas de la suite (rc 127: e2e first-task-to-closeout y 2 de test_ci_integration) se aceptan si fallan igual en origin/main.
