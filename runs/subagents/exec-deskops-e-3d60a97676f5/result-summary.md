# Resultado del ejecutor deskops-e-3d60a97676f5

Tarea: `task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo`

## Cambios (todos dentro de `files` del TaskDoc)

- `deskops/models/review.py`: `SUBJECT_REF_PATTERN` pasa de `[A-Za-z0-9_-]+` a `[A-Za-z0-9_.-]+` en el id de nodo. Un espacio o un segundo `#` siguen rechazados (el prefijo es `[^\s#]+` y la clase del id no los admite).
- `tests/test_review_doc.py`: `test_review_plan_node_subject_ref_accepts_a_dotted_node_id` (`dag.yaml#node:WS13.1` valida) y `test_review_plan_node_subject_ref_rejects_a_space_or_a_second_hash` parametrizado con `WS 13` y `WS13#x` (ValidationError sobre `subject_ref`).
- `tests/test_review_command.py`: `test_node_writes_the_review_doc_of_a_dotted_node_id`: en el desk sandbox `lifecycle_desk` con `fake_pi`, escribe un `dag.yaml` mínimo en `desk/drawer/plans/con-punto/` (ROOT con children `[WS13.1]` y la tarea `WS13.1`), corre `deskops review node desk/drawer/plans/con-punto WS13.1 --run test-run` y comprueba rc 0, un recibo `review-deskops-con-punto-ws13.1-node-1`, `subject_ref == desk/drawer/plans/con-punto/dag.yaml#node:WS13.1` y verdict `pending`.

`.sldb/core/models/ReviewDoc.yaml` no declara pattern (grep sin coincidencias): nada que tocar ahí.

## review_id

El review_id se deriva con `node_id.lower()` y queda `review-deskops-con-punto-ws13.1-node-1`; `REVIEW_ID_PATTERN` (`review-.+-node-N`) lo admite y el recibo se escribe sin choque. Formato sin cambios.

## Validación (validation.log)

- `pytest -q tests/test_review_doc.py`: 22 passed, 1 xfailed, rc=0.
- `pytest -q tests/test_review_command.py`: 26 passed, rc=0.

No corrí la suite completa ni `stores build --check` (para el integrador). No se agregó ni cambió ningún comando del CLI, así que no aplica test_command_registry.py.

## Riesgos

Bajo: el punto solo amplía el vocabulario aceptado del id de nodo. No corrí review node sobre planes reales del drawer.
