# Veredicto del tester deskops-t-69899116f4ae

Tarea: task-valores-con-llaves-rompen-edit-task-message-send-y-closeout-reason-y-closeout-verify-escribe-recibos (task.debug)
Entrega: cambios sin commitear del ejecutor deskops-e-a9bb6500e6e2. Evidencia: `validation.log` en este directorio.

## 1. Diff frente a las decisiones (reproduction-1, preflight-3)

- **(a) solo texto**: `deskops/cli/registry.py:1675` cambia la ayuda corta y `registry.py:1696-1700` añade un párrafo "Writes:" que dice que verify escribe un recibo por cada tipo de evidencia declarado (el ReviewDoc y `desk/reviews/<task>/evidence-<kind>-<n>.md`), sin commitearlos. La escritura no se mueve. Los goldens `deskops_closeout.txt` y `deskops_closeout_verify.txt` coinciden con la ayuda. Cumple.
- **`mutates=True` en verify** (`registry.py:1685`): el único consumidor del flag es `deskops/cli/main.py:155-162` (`_apply_test_root_override`). Cuando verify se corre **sin `--root` explícito** y hay `DESKOPS_TEST_ROOT` o un sandbox configurado, ahora va al sandbox desk; antes escribía recibos en el desk real. Eso es correcto, porque verify sí escribe. También concuerda con `closeout commit/supersede/retire/resolved-by`, que ya son `mutates=True`. No hay más efectos de comportamiento: con `--root` explícito no cambia nada. `tests/test_command_registry.py` lo fija.
- **(b) línea de éxito** (`deskops/services/closure.py:864-866`): `.format` se cambia por `.replace("{commit}", sha, 1)`. Todas las `success_line` (líneas 199/271/409/531/652) empiezan por el literal `{commit}`, así que solo se sustituye el primer placeholder, y un `{commit}` dentro del reason queda literal (hay un test para eso). Cumple.
- **(b) proyección en el commit de cierre** (`closure.py:765-770`): está dentro de `_close`, que es el camino común de commit, manual, supersede, resolved-by, legacy-resolved y retire. Por eso todos esos cierres hacen `git add -A desk/reviews/<task>/` y lo meten en el commit. Lo juzgo correcto:
  - El alcance se limita al directorio de la propia tarea.
  - Va en paralelo al `git add -A .sldb` previo, que ya mete los ReviewDoc de esos recibos en todos los modos. Antes el commit tenía el ReviewDoc pero no su proyección, que era justo la inconsistencia del caso (b).
  - Con `--paths` el directorio entra en el pathspec. Sin `--paths` queda en el índice que se commitea.
  - Riesgo menor: un supersede/retire también se lleva al commit los recibos sin commitear de esa tarea, por ejemplo un preflight o una reproducción pendientes. Son de la misma tarea que se cierra, así que lo acepto.
- **(c)**: `tests/test_message_cli.py:265-295` marca el test con `xfail(strict=True, reason=SLDB_JINJA_VALUE_NOTE)`. Ese reason es el nombre exacto de la nota y cubre 2 y 3 llaves de apertura y la pérdida silenciosa `{{ 7*7 }}`→`49`.

## 2. Tests (de a un archivo, PYTHONPATH al checkout, TMPDIR=/dev/shm)

| archivo | resultado |
|---|---|
| test_closeout.py | 70 passed |
| test_message_cli.py | 9 passed, 4 xfailed |
| test_command_registry.py | 3 passed |
| test_closeout_evidence_receipts.py | 5 passed |
| test_cli_grammar.py | 2 passed |
| test_output_goldens.py | 7 passed (438 s; la carga bajó a ~7 y lo corrí entero) |

Con `--runxfail`, los 4 xfail fallan por la causa documentada: 3 con `TemplateSyntaxError` (rc 3) y 1 con el cuerpo guardado como `valor 49 y  fin`. No es una falla de setup.

No corrí la suite completa porque el encargo lo prohíbe.

## 3. Reproducción con el closure.py de HEAD (copia en /dev/shm, ya borrada)

- Con `closure.py` = HEAD fallan los 8 tests nuevos de (b): 7 parametrizaciones de llaves (rc 1 o línea alterada) y el de la proyección.
- El test de la proyección usa `--reason "cierre {a}"`, así que podría estar fallando solo por las llaves. Para descartarlo corrí HEAD más **solo** el arreglo de `.format`. Sigue fallando con `'?? desk/reviews/' == ''`. Ese test prueba la proyección por sí mismo.

## 4. Nota a sldb

Existe `/mnt/ssd/proyectos/SLDB_1/sldb/desk/inbox/20261117-015212-suggestion-render-model-markdown-interpreta-como-jinja-el-valor-de-los-campos-llaves-dobles-rompen-expresiones-se-evaluan.md`, y su nombre es idéntico a `SLDB_JINJA_VALUE_NOTE`.

## Observaciones no bloqueantes (para el cierre)

1. `files:` del TaskDoc lista `deskops/cli/commands/closeout.py`, que la entrega no toca. No lista `deskops/cli/registry.py`, `tests/test_command_registry.py` ni los dos goldens de ayuda, que sí cambian. Conviene alinear `files:` con la entrega antes del commit de cierre.
2. El xfail de (c) solo cubre `message send`. `edit task` comparte el mismo origen en sldb (`replace_markers`) pero no tiene un xfail propio. El Done When ("(c) tiene test verde o xfail citando la nota") se cumple igual.

VEREDICTO: APROBADO
