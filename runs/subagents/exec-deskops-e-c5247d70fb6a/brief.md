# Encargo del ejecutor deskops-e-c5247d70fb6a (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-se-retiran-del-drawer-los-planes-workspace-documental-gates-por-tipo-deskops-ui-y-deskops-como-confi`

Contrato: `deskops show task task-se-retiran-del-drawer-los-planes-workspace-documental-gates-por-tipo-deskops-ui-y-deskops-como-confi --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las precisiones del coordinador de abajo son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`. El PYTHONPATH es obligatorio: el venv tiene deskops editable desde /mnt/ssd/herramientas/deskops y los tests que lanzan `python -m deskops` en subproceso probarían ese checkout y no este.
- Si la tarea agrega o cambia un comando del CLI, corre también tests/test_command_registry.py (pedido del integrador wA:p1): un comando que escribe desk, store o git se declara mutates=True en el registro y en MUTATING_COMMANDS del test.
- NO corras la suite completa ni `stores build --check` (orden del integrador wA:p1: los corre él una vez por integración en una copia limpia; el lock /dev/shm/sldb1-tests.lock es el cuello de botella). Tu validación son los tests de la Validation de la tarea, de a un archivo y sin lock. Si un comando de la Validation pide la suite completa, no lo corras: anótalo en result-summary.md como "para el integrador".
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-c5247d70fb6a/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Precisiones del coordinador (recibos preflight-1 y bundle-1)

Precisiones del coordinador (preflight 1 y bundle 1): (1) El fixture tests/fixtures/plans/gates-por-tipo/ es el minimo con el que pasan tests/test_review_command.py y tests/test_review_doc.py: incluye cada nodo que los tests nombran (ROOT, PC01, GC01, GC02, GC03 y los que el ejecutor encuentre al leerlos) y brief.md (el test lo reescribe), copiados del plan real antes de borrarlo. (2) Los literales de tests/test_review_doc.py (por ejemplo 'desk/drawer/plans/gates-por-tipo/dag.yaml#node:GC02') son valores de validacion del modelo, no leen archivos: se dejan como estan. (3) La ruta de ejemplo de registry.py y de docs/operator-manual.md pasa a 'desk/drawer/plans/mi-plan N01' (y 'desk/drawer/plans/mi-plan' donde no hay nodo). (4) Goldens de ayuda afectados: tests/fixtures/golden/help/deskops_review.txt, deskops_review_node.txt y deskops_review_status.txt; se regeneran solo esos. (5) En docs/deskops-ui.md la cita pasa a 'Copiado del alcance del plan deskops-ui (2026-11-04; plan retirado del drawer el 2026-11-17, queda en el historial de git).' (6) Linea base de graph missing: 35 entradas en HEAD antes del cambio; despues no puede haber mas.

## Notas del coordinador

- Pedido del supervisor (triaje del drawer). Cada nodo de los 4 planes ya tiene su recibo de review node dispuesto en desk/reviews/deskops-<plan>-<nodo>/: no los toques.
- Esta tarea SÍ borra archivos de desk/drawer/ con git rm (los 4 planes y desk/drawer/tasks/workspace-documental): es la excepción a "no toques desk/". Nada más de desk/ ni de .sldb/. No hagas git commit: deja los git rm en el índice o en el árbol; el coordinador commitea.
- Antes de borrar, copia el fixture y comprueba los tests con el plan real todavía presente.
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
