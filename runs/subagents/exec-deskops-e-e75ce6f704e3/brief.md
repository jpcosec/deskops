# Encargo del ejecutor deskops-e-e75ce6f704e3 (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-el-closeout-acepta-tests-de-otros-lenguajes-y-evidencia-de-commit-de-otro-repo-registrado`

Contrato: `deskops show task task-el-closeout-acepta-tests-de-otros-lenguajes-y-evidencia-de-commit-de-otro-repo-registrado --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las "Precisiones del preflight 1" son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`.
- La suite completa va UNA vez al final y bajo lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && flock /dev/shm/sldb1-tests.lock env TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests`. Si algo falla, aplica el criterio de la validation de la tarea (worktree limpio de origin/main en /dev/shm/wt-base, removerlo al terminar).
- Antes de correr la suite completa, `free -g`: si "available" es menor que 8, espera y vuelve a mirar.
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-e75ce6f704e3/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.

## Precisiones del coordinador (forman parte del contrato; están en los recibos preflight-5 y bundle-3)

(1) el test no-.py cuenta si esta en files o en references y existe bajo la raiz del desk; para los sufijos nuevos no rige la condicion de directorio tests/. (2) --test de resolved-by: ruta relativa a --root que existe, con test_*.py o un sufijo de la lista cerrada, sin condicion de tests/. (3) El registro del ecosistema es el que resuelve find_registered_desk (deskops/identity.py), reutilizado; primero el registro del desk y despues el del ecosistema, gana el primero que resuelve; si el repo-id no resuelve o es ambiguo, la referencia no cuenta (sin excepcion). (4) El punto de integracion (firma de RepositoryReferences y sus llamadores) lo elige el ejecutor dentro de closeout_gates.py y closure.py. (5) La doc va en la seccion de docs/workflow-policy-reference.md que ya describe la evidencia de tests y de commit del closeout. (6) Las dos notas, a scion y a marcado-ui, son requisito de cierre. (7) La primera linea del log empieza literalmente con '$ ', sin espacios delante. (8) Los sufijos son literales y distinguen mayusculas; *.test.ts y *.test.tsx son entradas separadas.

## Notas del coordinador

- PRIORIDAD 1: esta tarea desbloquea el cierre de sldb-ui, marcado-ui y scion.
- Las notas a scion y a marcado-ui (paso 6) llevan el hash del commit de cierre, que todavía no existe. NO las mandes tú: deja en result-summary.md el texto exacto de cada nota, con un marcador <SHA>, y las manda el coordinador después del commit.
- Mutaciones de deskops en tests: solo desks sandbox (tmp_path). Para el registro del ecosistema en los tests usa un registro sandbox (variable o fixture que ya use find_registered_desk), nunca ~/setup/desk/registry real.
- Si rompes goldens u otros tests por una razón legítima, actualízalos a propósito y explícalo. Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
- Las 3 fallas de entorno conocidas de la suite (rc 127: e2e first-task-to-closeout y 2 de test_ci_integration) se aceptan si fallan igual en origin/main. Antes de la suite, mira free -g y espera si "available" está por debajo de 8.
