## REFORMULACION

**Propósito:** que el store de deskops declare el namespace de tags `host` para que cada `TaskDoc` indique en qué máquina corre (`host:local` / `host:robocop2`), y que sldb no emita alertas de tag por tareas existentes.

**Resultado:** `deskops/atom_tags.py` agrega `host` a `DEFAULT_ATOM_TAG_NAMESPACES` con los textos dados y, con `TaskDoc` en `tag_models`, declara también `workspace`, `artifact` y `source`; una línea nueva en `docs/workflow-policy-reference.md` bajo `### Tasks`; test ampliado en `tests/test_atom_tags.py`; `.sldb/store.yaml` regenerado con `desk update --apply`; commit.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops` (deskops).

**Límites:** no taggear tareas existentes; no restringir valores; si tras declarar `workspace/artifact/source` siguen alertas, detenerse, enviar mensaje a sldb y cerrar solo con documentación. Es un `task.code` ejecutable (hoja), no un agregado.

## AMBIGUEDADES

1. `"se declaran tambien workspace, artifact y source (hierarchical=False)"` — no da `meaning`, `use_when`, `do_not_use_when` ni `examples` para esos tres; obliga a inventar textos de registro.
2. `"host con hierarchical: false y folder_axis: false"` choca con el comentario del código `"folder_axis is not declared"`; obliga a decidir si se declara `folder_axis` y se cambia la construcción de `TagNamespace`.
3. `"meaning, use_when y do_not_use_when de host van en el registro"` — omite `examples`, campo presente en todas las entradas; obliga a inventar ejemplos o dejarlo ausente.
4. `"la semilla de desk que la usa"` — no nombra archivo; obliga a decidir si es `desk/atoms/tag-namespaces.yaml` o solo `DEFAULT_ATOM_TAG_NAMESPACES`.
5. `"si TaskDoc entra en tag_models se declaran tambien..."` (condicional) frente a `"TaskDoc entra en tag_models"` (afirmativo); obliga a decidir si añadir `TaskDoc` es obligatorio o condicional.

## DRY-RUN

**Lecturas:** `deskops/atom_tags.py`, `sldb docs/architecture/tags.md`, modelo `sldb.api.stores.tag_namespace.TagNamespace`, `tests/test_atom_tags.py`, `tests/test_domain_tree.py`, `.sldb/store.yaml`, `desk/atoms/tag-namespaces.yaml`.

**Cambios previstos:** entradas nuevas en `DEFAULT_ATOM_TAG_NAMESPACES`; `TAG_MODELS` con `TaskDoc`; ajuste de `wanted_tag_declaration`; regeneración de la semilla; línea en la doc; test de sandbox con `host:robocop2`; `store.yaml` por `desk update --apply`.

**Dependencias:** API sldb de tag namespaces, `pytest`, desk sandbox.

**Validaciones futuras:** los cuatro comandos de la sección Validation, incluida la suite completa con baseline en worktree.

## FUTURO

El coordinador taggea las tareas existentes; sldb decide si necesita namespaces por modelo si se cumple el criterio de detención; un humano aprueba producto; Executor y Tester independientes validan; no es agregado, no hay hijos.
