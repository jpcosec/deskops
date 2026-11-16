REFORMULACION
Propósito: retirar el camino de compatibilidad de task_type ya migrado (DK3) en el repo deskops (/mnt/ssd/proyectos/SLDB_1/deskops). Resultado: en deskops/workspace.py borrar LEGACY_TASK_TYPE_KEYS, _task_type_migration_plan, pending_task_type_migration, _task_type_migration_line y migrate_task_types; en deskops/cli/commands/desk.py quitar import, uso y llamada; borrar los tests que ejercitan esas funciones; en docs/workflow-policy-reference.md línea 75 quitar «and migrates legacy task_type strings (...)» dejando «registers them». Se conservan LEGACY_TASK_TYPE_MAP, canonical_task_type_name y la aceptación de cualquier task_type por TaskDoc genérico. Límites: no otros legacy ni cambios en add task/closeout; no añadir comportamiento; dependencia externa closed; grep vacío y suite sin fallas nuevas.

AMBIGUEDADES
1. «Se borra el camino de migracion ... LEGACY_TASK_TYPE_KEYS, _task_type_migration_plan, pending_task_type_migration, _task_type_migration_line y migrate_task_types» no nombra helpers que quedarían muertos (_frontmatter_task_type, _rewrite_task_type, _task_lifecycle_errors, _inconsistent_task_line): inventar si se borran.
2. «... (el validador la reporta)» frente a «TaskDoc generico sigue aceptando cualquier task_type como hoy»: inventar qué validador y si el genérico acepta.
3. «tests/test_task_lifecycle_validator.py (casos legacy)» y «como valor a migrar» frente a test_desk_update_reports_an_inconsistent_task..., que usa task_type: code sin probar migración: inventar si se borra o reescribe.
4. «y sus tests» frente a files, que omite tests/test_cli.py pero validation lo ejecuta: inventar si sus aserciones sobre «Pending task type migration» entran.
5. «el import y el uso ... y la llamada a la migracion» no menciona la línea de reporte «Pending task type migration»: inventar si se elimina.

DRY-RUN
Lecturas: archivos citados (workspace.py, desk.py, tests, docs) y estado de la dependencia con `deskops show task ... --root .`; sin ejecutar. Cambios previstos: borrar las cinco funciones y referencias en desk.py —incluido el bloque de reporte si se decide—; borrar tests y helpers muertos; recortar la frase de docs. Dependencias: tarea externa closed, fixtures lifecycle_desk, sldb, .venv y worktree de origin/main. Validaciones futuras: grep vacío; pytest de test_task_types.py, test_task_lifecycle_validator.py y test_cli.py; suite completa -n 4; cada falla se compara en worktree limpio y se lista en el informe.

FUTURO
Otro nodo/ejecutor implementará y correrá validaciones; un Tester independiente validará; el coordinador resolverá las ambigüedades y decidirá alcance de tests/helpers; closeout commit cerrará con evidencia. La dependencia externa la cierra otro nodo.
