# Result summary — testing independiente

run_id: run-deskops-t-873e90b300b4-a2
task: task-un-ejecutor-bloqueado-no-puede-dejar-su-tarea-en-testing-y-existe-la-vuelta-de-testing-a-execution
role: deskops-tester

## Veredicto: FAIL

La funcionalidad pedida cumple: la transición manual testing→execution se siembra, `--back
--reason` devuelve la tarea con status active y `task_returns_to_execution: <motivo>` en
history, el avance normal sigue a closeout, los tres usos incorrectos salen con 2, el nodo sin
vuelta sale bloqueado con el mensaje acordado, los post-hooks corren y el agents.md del
executor trae la regla de `sciontool status blocked`. El desk desechable creado con
`deskops init` + CLI real pasó la secuencia completa y `deskops doctor` no informó deriva.

Pero quedan dos regresiones en tests existentes, ambas causadas por los cambios de esta tarea
y ambas verdes en una copia limpia de HEAD:

1. `tests/test_closeout_gates.py::test_transitions_match_the_linked_index` — FAIL.
   `tests/closeout_graph_oracle.py` incluye la nueva arista manual y no la marca/ignora como
   manual, así que no coincide con `lifecycle.transitions_from` (que ahora excluye manuales).
2. `tests/test_packaging.py::test_desk_declaration_and_templates_ship_inside_the_package` — FAIL.
   Sigue esperando 6 RelationDoc / 22 seeds de lifecycle; ahora hay 8 / 24 por los dos seeds
   nuevos.

## Puntos PASS
- Validation 1 (`test_lifecycle_graph.py` + `test_scion_runtime.py`): 64 passed. Incluye (a)-(e).
- Validation 2 (help goldens + scaffold): PASS; solo cambió `deskops_advance_task.txt` en help
  y los dos seeds en los goldens de scaffold.
- Validation 3 (`deskops doctor` en desk recién inicializado): PASS.
- Done When funcional en desk desechable real: PASS. Secuencia probada: add task → recibos
  preflight/bundle (los mismos del repo) → advance a ritual-testing → `--back --reason "prueba"`
  a ritual-execution (active, history con motivo) → advance normal a ritual-testing →
  advance normal a ritual-closeout → doctor healthy. Desk borrado.
- `tests/test_desk_sync.py` + `tests/test_task_lifecycle_validator.py`: 47 passed.
- `tests/test_lifecycle_seed_drift.py`, `tests/test_legacy_task_states.py`: pasan; el único fallo
  del grupo es el de closeout gates ya descrito.
- Diagram/lifecycle end-to-end: 7 passed.

## Entorno
El fallback del prompt con `python3` no funciona aquí: `python3` es 3.11 y el site-packages del
venv es 3.13 (`pydantic_core` compilado). Se usó el Python 3.13 de uv:
`/home/scion/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu/bin/python3.13`, con
`PYTHONPATH=/workspace/deskops:/workspace/sldb/src:/workspace/sldb/.venv/lib/python3.13/site-packages`
y `TMPDIR=/dev/shm`.

No se editó ni commiteó nada del repo. Cambios ajenos ignorados.

## Detalle
Ver `validation.log` en este run_dir.
