# Veredicto del tester deskops-t-91635780a910

Tarea: task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista
Entrega: ejecutor deskops-e-df9455e89049 (cambios sin commitear). Evidencia: validation.log.

## 1. Diff contra contrato y precisiones (preflight-1/bundle-1)
- `task.receipts` dentro de `task`, mismo nivel que `gates`: sí (view.py, dict de `task`).
- Claves exactas id, kind, verdict, anchor_state, created_at: sí; el test las fija con `set(item) == {...}`.
- Pertenencia por subject sin pin: `subject.split("@",1)[0] == doc:<modelo>:<id>`; modelo sacado del export_id de la fila. Recibos de nodo (subject vacío) quedan fuera por construcción.
- Orden (created_at, id): sí (`sorted`), probado.
- anchor_state: `subject__anchor_state` del índice compuesto (`load_edge_index`), lo mismo que lee `^subject` en la regla de activación (sldb predicate_reach). Comprobado en vivo: coincide con el witness de la regla.
- Error de índice a `errors` con lista `[]`: sí (try/except → `_error`, `return []`). No tiene test propio (menor).
- json y yaml con la misma estructura: sí, probado en el test.
- Texto: una línea `receipt <id> <kind> <verdict> <anchor_state> <created_at>` por recibo: sí, probado.
- Board sin receipts: solo se añade en la vista task; render_text de board no cambia.
- docs/deskops-ui.md: ejemplo, viñeta del campo, fila de fuentes y fila del mapeo actualizadas.

## 2. Cambios fuera de `files`
- registry.py: una línea (`OUTPUT_FORMAT_ARG` → `OUTPUT_FORMAT_YAML_ARG`, constante existente). Necesaria: view task no aceptaba yaml y la precisión (5) lo exige. Mínima.
- tests/fixtures/golden/help/deskops_view_task.txt: consecuencia directa del cambio anterior. Mínimo.
- tests/fixtures/golden/output/view_task.json: solo `"receipts": []`; permitido por la precisión (6) y declarado por el ejecutor.
- Observación para el cierre: `files` del TaskDoc no lista estos tres archivos; habrá que reconciliarlo al cerrar.

## 3. Pruebas (sin lock, una a la vez)
- tests/test_view.py: 17 passed, rc=0
- tests/test_view_goldens.py: 1 passed, rc=0
- tests/test_command_registry.py: 3 passed, rc=0
- tests/test_output_goldens.py -k help_goldens: 1 passed, rc=0

## 4. Reproducción
Copia del repo en /dev/shm con view.py de HEAD: el test nuevo falla con `KeyError: 'receipts'` (1 failed). Con la entrega pasa. Copia borrada.

## 5. Caso real (solo lectura)
No queda en el desk ninguna tarea cerrada con recibos (al cerrar salen de desk/tasks/; la tarea cerrada en 07b512ae da "does not resolve"). Usé dos tareas abiertas:
- La propia tarea: preflight-1 y bundle-1, accepted, `intact`, en orden; pin e178b433 sin cambios en la tarea.
- task-graph-missing-separa-…: 4 recibos (preflight/bundle 1 rejected, 2 accepted), todos `changed`, en orden por created_at. Es coherente: la tarea se editó después (ce5bda0a, 06:22Z, posterior a los recibos de 06:14–06:20Z), y `show task` muestra el gate bloqueado con el witness `{"anchor_state":"changed"}`.
- Ningún error de recibos en `errors`.

## Hallazgos menores (no bloquean)
- La rama de error del índice (errors + []) no tiene test.
- `except Exception` amplio y fallback del modelo a "TaskDoc" si el export_id no trae ":".
- No corrí la suite completa ni `stores build --check` (fuera del encargo).

VEREDICTO: APROBADO
