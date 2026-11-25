## REFORMULACION

El nodo es un TaskDoc ejecutable, no un agregado ni paquete. **Propósito:** retirar el resto legacy de `deskops message` tras el retiro de `deskops inbox`. **Resultado:** `deskops message` sin subcomando falla con ayuda/error de uso y rc 2, sin `_run_legacy`; el e2e usa `deskops message list --root .`; dos docstrings dejan de presentar `deskops inbox` como vigente. **Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`. **Límites:** entran `deskops/cli/commands/message.py`, el escenario e2e, los dos tests citados (solo docstrings) y tests de message; quedan fuera el registro de comandos y docs.

## AMBIGUEDADES

1. “el error de uso claro (la ayuda de message con sus subcomandos)” frente a “el error de uso de argparse o la ayuda, con rc 2”: no se fija salida exacta, stream ni si se imprime ayuda completa o error breve. Obliga a inventar el texto y el canal.
2. “los dos docstrings dejan de presentar deskops inbox como comando vigente”: no se identifican líneas ni redacción esperada. Obliga a inventar qué frase reemplazar y por cuál.
3. “cae a su alternativa con ||”: no se aclara si el fallback debe eliminarse o conservarse al cambiar la rama principal. Obliga a inventar el tratamiento del `||`.
4. “Test: deskops message sin subcomando da rc 2 y nombra send, list, read y ack”: no se indica si se añade a `tests/test_message_cli.py` o se modifica otro test. Obliga a inventar ubicación y forma.

## DRY-RUN

**Lecturas:** `message.py`, escenario `inbox-to-task.yaml`, `test_repo_identity.py`, `test_inbox_promote_cli_gaps.py`, `test_message_cli.py` y registro/CLI para confirmar el flujo. **Cambios previstos:** borrar `_run_legacy` y su docstring; hacer que message sin subcomando muestre uso/ayuda con rc 2; sustituir la rama e2e por `deskops message list --root .`; ajustar los dos docstrings; añadir o ajustar el test de rc 2 y subcomandos. **Dependencias:** estructura argparse vigente, ausencia de `deskops inbox` en registro y utilidades del escenario. **Validaciones futuras:** los tres pytest de Validation, grep de `_run_legacy` y grep del escenario. Sin ejecutar nada.

## FUTURO

Otro nodo ejecutor aplicará los cambios y correrá las validaciones. Un humano decidirá si la redacción final de ayuda, docstrings y fallback e2e satisface la intención, y si procede commit/closeout.
