# Encargo del ejecutor deskops-e-af97f091952a (intento 1)

Rol: `desk/roles/deskops-executor.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Implementas UNA tarea y entregas evidencia; no cierras, no commiteas, no ruteas.

## Tarea

`task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb`

Contrato: `deskops show task task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb --root .` (o el archivo en desk/tasks/). El goal, el scope, el implementation_path, la validation y el done_when de ese TaskDoc mandan; las precisiones del coordinador de abajo son parte del contrato. Atomos ligados: los del campo atoms.

## Reglas

- Trabajas en /mnt/ssd/proyectos/SLDB_1/deskops, rama main, sin worktree y sin crear ramas. Hay otras sesiones: no toques archivos fuera del scope ni desk/ ni .sldb/ (salvo lo que escriba un comando deskops de tu validación en un desk sandbox temporal).
- `export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add -A`, `--autostash`, `git commit`, `git push`, `git stash`.
- Tests puntuales de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`.
- NO corras la suite completa ni `stores build --check` (orden del integrador wA:p1: los corre él una vez por integración en una copia limpia; el lock /dev/shm/sldb1-tests.lock es el cuello de botella). Tu validación son los tests de la Validation de la tarea, de a un archivo y sin lock. Si un comando de la Validation pide la suite completa, no lo corras: anótalo en result-summary.md como "para el integrador".
- Si el contrato es ambiguo de verdad, para y escríbelo en result-summary.md como bloqueo; no inventes intención.

## Evidencia (en runs/subagents/exec-deskops-e-af97f091952a/)

- `validation.log`: cada comando de la validation con su salida y su rc.
- `result-summary.md`: qué cambiaste (archivos y por qué), resultado de cada validación, fallas de la suite comparadas con origin/main, riesgos.
- `task.txt`: salida de `deskops show task <id> --root .`; `board.txt`: salida de `deskops show board Board --root .`; `git-status.txt`: salida de `git status --short` al terminar.
- Al terminar, tu última línea en la conversación es `ENTREGA LISTA` o `BLOQUEADO: <motivo>`.


## Precisiones del coordinador (forman parte del contrato; están en los recibos preflight-1 y bundle-1)

Precisiones del coordinador (preflight 1): (1) La aserccion modelo es la que hoy hace re.fullmatch(r"doc:TaskCodeDoc:task-x@sha256:[0-9a-f]{64}", doc["subject"]) dentro de test_subject_is_pinned_and_the_anchor_is_intact (linea 266 en origin/main ee9bc3cd). (2) En test_a_short_selector_keys_and_anchors_receipts_on_the_full_task_id el id del ancla es el id COMPLETO de la tarea (la variable full del test), nunca el selector corto: el test existe justo para eso. (3) El alcance son exactamente las aserciones de igualdad sobre subject que hoy fallan (lineas 261, 363 y 371 de test_review_record.py y 165 de test_review_command.py en ee9bc3cd); un subject de otro modelo o id no se toca. (4) Redaccion libre del ejecutor, una o dos frases: sldb pinnea __doc_anchors__ al crear (create_document, desde sldb 477d1bc0) y al guardar; solo ese docstring.
Precisiones del coordinador (bundle 1), ademas de las del preflight 1: (1) Agregar import re en tests/test_review_command.py entra en alcance. (2) El ejecutor no commitea: el commit y el closeout los hace el coordinador con deskops closeout commit. (3) El ejecutor comprueba que el sldb que importa el venv incluye 477d1bc0 (git -C de la raiz del paquete sldb importado: merge-base --is-ancestor 477d1bc0 HEAD) y lo anota; si no lo incluye, para y lo informa, sin reinstalar nada.

## Notas del coordinador

- Pedido del integrador wA:p1: son las 3 fallas de la suite sobre origin/main (ee9bc3cd) por sldb 477d1bc0. Solo tests.
- En el checkout hay cambios sin commitear de otra tarea (atoms citations: deskops/services/atoms.py, deskops/cli/*, tests/test_atom_citations.py, goldens de ayuda) y de .sldb: no los toques.
- Lista cada archivo tocado y, si alguno está fuera de files, explica por qué.
