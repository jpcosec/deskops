## REFORMULACION

**Propósito:** ampliar las compuertas de evidencia de closeout del repo `deskops` (`/mnt/ssd/proyectos/SLDB_1/deskops`) para aceptar tests de otros lenguajes, logs de validación bajo `runs/` y evidencia de commits en otro repo registrado; extender también `closeout resolved-by`. **Resultado:** `reference_points_to_test` acepta además `*_test.go`, `*.test.sh` y `*.bats`; un archivo bajo `runs/` con primera línea que empieza por `$ ` y última `rc=0` cuenta como evidencia de tests; `RepositoryReferences` resuelve `<repo-id>:<sha>` también contra el registro del ecosistema (`find_registered_desk` en `deskops/identity.py`); `resolved-by` acepta esos sufijos en `--test` y `<repo-id>:<sha>` en `--ref`. **Límites:** solo `closeout_gates.py`, `closure.py` (rama resolved-by), `docs/workflow-policy-reference.md` y tests en `tests/test_closeout_gates.py`/`tests/test_closeout_resolved_by.py`; no se cierran las tres tareas de scion ni se cambia qué evidencia exige cada tipo.

## AMBIGUEDADES

1. `"files sigue sirviendo solo para ampliar ubicaciones, como hoy"` frente a `"el archivo debe estar en files o references de la tarea"`: no queda claro si `files` cuenta como evidencia por sí mismo o solo amplía ubicaciones. Obliga a inventar el criterio.
2. `"que existan en el repo y esten citados en references"`: no dice si para los sufijos nuevos siguen aplicando la exigencia de directorio `tests/` y las exclusiones (ocultos, `site-packages`, `node_modules`); `cmd/build_context_test.go` está en `cmd/`. Obliga a inventar.
3. `"cuya ultima linea no vacia es 'rc=0'"` (Goal) frente a `"cuya ultima linea es 'rc=0'"` (Scope): no aclara si vale la última línea no vacía o la última literal, ni si sustituye o se suma al gate `tests`. Obliga a inventar.
4. `"debe buscar tambien en el registro del ecosistema, con la misma resolucion que usa deskops message send --to (find_registered_desk en deskops/identity.py)"`: no define qué es ese registro ni si devuelve repos o desks, ni contra qué `HEAD` se comprueba el ancestro. Obliga a inventar.
5. `"closeout resolved-by acepta en --test los sufijos de (1)"`: no aclara si `resolved-by` acepta también el log `runs/` de (2) como `--test`. Obliga a decidir.

## DRY-RUN

Lecturas hipotéticas: `closeout_gates.py:140-300` y `deskops/identity.py::find_registered_desk` (no incluidos en el bundle), `closure.py`, y los tres tests nombrados. Cambios previstos: tabla cerrada de sufijos en `reference_points_to_test`; nueva comprobación de log `runs/`; `RepositoryReferences` consultando también el registro del ecosistema; parseo en la rama `resolved-by`; doc de evidencia; casos de test del paso 5. Dependencias: `identity.py`, `closure.py` y `tests/test_closeout_test_paths.py` no vienen en el input; la nota final usa `deskops message send --to scion`. Validaciones futuras: los tres pytest y la suite `-n 4`, con baseline en worktree limpio de `origin/main` para fallas nuevas.

## FUTURO

Otro nodo implementa y entrega el hash; el Tester valida; el coordinador envía la nota a scion con `deskops message send`; el coordinador de scion cierra sus tres tareas; el humano decide.
