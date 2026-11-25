## REFORMULACION

Encargo: en el repo `deskops`, declarar el tag namespace `host` para que cada TaskDoc indique la máquina donde corre (`host:local` / `host:robocop2`). Resultado esperado: `deskops/atom_tags.py` (semilla `TagNamespace`, ~159-204) incluye `host` con `hierarchical=False`, `folder_axis=False`, y textos meaning/use_when/do_not_use_when indicados; `TaskDoc` entra en `tag_models` y se declaran también `workspace`, `artifact`, `source`; una línea en `docs/workflow-policy-reference.md` sección `### Tasks`; test ampliado en `tests/test_atom_tags.py`; `.sldb/store.yaml` actualizado tras `deskops desk update --apply`. Límites: no taggear tareas existentes; no restringir valores (sldb no tiene enumeraciones); si `stores check` sigue alertando con los tres namespaces extra, detenerse, enviar mensaje a sldb y cerrar solo con documentación.

## AMBIGUEDADES

1. "la semilla de desk que la usa" — no identifica archivo; obligaría a inventar cuál semilla además de `atom_tags.py`.
2. "si con workspace, artifact y source declarados sldb stores check sigue dando alertas de tag en tareas existentes" — no aclara si se declaran incondicionalmente o solo al detectar alertas; obligaría a inventar el orden de decisión.
3. "un test nuevo o ampliado en tests/" frente a "El test va en tests/test_atom_tags.py (ampliado)" — contradicción menor; obligaría a elegir.
4. "La tarea de prueba es una creada en el desk sandbox del test" — no define cómo se construye ese sandbox; obligaría a inventar el fixture.
5. "una tarea con host:robocop2 no produce alertas de tag en sldb stores check" — no fija el comando exacto ni el root del check en el criterio; obligaría a inferirlo de Validation.

## DRY-RUN

Lecturas: `deskops/atom_tags.py`, `sldb docs/architecture/tags.md`, `.sldb/store.yaml`, `tests/test_atom_tags.py`, `docs/workflow-policy-reference.md`. Cambios: añadir `host` (y `workspace`/`artifact`/`source`) a la semilla y a `DEFAULT_ATOM_TAG_NAMESPACES`; incluir `TaskDoc` en `tag_models`; ampliar test; una línea de doc; regenerar store con `desk update --apply`. Dependencias: modelo `TagNamespace` de sldb tal cual; `tag_models` global. Validaciones futuras: pytest de `test_atom_tags.py` y `test_domain_tree.py`, `sldb stores check`, suite completa con comparación en worktree limpio.

## FUTURO

Coordinadores taggean tareas existentes; sldb decide namespaces por modelo si falla el criterio de detención; humano/JP valida textos y commit de `.sldb/store.yaml`.
