## REFORMULACION

Propósito: ampliar el closeout para que reconozca evidencia real de trabajo hecho en otros lenguajes o repos. Resultado: `reference_points_to_test` acepta una lista cerrada de sufijos (`*_test.go`, `*.test.sh`, `*.bats`) y `runs/.../validation.log` como prueba; `reference_points_to_commit` (y `resolved-by`) acepta `repo:<nombre>@<sha>` de un repo registrado, existente y ancestro de su HEAD. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops` (archivos `closeout_gates.py`, `closure.py`, `docs/workflow-policy-reference.md`, tests). Límites: no cierra las tres tareas de scion, no cambia qué evidencia exige cada tipo; sufijos cerrados; log con `$ ` inicial y `rc=0` final.

## AMBIGUEDADES

1. "una referencia repo:<nombre>@<sha>" — el código existente parte en el primer `:` y espera `<repo-id>:<sha>`; `repo:` con `@` obligaría a inventar si es literal o ilustrativo y cómo convive con `RepositoryReferences.split`.
2. "cuenta como evidencia de tests para artefactos sin framework de tests" frente a "se acepta para cualquier tarea, no hay que detectar 'sin framework'" — obligaría a decidir si la condición "sin framework" se ignora del todo.
3. "el archivo debe estar en files o references" — el recolector actual solo marca tests desde `references`, usando `files` solo para ampliar ubicación; obligaría a inventar si basta estar en `files`.
4. "Lo mismo vale para closeout resolved-by" — no dice si `--test` acepta también los sufijos nuevos ni si `--ref` acepta `repo:...@...`.
5. La validación incluye `tests/test_closeout_test_paths.py`, ausente de `files`; obligaría a inventar si existe o debe crearse.
6. "la nota a scion ... con el hash del commit" — no aclara de qué commit (el de cierre de esta tarea).

## DRY-RUN

Lecturas: `closeout_gates.py:140-260`, rama resolved-by de `closure.py`, `docs/workflow-policy-reference.md`, los tres archivos de test. Cambios previstos: tabla de sufijos, chequeo de log bajo `runs/`, resolución de repo registrado con `merge-base --is-ancestor`, docs y tests nuevos. Dependencias: entradas de registro con raíz local, repos git accesibles, comando `deskops message send`. Validaciones futuras: los cuatro comandos pytest del TaskDoc, más worktree limpio de `origin/main` para fallas. No se ejecuta nada.

## FUTURO

El coordinador de scion cierra sus tres tareas tras el cambio; un humano o coordinador decide si fallas de la suite son preexistentes; el envío final del mensaje con el hash queda para el ejecutor.
