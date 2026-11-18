# Result: python venv in scion containers

Chosen route (a). Measured in this scion-claude container: `uv venv /tmp/ws-venv --python 3.12` 27.9 s (downloads CPython 3.12.16),
`uv pip install -e ".[dev]" -e ../sldb` 2.2 s; total ~30 s. `tests/test_dispatch.py`: 18 passed (188 s).
Note: the task text's `/mnt/ssd/herramientas/sldb` does not exist; sldb lives at `<workspace>/sldb` (parent of DESKOPS_SLDB_SOURCE_ROOT), which the template derives from the context.
Scion has no start hook, so the step is a "Python environment (run first)" section in the generated agents.md (executor and tester). Route (b) not needed.

Files changed: deskops/runtime/scion.py, tests/test_scion_runtime.py, docs/operator-manual.md, plus new atom (deskops add atom) under .sldb.
Validation: see validation.log. Review: the test_dispatch run used the manually run commands equal to the template's; a dispatched container using the new template was not launched from here.
Commit: code + atom committed with Task-Id (scion.py, test_scion_runtime.py, operator-manual.md, atom md+yaml). store_index and model yaml changes left uncommitted.
