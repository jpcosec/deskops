# Resultado (segundo intento, acotado)
Cambios (solo declaraciones, sin tocar el trabajo previo):
- tests/test_cli.py: lista de primer nivel ahora `...,message,queue,review,...`.
- tests/test_cli_grammar.py: `queue` en TOP_LEVEL_GRAMMAR["operational"] (junto a message).
- tests/test_command_registry.py: MUTATING_COMMANDS += ("queue",), ("queue","add"), ("queue","run").
- grep de otras listas de primer nivel (docs/README/deskops/*.py): sin coincidencias que actualizar.

Tests (python3.13 + site-packages de /workspace/sldb/.venv, porque el .venv del proyecto es py3.12 y el contenedor solo tiene 3.13):
`pytest tests/test_cli.py tests/test_cli_grammar.py tests/test_command_registry.py tests/test_queue.py tests/test_output_goldens.py -k "help_uses_deskops_name or top_level_nouns or mutating_commands or queue or help"`
=> 21 passed, 1 failed. Los 3 guardianes y los goldens de help en verde.
Fallo: tests/test_queue.py::test_concurrent_runs_execute_once: ambiental. El test lanza subprocesos con PYTHONPATH=ROOT, que reemplaza mi PYTHONPATH, y el subproceso falla con `No module named 'sldb.store'` (sldb equivocado en este entorno improvisado). El supervisor debe reejecutarlo en el venv real.
No se corrio `deskops advance`. Sin git add/commit.
