PASA

# Veredicto del tester

El commit del ejecutor cumple el Done When: `add task` rechaza items de lista no string antes de crear la tarea, con un mensaje que nombra el campo y el indice y sugiere entrecomillar; el mismo item entrecomillado crea la tarea con la linea literal. No hay hallazgos bloqueantes.

## Commit evaluado

- Commit: `4963966abd4f79e47b5a4f8ba75cf40fb84d4929`
- Mensaje: `add task --from-yaml rechaza items de lista no string`
- Trailer: `Task-Id: task-add-task-from-yaml-rechaza-un-item-de-lista-que-yaml-leyo-como-dict-igual-que-edit-task`
- Archivos:
  - `deskops/cli/parse_input.py`
  - `tests/test_cli.py`

## Implementacion verificada

`parse_task_input` carga el YAML/JSON y llama a `_ensure_string_list_items` antes de crear el bundle. La funcion recorre `validation`, `depends_on`, `inherits_from`, `atoms`, `evidence`, `closeout_evidence` y `references`, y lanza `ValueError` si un item no es `str`. El error incluye campo, indice (`item 0`), tipo encontrado y la sugerencia de entrecomillar cuando el item contiene `': '`. Al ocurrir antes de `create_task_bundle`, no se escribe `desk/tasks/<id>.md`.

## Pruebas ejecutadas

Nota de entorno: el `../.venv` indicado en la Validation apunta a un Python 3.12 ausente en este contenedor y su `python` resuelve a 3.11 sin pytest. Use el venv funcional `/dev/shm/t311` con `PYTHONPATH` al repo y a `sldb/src`.

- `TMPDIR=/tmp .../python -m pytest -q tests/test_cli.py`
  - Resultado: **103 passed**, exit 0 (incluye el test nuevo `test_add_task_from_yaml_rejects_unquoted_colon_list_item`).
- `TMPDIR=/tmp .../python -m pytest -q tests/test_add_task_from_drawer.py`
  - Resultado: **3 passed**, exit 0.
- No existe `tests/test_parse_input.py`; el modulo tocado no tiene archivo de test dedicado. No se corrio la suite completa.

## Chequeos manuales adicionales

- Payload JSON inline posicional (`deskops add task '<json>'`) con `validation` conteniendo `{"Suite completa, bajo flock /dev/shm/x.lock": "CMD foo"}`:
  - exit 1, mensaje `Field 'validation' item 0 must be a string, got dict... wrap it in quotes`, y `desk/tasks/` sin archivos.
- El mismo payload JSON con el item como string:
  - exit 0 y la tarea contiene `- Suite completa, bajo flock /dev/shm/x.lock: CMD foo`.
- YAML sin comillas: falla sin crear `task-*.md`; YAML con comillas: crea la tarea con la linea literal (cubierto por el test nuevo).
