PASA

# Resultado del tester (a2)

Tarea: task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt
Run: exec-deskops-t-1ec12a48e094-a2-testing

## Commits evaluados

- `3db148a0b73c7b314ab805c04685c05680e03cc2` — código y tests: AtomDoc e InboxNoteDoc ganan conversation_ref; --conv en add atom, message send y list atoms. Trailer `Task-Id:` verificado.
- `1b44a9d95e21bb370f665e88a4bff9012be893ed` — `sldb stores update`: contract_hash nuevo de AtomDoc e InboxNoteDoc. Trailer verificado.
- `44e71c26056b36b0d27a657cbf9dfe858341e67f` — store tras conversation_ref (re-extracción, hashes y documentos actualizados). Trailer verificado.
- `796ca0d845f47dba288d8847392a6929ef844619` — re-extracción de stores update. Trailer verificado.

El código evaluado coincide con HEAD en `deskops/` y `tests/` para los módulos de la tarea.

## Veredicto

La funcionalidad pedida y sus tests pasan. También se corrigió el motivo del FALLA anterior: los commits de store actualizaron `contract_hash` y re-extrajeran los documentos, por lo que `deskops doctor --root .` ya **no** reporta errores de AtomDoc ni de InboxNoteDoc. El Done When se cumple para atoms e inbox.

Verificado:
- `.sldb/core/models/AtomDoc.yaml` y `.sldb/core/models/InboxNoteDoc.yaml` tienen los hashes nuevos (`84cf8be0…` y `923f97f6…`), iguales a `tests/fixtures/model_contract_hashes.json`.
- `deskops doctor --root .`: 0 errores de AtomDoc/InboxNoteDoc (antes del fix había 2). Los errores restantes son de RunDoc/ReviewDoc por drift de extracción de una versión de sldb, ajenos a esta tarea.
- `sldb stores check --store .sldb`: 0 errores de AtomDoc/InboxNoteDoc; los 195 errores y 846 alertas son de RunDoc/ReviewDoc y de receipts `anchors/doc_lost` ya existentes en main, no de los modelos tocados.
- En el commit padre `d5ad7dd4`, el baseline ya traía 210 errores (incluido 1 InboxNoteDoc por `ack_reason`, corregido por estos commits de store); ahora hay 195 y ninguno de AtomDoc/InboxNoteDoc. No se suman errores nuevos por estos modelos.

## Comportamiento comprobado

Los cuatro tests nuevos pasan:
- `test_add_atom_with_conv_writes_conversation_ref`: `--conv` se escribe en el atom; un atom sin `--conv` no lleva el campo.
- `test_list_atoms_filters_by_conv`: filtra por `ref == hilo` o `ref` que empieza por `hilo + "/"` (no confunde `#acuerdos-sldb1` con `#acuerdos-sldb10`); `--format json` incluye `conversation_ref`.
- `test_add_atom_refuses_duplicate_conv`: duplicado exacto sale con 1, escribe en stderr `ya existe <atom id> con conversation_ref <ref>` y no crea el archivo.
- `test_send_with_conv_writes_conversation_ref`: `message send --conv` escribe la referencia en la InboxNote del destino y la nota se puede leer.

Además, los goldens de ayuda regenerados (`deskops_add_atom.txt`, `deskops_list_atoms.txt`, `deskops_message_send.txt`, `deskops_add_inbox-note.txt`) coinciden.

## Tests ejecutados (de a uno)

Entorno: el `.venv` del checkout está roto en este contenedor (apunta a `/usr/bin/python3.12`, ausente; el `python3` real es 3.11). Se creó un CPython 3.12.16 con `uv` en `/tmp/deskops-test-venv-a2` y se instalaron ahí el proyecto, sldb local, pytest y pytest-xdist. No se modificó el repo para esto. `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-1ec12a48e094-a2`, `TMPDIR=/tmp`.

```text
tests/test_atoms_cli.py                 -> 7 passed
tests/test_message_cli.py               -> 18 passed
tests/test_model_contract_snapshot.py   -> 2 passed
tests/test_output_goldens.py            -> 7 passed
tests/test_model_validators.py          -> 14 passed
tests/test_command_registry.py          -> 3 passed
tests/test_operational.py               -> 8 passed
tests/test_message_delivery.py          -> 9 passed
tests/test_atom_folder_axis.py          -> 13 passed
tests/test_cli_grammar.py               -> 2 passed
tests/test_cli_contract.py              -> 8 passed
tests/test_registry_robustness.py       -> 8 passed
```

No se corrió la suite completa.

## Conclusión

PASA: los cuatro tests nuevos y los archivos de test de los módulos tocados pasan; el campo se escribe, se filtra, aparece en JSON y el duplicado se rechaza; el store del desk quedó actualizado y doctor no suma errores para AtomDoc/InboxNoteDoc.
