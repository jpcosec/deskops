REFORMULACION

Propósito: sustituir los selectores propios de deskops por `sldb.api.select_documents` (GD23), conservando la regla exacto > prefijo único y los mensajes de error armados con los candidatos que devuelve sldb. Resultado: `desk_paths`, `operations`, `issues` y `drawer` dejan de resolver documentos por su cuenta; los alias privados que graph_ui importa se conservan hasta CC34. Repo dueño: deskops. Límites: es la parte (2) de CC35; no toca la transacción (CC35a) ni tags/reemplazo (CC35d); no escribe en sldb ni suple reglas con Python; mantiene el formato del desk y la gramática del CLI.

AMBIGUEDADES

1. «salvo los alias para graph_ui marcados CC34» y «Los alias privados que graph_ui importa se conservan hasta CC34». No nombra los alias ni qué significa «marcados CC34»; alcance.md dice que graph_ui importa `_read_doc`, `_resolve_glob`, `_registered_repositories`, `_repository_root`, pero el grep no vigila esos nombres. Obligaría a inventar la lista de alias y la convención de marcado.

2. «grep -rn "resolve_selector\|_tracked_task_paths" deskops/ vacío» frente al scope, que también manda migrar `resolve_glob`, `resolve_artifact_selector[_multi]`, `_registered_repositories`, `_resolve_ritual_selector`, `issues.find_issue/list_issues` y `drawer.resolve_drawer_source/_resolve_unique`. La aceptación no comprueba esos nombres; obligaría a inventar si deben borrarse y cómo se verifica.

3. `output_scope` incluye «deskops/doc_access.py» pero el scope no le asigna cambio alguno (solo menciona `desk_paths`, `operations`, `services`, `issues` y `drawer`). Obligaría a inventar qué se modifica allí.

DRY-RUN

Hipotético, sin ejecutar. Lecturas: `desk_paths.py`, `doc_access.py`, `operations.py`, `services/issues.py`, `drawer.py`, tests y goldens de ayuda/salida. Cambios previstos: reemplazar cada selector por `sldb.api.select_documents`, conservar los alias exigidos por graph_ui marcados CC34, borrar el código viejo en el mismo paso, actualizar tests y `CHANGELOG.md`. Dependencias: CC35a integrado; `G_GD23` satisfecho con el pin de sldb ≥0.1.13. Validaciones futuras: grep de aceptación, comparación de goldens, tests de archivos tocados, `deskops doctor` en los 6 desks, líneas antes/después; capturar goldens antes del cambio si faltan (regla 4).

FUTURO

CC35d consumirá selectores ya migrados; CC34 retirará los alias de graph_ui; el supervisor correrá la suite completa sobre lo integrado y el coordinador promoverá el nodo cuando corresponda.
