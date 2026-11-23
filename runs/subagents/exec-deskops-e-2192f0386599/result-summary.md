# Result summary
run_id: exec-deskops-e-2192f0386599

Hecho (commit en rama deskops/deskops-e-2192f0386599, trailer Task-Id):
- `deskops queue job set <job> <field> <value> --root .` (deskops/queue.py, deskops/cli/registry.py): valor JSON o string, valida con QueueJob, reescribe solo esa entrada de desk/config.json; error (exit 2) sin tocar el archivo si job/campo/valor es inválido.
- deskops/data/templates/config.json (seed de init): declara dispatch-executor/tester/reap con retry_exit_codes [3].
- desk/config.json: dispatch-reap con retry_exit_codes [3], aplicado con el comando nuevo.
- tests/test_queue_cli.py (nuevo), CHANGELOG.md, docs/operator-manual.md.

Validación: tests/test_queue_cli.py + tests/test_queue.py: 21 passed.
Anotación: la suite completa con -n 4 no terminó a tiempo (se lanzó con -n 4); se entrega con tests enfocados por indicación del coordinador. Revisar.
Nota: el venv /tmp/ws-venv es editable sobre el checkout principal; los tests CLI usan PYTHONPATH del worktree.
