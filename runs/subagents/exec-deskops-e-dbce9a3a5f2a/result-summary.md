# result-summary
- scion.py: `_command_args(role_doc, profile, harness="")`; si harness == "pi" emite opcion y valor como dos elementos; otros harness conservan `opcion=valor`. El llamador pasa `harness`.
- tests/test_scion_runtime.py: nuevo `test_pi_tools_are_option_and_value_as_separate_args` (espera `["--tools", "read,grep,bash"]`).
- operator-manual.md: no menciona command_args; sin cambios. Sin cambio de ayuda CLI, sin goldens.
- VALIDACION NO EJECUTADA: ni /usr/bin/python3, ni /mnt/ssd/proyectos/SLDB_1/.venv, ni /workspace/.venv tienen pytest ni yaml. No hay validation.log. No corri advance.
- Supervisor: ejecutar `TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py` en un entorno con dependencias.
