# Resultado
Files: deskops/integrate.py, tests/test_integrate.py
- integrate.py: _resolve_failed, tras un integrate real exitoso (push o 'ya integrado'; no dry-run, no modo pr) mueve a done los JSON de runs/queue/failed con kind integrate cuyo commit 'Task-Id: <id>' en la rama local es ancestro de lo recien traido del remoto; agrega al log la linea 'resuelto por integrate <task>: <sha> ya en origin/<branch>'.
- Tests: test_integrate_moves_failed_already_in_origin_to_done, test_integrate_keeps_failed_not_in_origin.
- Validacion: ver validation.log. Nota: con -n 4 el archivo falla por basetemp compartido (PYTEST_ADDOPTS), sin -n pasa.
- Revisar: el fetch usa cfg.remote_url en root (solo FETCH_HEAD); en modo pr el barrido solo corre en 'ya integrado'.
