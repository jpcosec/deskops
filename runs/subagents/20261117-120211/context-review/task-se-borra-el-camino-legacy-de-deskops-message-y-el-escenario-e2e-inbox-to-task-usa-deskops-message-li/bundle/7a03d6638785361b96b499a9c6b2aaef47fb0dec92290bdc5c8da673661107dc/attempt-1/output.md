## REFORMULACION

**Propósito:** retirar el camino legacy de `deskops message` y alinear el escenario e2e y los docstrings con `deskops message` como único comando de mensajería. **Resultado:** `deskops message` sin subcomando falla con uso claro y rc 2 sin pasar por `_run_legacy`, que se elimina; `inbox-to-task.yaml` usa `deskops message list --root .`; los docstrings dejan de presentar `deskops inbox` como vigente; los tests indicados pasan. **Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`. **Límites:** entran `deskops/cli/commands/message.py`, el escenario e2e, docstrings de `tests/test_repo_identity.py` y `tests/test_inbox_promote_cli_gaps.py`, y tests de message; quedan fuera el registro de comandos y docs.

## AMBIGUEDADES

1. “imprima el error de uso de argparse o la ayuda, con rc 2”: obliga a inventar si se usa `parser.error`, ayuda explícita u otro mecanismo, y el texto exacto.
2. “los dos docstrings dejan de presentar deskops inbox como comando vigente”: ambos archivos contienen varios docstrings; obliga a inventar cuáles son “los dos”.
3. “Cambiar la rama del escenario e2e” y “usa deskops message list --root .”: no precisa si se elimina el fallback `|| deskops list inbox-notes --root .`; obliga a inventar si se conserva.
4. “tests de message” frente a “Test: deskops message sin subcomando...”: no aclara si se modifica `test_retired_inbox_alias_is_an_unknown_command` o se añade otro test.

## DRY-RUN

**Lecturas:** `message.py`, `inbox-to-task.yaml`, `test_repo_identity.py`, `test_inbox_promote_cli_gaps.py`, `test_message_cli.py` y helpers de `test_cli.py`. **Cambios previstos:** borrar `_run_legacy` y su mención en el docstring; enrutar `message` sin subcomando a uso/ayuda con rc 2; sustituir la referencia e2e por `deskops message list --root .`; ajustar los docstrings señalados; añadir o ajustar el test de rc 2 y verbos. **Dependencias:** repo y venv disponibles, `pytest`, `sldb`; sin tocar registro ni docs. **Validaciones futuras:** los tres comandos pytest de la sección Validation, `grep _run_legacy` vacío, ausencia de `deskops inbox` en el escenario y commit descriptivo según el átomo.

## FUTURO

El closeout o un humano decide el mensaje del commit y su ejecución; otro nodo puede ejecutar el escenario e2e completo, que no figura en la Validation, y confirmar que registro y docs siguen fuera de alcance.
