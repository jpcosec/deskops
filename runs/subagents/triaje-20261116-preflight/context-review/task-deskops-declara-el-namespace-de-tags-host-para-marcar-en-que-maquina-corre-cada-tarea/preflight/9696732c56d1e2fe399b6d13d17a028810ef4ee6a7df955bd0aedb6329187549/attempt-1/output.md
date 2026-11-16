## REFORMULACION

**Propósito:** que cada TaskDoc declare en qué máquina corre y se valida, usando `TaskDoc.tags`, porque ningún store del ecosistema declara hoy un namespace de máquina.

**Resultado:** la semilla de tags de deskops (`deskops/atom_tags.py`: `DEFAULT_ATOM_TAG_NAMESPACES` y la sincronización de `tag_namespaces`/`tag_models`, ~líneas 159-204) incluye un namespace `host` no jerárquico, aplicable a TaskDoc, con `meaning` "máquina donde se ejecuta y valida la tarea", valores documentados `host:local` y `host:robocop2`, `use_when` y `do_not_use_when`; una línea en `docs/workflow-policy-reference.md`; un test nuevo o ampliado; y `.sldb/store.yaml` del desk deskops actualizado tras `desk update --apply`, de modo que una tarea con `host:robocop2` no genere alertas en `sldb stores check`.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops` (con `sldb/src` como referencia de solo lectura). Es una tarea `task.code` ejecutable, no un agregado.

**Límites:** no taggear tareas existentes; no imponer enumeración si sldb no la soporta (solo documentar); no tocar superficies fuera de atom_tags, doc, test y store.

## AMBIGUEDADES

1. "no jerárquico" — no define la forma del namespace en `tag_namespaces`/`tag_models`; obligaría a inventar el esquema.
2. "tag_models que incluya TaskDoc" — no fija formato ni cómo excluir atoms/pills; inventar representación.
3. "use_when y do_not_use_when (no se usa en atoms ni pills)" — no da textos; inventar redacción.
4. "restringir valores si sldb no soporta enumeraciones (se documentan)" — no aclara si se intenta enum o solo doc; decisión inventada.
5. "`deskops edit task <id> tags '[...]'`" — `<id>` no identificado; inventar qué tarea usar.
6. "buscar el test actual de tag namespaces" y "un test nuevo o ampliado" — sin archivo ni criterio ampliar/crear; elección inventada.
7. "docs/workflow-policy-reference.md" — ruta no anclada (¿deskops/docs o raíz SLDB?); inventar ubicación.
8. "sin fallas nuevas respecto de main" — baseline/rama no definidos; inventar criterio.

## DRY-RUN

**Lecturas:** `deskops/atom_tags.py`, `sldb docs/architecture/tags.md`, `docs/workflow-policy-reference.md`, `.sldb/store.yaml`, grep de `tag_namespaces` en `tests/`. **Cambios:** añadir `host` a la semilla y sincronización; una línea de doc; test; regenerar store. **Dependencias:** soporte de `sldb stores check` para tags, `desk update --apply` en sandbox. **Validaciones futuras:** los cuatro comandos de `Validation`. Nada se ejecuta aquí.

## FUTURO

Otros nodos/coordinadores taggean las tareas existentes; un humano confirma si `host:local` es literal o nombre de máquina y aprueba textos; sldb podría añadir soporte de enumeraciones; el ejecutor futuro commitea `.sldb/store.yaml`.
