# result-summary
run_id: exec-deskops-e-b526639a788c

Hecho (commit en rama deskops/deskops-e-b526639a788c, Task-Id en el cuerpo):
- deskops/dispatch.py: constante SCION_PYTEST_TMP=/dev/shm/pytest-of-scion; seccion "Temporales de pytest" (export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-<agente>") en el prompt de executor y tester (_role_instructions recibe name); reap borra SCION_PYTEST_TMP e imprime "limpieza: <ruta>" si tras reapear no queda agente running en el proyecto, y no lo toca si queda alguno.
- tests/test_dispatch.py: test_prompt_sets_pytest_basetemp_in_container_tmp (executor y tester), test_reap_cleans_scion_pytest_tmp_when_no_agent_is_alive, test_reap_keeps_scion_pytest_tmp_while_an_agent_runs.

Archivos: deskops/dispatch.py, tests/test_dispatch.py

Validacion: tests/test_dispatch.py 49 passed. Suite completa -n 4: 1349 passed, 1 failed:
tests/test_global_store_isolation.py::test_deskops_init_does_not_touch_the_real_global_store (hash del store global real cambio durante la corrida de 93 min; ajeno a este cambio, a revisar por el supervisor/re-ejecutar aislado).
