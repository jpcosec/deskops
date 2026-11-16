## REFORMULACION

Encargo ejecutable: migrar las claves legacy de frontmatter `checklists` y `routine` en los TaskDocs de `desk/tasks`, para que `closeout supersede` y `edit` puedan reescribirlos. Resultado esperado: `desk update` en dry-run reporta cada archivo y clave afectados y devuelve rc 1 si hay pendientes; `desk update --apply` elimina solo esas líneas del frontmatter, conserva el resto del documento y del YAML sin re-serializar, imprime `<ruta relativa>: removed <clave> = <valor anterior JSON compacto>` y devuelve rc 0. La lista de claves es cerrada; otras claves no declaradas siguen provocando el rechazo actual de `write_doc`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: tocar `deskops/workspace.py`, `deskops/cli/commands/desk.py` y `tests/test_legacy_task_states.py`; no cambiar `write_doc`, no añadir flags a `supersede`, no declarar esas claves en `TaskDoc`, no cerrar las tareas de marcado ni abordar `message send --root`.

## AMBIGUEDADES

1. «lista cada TaskDoc ... con el archivo y la clave» no fija el formato exacto del dry-run ni si será una línea por archivo o por clave. Obligaría a inventar el formato de reporte.
2. «una linea por clave quitada» no define el orden cuando coexisten `checklists` y `routine`. Obligaría a inventar el criterio de orden.
3. «valor anterior en JSON compacto de una linea» no indica cómo serializar valores YAML no representables directamente en JSON. Obligaría a inventar la conversión.
4. «da rc 1 como cualquier migracion pendiente» no especifica el comportamiento ante un TaskDoc ilegible o con frontmatter malformado. Obligaría a inventar el manejo de errores.

## DRY-RUN

Lecturas previstas: `legacy_task_states` y `migrate_legacy_task_states` en `workspace.py`; `write_doc` y `undeclared_frontmatter_keys` en `doc_access.py`; bloque de `desk update` en `desk.py`; modelo `TaskDoc`; tests existentes. Cambios previstos: detección de claves en `desk/tasks` bajo `--root`; reporte en dry-run y rc 1; edición textual en `--apply` con salida por clave; tests en sandbox `tmp_path`, incluido caso mixto y verificación con `closeout supersede`. Dependencias: parser de frontmatter, patrón de migraciones existente y CLI. Validaciones futuras: los pytest listados, suite completa y comprobación de que las claves desaparecen sin alterar el resto.

## FUTURO

Un humano prioriza y acepta el resultado; el coordinador de marcado ejecutará el CLI para cerrar los tres TaskDocs; otro nodo reportará fallas de la suite en `origin/main`; la entrega incluirá tests y commit según los átomos.
