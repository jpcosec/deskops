FALLA

# Resultado del tester

Tarea: task-closeout-commit-stagea-solo-lo-que-escribio-el-cierre-sin-git-add-a-sobre-sldb-y-sin-nothing-staged
Run: run-deskops-t-a1f712d51bc9
Commit evaluado: `2fe1b60ec478e430e93ca45b95abdd4c5f6be3bb` — "closeout commit: stage only what the close wrote under .sldb; no mute Nothing staged".
Trailer verificado: `Task-Id: task-closeout-commit-stagea-solo-lo-que-escribio-el-cierre-sin-git-add-a-sobre-sldb-y-sin-nothing-staged`.
Archivos del commit: `deskops/services/closure.py` y `tests/test_closeout.py`.

## Veredicto

Los tests nuevos del ejecutor pasan y los dos síntomas concretos de las notas del inbox quedan
cubiertos, pero la implementación **no cumple el Goal** en su parte absoluta: todavía arrastra al
commit archivos de `.sldb` que ya estaban sin trackear (o modificados) antes del cierre y que el
cierre no escribió. La causa es `_sldb_belongs_to_close`, que exceptúa del criterio "solo lo que
escribió el cierre" a todo `.sldb/core/models/*`, a `.sldb/store.yaml`,
`.sldb/core/store_index.yaml` y a cualquier documento cuyo nombre o cuerpo contenga el task id o
el stem de un path. Además, sin `--paths` el `git commit` se ejecuta sin pathspec, así que también
se lleva cualquier cambio que ya estuviera staged antes del cierre.

## Tests ejecutados (de a uno, `TMPDIR=/tmp`)

El `.venv` versionado apunta a `/home/robocop/...` y a un Python 3.12 ausente en este host. Usé un
venv temporal en `/tmp/tester-venv` con Python 3.13.18, `pytest 9.2.0` y los paquetes locales
`deskops` y `structuredlanguagedb` en modo editable.

```text
TMPDIR=/tmp /tmp/tester-venv/bin/python -m pytest -q tests/test_closeout.py
  -> 79 passed (94.66 s)
TMPDIR=/tmp /tmp/tester-venv/bin/python -m pytest -q tests/test_closeout_atomless.py tests/test_closeout_resolved_by.py
  -> 40 passed (67.31 s)
TMPDIR=/tmp /tmp/tester-venv/bin/python -m pytest -q tests/test_closeout_gates.py tests/test_closeout_evidence_receipts.py \
  tests/test_closeout_declared_evidence.py tests/test_closeout_resolved_by_xrepo.py tests/test_closeout_test_paths.py \
  tests/test_closeout_rules.py tests/test_closeout_skill_links.py
  -> 102 passed (404.54 s)
```

No existe `tests/test_closure.py` para el módulo tocado. No corrí la suite completa (la corre
integrate en el host). No hubo fallas en los archivos ejecutados.

## Lo que sí funciona

- `tests/test_closeout.py` incluye los casos pedidos (untracked ajeno en
  `.sldb/core/documents`, tracked modificado antes del cierre y cierre sin `--paths`) y pasan.
- Repetí esos escenarios en un desk sandbox con store, y además sin `--paths`: un
  `.sldb/core/documents/foreign.yaml` sin trackear antes del cierre sigue sin trackear y no entra
  al commit; el TaskDoc/`TaskExternalDoc` y `desk/tasks/Board.md` sí entran; el error de "Nothing
  staged" lista el `git status --porcelain` y sugiere `--paths`.
- `resolved-by`, `retire` y `supersede` pasan por el mismo `_close`, y sus suites pasan.

## Evidencia del incumplimiento del Goal

En un `lifecycle_desk` real (store-backed), después de crear y commitear la tarea y correr
`closeout verify`, preparé antes del cierre:

1. `.sldb/core/models/ForeignModelDoc.yaml`, **sin trackear**, creado antes del cierre.
2. `.sldb/core/documents/foreign-other.yaml`, **sin trackear**, cuyo cuerpo menciona el task id.
3. `.sldb/core/models/UnusedDoc.yaml` y `.sldb/core/documents/unused-other.yaml`, ambos trackeados
   y modificados a mano antes del cierre, sin que el cierre los use.
4. `unrelated.txt` ya staged antes del cierre, para el caso sin `--paths`.

Resultado observado en `git show --name-only HEAD`:

```text
.sldb/core/models/ForeignModelDoc.yaml          <- untracked ajeno antes del cierre, SÍ entra
.sldb/core/documents/foreign-other.yaml         <- untracked ajeno antes del cierre, SÍ entra
.sldb/core/models/UnusedDoc.yaml                <- modificado antes, no tocado por el cierre, SÍ entra
.sldb/core/documents/unused-other.yaml          <- modificado antes, no tocado por el cierre, SÍ entra
unrelated.txt                                   <- staged ajeno, SÍ entra sin --paths
```

Tras el commit, los archivos `UnusedDoc.yaml` y `unused-other.yaml` quedan limpios (fueron
commiteados), justo lo que el Implementation Path prohíbe: "una ruta trackeada ya modificada antes
del cierre y que el cierre no vuelve a tocar no se stagea". Igual de claro para el punto 3 del
Implementation Path: "Sin `--paths`: stagear el TaskDoc, el Board y las rutas del paso 2", no todo
el índice.

## Acción sugerida para el ejecutor

- Quitar las excepciones de `_sldb_belongs_to_close`: una ruta presente en la foto A que no cambió
  de código en B no debe stagearse, aunque sea modelo, store_index o documento que mencione el task
  id. Si hace falta detectar escrituras reales del cierre, comparar contenido/hash en la foto, no
  el nombre.
- Sin `--paths`, commitear con pathspec explícito de `commit_paths` (o limpiar el índice ajeno
  antes del commit) para que un cambio ya staged no viaje en el commit de cierre. Agregar tests
  para estos dos casos, además de los ya presentes.

## Datos del run

- Task id: task-closeout-commit-stagea-solo-lo-que-escribio-el-cierre-sin-git-add-a-sobre-sldb-y-sin-nothing-staged
- Role: tester
- Commit evaluado: 2fe1b60ec478e430e93ca45b95abdd4c5f6be3bb
- Los probes se ejecutaron en directorios temporales de pytest y se eliminaron; no se modificó el repo.
