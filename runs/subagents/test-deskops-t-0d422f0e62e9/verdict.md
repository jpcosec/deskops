# Veredicto del tester deskops-t-0d422f0e62e9

Tarea: task-el-test-de-llaves-de-message-send-deja-de-ser-xfail-porque-sldb-ya-renderiza-los-valores-literales

## Hallazgos

1. Diff (tests/test_message_cli.py, -10 líneas): solo quita `@pytest.mark.xfail(strict=True, ...)`, la constante `SLDB_JINJA_VALUE_NOTE` y su comentario. Las 4 variantes del parametrize de `test_message_send_keeps_braces_in_the_body_literal` no cambian. La constante no queda referenciada en tests/ ni deskops/.
2. Procedencia: la suite importa sldb de `../sldb/src` (tests/conftest.py, `_SIBLING_SLDB_SRC`), HEAD 3b3c51fe, que incluye d49f6ddc. Tanto `../.venv` como el CLI instalado (uv tool deskops; `~/herramientas` es symlink a `/mnt/ssd/herramientas`) importan `/mnt/ssd/herramientas/sldb` en 6e793686, que NO incluye d49f6ddc. Se confirma lo que informó el ejecutor; la precisión (3) del preflight (que esperaba /mnt/ssd/herramientas/sldb) no aplica a la suite.
3. `PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -rxX tests/test_message_cli.py`: 16 passed, sin xfail ni XPASS.
4. Contraprueba con `SLDB_SRC=/mnt/ssd/herramientas/sldb/src -k braces`: 4 failed. El test vuelve a fallar con un sldb sin d49f6ddc, así que pinchea el contrato de verdad.

## Observación (no bloquea la entrega)

El sldb desplegado en /mnt/ssd/herramientas (el que usan el CLI y ../.venv) sigue sin d49f6ddc: `deskops message send` real todavía altera las llaves hasta que se actualice esa herramienta. Es decisión del coordinador, fuera del alcance de esta tarea.

No corrí la suite completa (por encargo). Nada editado fuera de este directorio.

VEREDICTO: APROBADO
