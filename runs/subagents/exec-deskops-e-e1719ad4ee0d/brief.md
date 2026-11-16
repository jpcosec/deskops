# Encargo del ejecutor deskops-e-e1719ad4ee0d (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-deskops-quita-el-enlace-federado-al-store-de-spec2viz-de-su-sldb-g5-opcion-b-de-jp`

Contrato: `deskops show task task-deskops-quita-el-enlace-federado-al-store-de-spec2viz-de-su-sldb-g5-opcion-b-de-jp --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las precisiones del coordinador de abajo son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`.
- NO corras la suite completa ni `stores build --check` (orden del integrador wA:p1: los corre él una vez por integración en una copia limpia; el lock /dev/shm/sldb1-tests.lock es el cuello de botella). Tu validación son los tests de la Validation de la tarea, de a un archivo y sin lock. Si un comando de la Validation pide la suite completa, no lo corras: anótalo en result-summary.md como "para el integrador".
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-e1719ad4ee0d/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Precisiones del coordinador (forman parte del contrato; están en los recibos preflight-1 y bundle-1)

Precisiones del coordinador (preflight-1): (1) El run dir es el del ejecutor, runs/subagents/exec-<id>/, con antes-stores-check.txt, antes-doctor.txt, antes-graph-missing.txt y sus pares despues-*.txt, en texto plano con la salida y el rc. (2) Un test se rompe legitimamente si pasa en el worktree limpio de origin/main, falla con el cambio y su asercion depende del enlace spec2viz del store real; cada uno se nombra y se justifica en el informe. Cualquier otra falla nueva bloquea. (3) Comparacion por conjunto de lineas de hallazgo: es nuevo el que aparece despues y no antes; el informe da los conteos antes y despues y lista los nuevos y los que desaparecen.
Precisiones del coordinador (bundle-1): (1) La semantica system.spec2viz del modelo ViewDoc (model_ref sldb.models.notation_models:ViewDoc, viene del paquete sldb) es una etiqueta, no una dependencia del store de spec2viz; no se toca. (2), (3) y (4) como en el preflight-1: legitimo = pasa en origin/main limpio, falla con el cambio y su asercion depende del enlace spec2viz del store real; run dir runs/subagents/exec-<id>/ con antes-*.txt y despues-*.txt; comparacion por conjunto de lineas de hallazgo. (5) tests/test_migrate_desk_stores.py solo se corre; se modifica solo si se rompe legitimamente segun (2). (6) La herencia la detecta el propio sldb stores remove (rechaza mientras un modelo de aqui hereda del store enlazado); antes se mira con grep '../spec2viz' en .sldb/core/models, y si stores remove rechaza, se para y se informa.

## Notas del coordinador

- URGENTE: esta tarea bloquea a IR (task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opcion-a). Decisión de JP (opción b).
- Sin suite completa (ver Reglas): para el criterio (2) de las precisiones, corre de a uno y sin lock los tests de la Validation y los que se rompan; para cada test que falle con el cambio, compruébalo en un worktree limpio de origin/main en /dev/shm/wt-base (git worktree add /dev/shm/wt-base origin/main; git worktree remove /dev/shm/wt-base al terminar). sldb stores check, deskops doctor y deskops graph missing sí se corren (no son build --check).
- El texto de la tarea cita "deskops/.sldb/store.yaml": es .sldb/store.yaml de este repo (la ruta está escrita relativa a SLDB_1). graph missing ya lo marca como hallazgo antes del cambio; no cuenta como nuevo.
- El cambio del store lo hace el comando sldb stores remove spec2viz --store .sldb; no edites .sldb a mano.
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
