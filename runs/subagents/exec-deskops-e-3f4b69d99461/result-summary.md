# Resultado del ejecutor deskops-e-3f4b69d99461

Tarea: `task-el-test-de-llaves-de-message-send-deja-de-ser-xfail-porque-sldb-ya-renderiza-los-valores-literales`

## Cambio

- `tests/test_message_cli.py`: quité `@pytest.mark.xfail(strict=True, reason=SLDB_JINJA_VALUE_NOTE)` de
  `test_message_send_keeps_braces_in_the_body_literal`. También borré la constante `SLDB_JINJA_VALUE_NOTE` y el comentario
  que la precedía, que explicaba la causa ya resuelta. Precisión 1: `grep -rn SLDB_JINJA_VALUE_NOTE tests/ deskops/` solo la
  encontraba en ese archivo y ahora no la encuentra en ningún lado (rc=1).
- Las 4 variantes del parametrize no cambian (precisión 2).
- El diff solo toca ese archivo. No modifiqué el código de deskops ni el de sldb.

## Procedencia de sldb (precisión 3 e implementation_path 1). Hay que leerlo

- El venv importa sldb de `/mnt/ssd/herramientas/sldb/src`, que está en `6e793686` con HEAD detached.
  `git -C /mnt/ssd/herramientas/sldb merge-base --is-ancestor d49f6ddc HEAD` da **rc=1**: ese checkout **no** incluye d49f6ddc.
  Lo confirmé a mano: `render_model_markdown(InboxNoteDoc, ...)` con ese sldb devuelve `49` para `{{ 7*7 }}` y lanza
  `TemplateSyntaxError` para `texto {{a fin`.
- Los tests no usan ese sldb. `tests/conftest.py` pone primero en `sys.path` el checkout hermano `../sldb/src`
  (o `$SLDB_SRC` si está definido). Ese checkout es `/mnt/ssd/proyectos/SLDB_1/sldb`, en `0590ed11` (main), y
  `merge-base --is-ancestor d49f6ddc HEAD` da **rc=0**. Por eso las 4 variantes daban XPASS y ahora pasan.
- Conclusión: el goal se cumple tal como la suite resuelve sldb, que es contra lo que corre el integrador. La premisa del
  rationale ("ya instalado en /mnt/ssd/herramientas/sldb") es falsa.

## Validación (validation.log)

- `PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -rxX tests/test_message_cli.py`: **16 passed, rc=0**
  (sin xfail ni XPASS, en 166 s). Antes del cambio, las 4 variantes daban XPASS(strict) y quedaban como FAILED.
- Para el integrador: el diff de la tarea es solo `tests/test_message_cli.py` (-10 líneas). Los cambios de `.sldb/` que
  aparecen en git-status.txt ya estaban antes de que yo empezara y no son míos.
- No corrí la suite completa ni `stores build --check`, por orden del integrador.

## Riesgos

- **El deskops desplegado sigue expuesto**: el CLI que usa el venv (sldb de herramientas en 6e793686) todavía compila como
  Jinja el cuerpo de `deskops message send`. Hay que desplegar sldb en `/mnt/ssd/herramientas/sldb` (avanzarlo a main) para
  que la conducta real coincida con la de los tests. Eso queda fuera del scope de esta tarea y lo decide el coordinador.
- Si alguien corre la suite con `SLDB_SRC` apuntando a herramientas, o sin el checkout hermano, el test vuelve a fallar
  (ahora como FAILED, ya no como XPASS).
