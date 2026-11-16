REFORMULACION
Propósito: migrar las claves legacy `checklists` y `routine` del frontmatter de los TaskDocs de `desk/tasks`, porque `write_doc` (`deskops/doc_access.py`, `undeclared_frontmatter_keys`) rechaza reescribirlos y eso bloquea `closeout supersede` de tres tareas de marcado. Resultado: `desk update` (dry-run) lista archivo y clave de cada TaskDoc afectado con rc 1; `--apply` elimina solo esas dos claves, conserva el resto del documento e imprime clave y valor anterior; tras `--apply`, `supersede` deja de fallar por esas claves. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: tocar `deskops/workspace.py`, `deskops/cli/commands/desk.py` y `tests/test_legacy_task_states.py`; no cambiar `write_doc`, no añadir flags a `supersede`, no declarar las claves en TaskDoc, no cerrar tareas de marcado, no el bug de `message send --root`. Nodo ejecutable (task.code), no agregado.

AMBIGUEDADES
1. "imprime por cada archivo la clave quitada y su valor anterior en una linea": formato no definido (separador, quoting, valores multilínea de `checklists`); obligaría a inventar sintaxis de salida.
2. "da rc 1 como cualquier migracion pendiente": no aclara si `--apply` devuelve 0 o 1; obligaría a decidir el contrato de exit codes.
3. "una tarea con otra clave no declarada no se toca y supersede sigue rechazandola": no cubre el caso mixto (checklists/routine + otra clave no declarada); obligaría a decidir si `--apply` reescribe parcialmente o aborta.
4. "sin tocar el resto del documento" frente a "reescribir el frontmatter": no fija orden de claves ni estilo YAML; obligaría a inventar política de serialización.
5. "desk/tasks" sin indicar resolución de raíz (cwd, `--root`, sandbox); obligaría a asumir dónde busca.
6. En Validation, la última entrada aparece como dict con la clave truncada por ":"; no es un comando claro.

DRY-RUN
Lecturas: `legacy_task_states`/`migrate_legacy_task_states` en `workspace.py`; `write_doc`/`undeclared_frontmatter_keys` en `doc_access.py`; bloque `desk update` en `cli/commands/desk.py`; tests existentes. Cambios previstos: función de detección/migración de las dos claves, reporte y condición de "up to date" en el CLI, tests sandbox con los tres casos del paso 5. Dependencias: modelo TaskDoc y `write_doc` intactos; estados legacy ya migrados. Validaciones futuras: los tres pytest indicados y suite completa con comparación contra `origin/main` en worktree limpio para fallas nuevas. Nada se ejecuta aquí.

FUTURO
El coordinador de marcado cierra las tres tareas con el CLI nuevo tras el merge; el bug de `message send --root` corresponde a otro nodo; la prioridad 1 la fija el supervisor.
