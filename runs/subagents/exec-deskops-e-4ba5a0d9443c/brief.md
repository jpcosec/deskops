# Encargo del ejecutor deskops-e-4ba5a0d9443c (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados`

Contrato: `deskops show task task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las precisiones del coordinador de abajo son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`.
- NO corras la suite completa ni `stores build --check` (orden del integrador wA:p1: los corre él una vez por integración en una copia limpia; el lock /dev/shm/sldb1-tests.lock es el cuello de botella). Tu validación son los tests de la Validation de la tarea, de a un archivo y sin lock. Si un comando de la Validation pide la suite completa, no lo corras: anótalo en result-summary.md como "para el integrador".
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-4ba5a0d9443c/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Precisiones del coordinador (forman parte del contrato; están en los recibos preflight-1 y bundle-1)

Precisiones del coordinador (preflight 1): (1) El ensanchamiento es intencional: bajo docs/architecture valen los mismos sufijos que hoy valen bajo docs/architecture/spec2viz (.md, .yaml, .yml), sin excluir Markdown; la precedencia entre FILE_RULES y DocumentSurfaces queda como esta. (2) El retirement check de IR es contexto: esta tarea no espera a nada ni lo corre. (3) Solo cambia la regla: no se mueve ni renombra ningun archivo (deskops no tiene docs/architecture). (4) sldb notations sync es contexto de la decision de JP; la tarea no ejecuta ese comando ni depende de el.
Precisiones del coordinador (bundle 1), ademas de las del preflight 1: (1) El ejecutor elige el nombre de la funcion de test nueva, siguiendo el estilo de las del archivo (test_<lo que comprueba>). (2) El ejecutor elige el subdirectorio y el nombre del YAML del sandbox; cualquier subdirectorio de docs/architecture sirve. (3) test_graph_snapshot.py y test_graph_missing_existing_files.py solo se corren; si alguno falla por este cambio, el ejecutor para y lo informa como bloqueo en vez de modificarlo.

## Notas del coordinador

- Pedido de IR13 (retiro de spec2viz). Después de esto, grep de spec2viz en deskops/graph/desk_graph.py debe dar vacío.
- Mutaciones de desk en tests: solo desks sandbox (tmp_path).
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
