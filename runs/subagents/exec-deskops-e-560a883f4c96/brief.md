# Encargo del ejecutor deskops-e-560a883f4c96 (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi`

Contrato: `deskops show task task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las precisiones del coordinador de abajo son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`.
- NO corras la suite completa ni `stores build --check` (orden del integrador wA:p1: los corre él una vez por integración en una copia limpia; el lock /dev/shm/sldb1-tests.lock es el cuello de botella). Tu validación son los tests de la Validation de la tarea, de a un archivo y sin lock. Si un comando de la Validation pide la suite completa, no lo corras: anótalo en result-summary.md como "para el integrador".
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-560a883f4c96/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Precisiones del coordinador (forman parte del contrato; están en los recibos preflight-1 y bundle-1)

Precisiones del coordinador (preflight 1):
(1) Aislamiento del registro en tests: la variable de entorno DESKOPS_ECOSYSTEM_REGISTRY (ECOSYSTEM_REGISTRY_ENV de deskops/identity.py, leída por ecosystem_registry_dir) apuntando a un directorio registry dentro de tmp_path; en tests en proceso con monkeypatch.setenv, en subprocesos con env (patrón de tests/test_message_ecosystem_registry.py). Nunca ~/setup/desk/registry.
(2) "El registro del desk" es desk/registry/repo-*.md del desk bajo --root (las entries que ya recibe RepositoryReferences). Si el repo-id no está ahí, se busca en el registro del ecosistema (load_ecosystem_registry / find_registered_desk). El registro local gana si están en ambos.
(3) "Alcanzable" es exactamente el criterio de reference_points_to_commit: id hex en minúsculas, git rev-parse --verify <sha>^{commit} en el repo de ese repo-id, y ancestro de su HEAD. Reutiliza esa función (CloseoutGatesService sobre la raíz de ese repo), no la dupliques.
(4) Doc: subsección nueva "Commit evidence from another repository" dentro de "Closeout rules" de docs/workflow-policy-reference.md, justo después de "Tests evidence from a suite in another language". Contenido: la forma <repo-id>:<sha>, el orden de resolución (registro local y luego ecosistema), el criterio de (3) y que una referencia que no resuelve no cuenta y no lanza excepción.
(5) La nota a scion la manda el coordinador después del closeout, con deskops message send --to scion, porque el hash solo existe entonces. El ejecutor no la manda; deja en result-summary.md un texto de 3 a 5 líneas para esa nota (qué cambió y cómo referenciar <repo-id>:<sha>).
Precisiones del coordinador (bundle 1), además de las del preflight 1 (que ya resuelven 1, 2 y 4: el registro local gana, DESKOPS_ECOSYSTEM_REGISTRY con tmp_path, la nota a scion la manda el coordinador):
(3) En resolved-by solo cambia --ref; --test queda como está.
(5) Si el root registrado no existe en la máquina, la referencia no cuenta como evidencia, sin excepción: verify la reporta como no encontrada con el mensaje de missing_root_message (comportamiento actual del registro local), y lo mismo para un repo resuelto por el ecosistema.

## Notas del coordinador

- La nota de inbox desk/inbox/20261116-163831-suggestion-closeout-resolved-by-y-gates-los-calificadores-repo-id-solo-leen-desk-registry-del-propio-desk-no-el-registro-del-ecosistema.md (de otra sesión) describe el mismo hueco; léela como contexto.
- La doc va en una subsección nueva "Commit evidence from another repository" justo después de "Tests evidence from a suite in another language" (ya existe; la agregó el puente de pytest, 3f613469).
- Mutaciones de desk y registros en tests: solo sandbox (tmp_path y DESKOPS_ECOSYSTEM_REGISTRY a un registro sandbox). Nunca ~/setup/desk/registry.
- NO toques el gate de tests (decisión de JP): solo la resolución del repo-id para la evidencia de commit y para resolved-by --ref.
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
