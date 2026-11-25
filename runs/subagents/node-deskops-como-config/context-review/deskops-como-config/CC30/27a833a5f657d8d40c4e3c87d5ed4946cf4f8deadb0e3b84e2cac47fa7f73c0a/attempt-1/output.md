## REFORMULACION
Encargo de planificación (nodo `delivery`, no agregado): limpieza previa en deskops para que `operations.py` sea fachada sin lógica y desaparezcan los specs YAML duplicados. Resultado: helpers privados que los servicios piden a operations viven en `deskops/doc_access.py` o en el servicio dueño; los servicios dejan de construir `DeskopsOperations`; la fachada solo delega; los privados que importa graph_ui se conservan como alias comentados hasta CC34; `_normalize_task_payload`/`compile_task_spec` y el loader de `task_lifecycle.yaml` quedan únicos; se borran `spec/artifacts/`, `spec/fields/`, `SpecRegistry` y `_ARTIFACT_DEFAULTS`, y `id_pattern`/`status_default`/`tags` pasan a atributo de clase del modelo. Repo dueño: deskops. Límites: sin cambio de comportamiento, goldens de ayuda y salida idénticos, alcance acotado a `output_scope`, invariante de `alcance.md` (borrar el código viejo en el mismo paso).

## AMBIGUEDADES
1. "pasan a un módulo deskops/doc_access.py (…) o al servicio dueño": deja dos destinos posibles por helper sin criterio ni comprobación en la aceptación; obliga a inventar la regla de asignación.
2. "specs/mermaid.py si solo los usan tests": borrado condicional sin fijar qué cuenta como "solo tests"; obliga a inventar el criterio y el alcance del grep.
3. "_add_closeout_facts y los demás que el grep delate": conjunto abierto sin patrón de grep fijado; obliga a inventar qué pruebas deciden la lista.

## DRY-RUN
Lecturas: `operations.py`, `services/` (tasks, atoms, closure), `specs/loader.py`, `spec/mermaid`, `spec/artifacts|fields`, `cli/model_introspection.py`, `models/`, `workflow/next_actions.py`, tests de specs, extension points y desk_view. Cambios previstos: crear `doc_access.py`, mover helpers, quitar constructores `DeskopsOperations`, alias comentados CC34, unificar normalize/compile y el loader de lifecycle, borrar specs y `_ARTIFACT_DEFAULTS`, añadir atributo de artefacto en modelos, adaptar tests, CHANGELOG. Dependencias: `G_P0` y `G_GATES_FROZEN`, ambos `satisfied`; `depends_on: []`. Validaciones futuras: greps del acceptance vacíos, goldens sin `--update-golden`, tests de archivos tocados y `test_desk_view.py`, conteo de líneas antes/después.

## FUTURO
CC34 retira los alias; CC31, CC32, CC35, CC38 y CC51 dependen de este nodo; el supervisor corre la suite completa sobre el resultado integrado; `deskops doctor` y los 6 desks los valida el cierre.
