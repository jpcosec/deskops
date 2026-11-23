FALLA

# Resultado del tester

Tarea: task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt
Run: exec-deskops-t-1ec12a48e094-testing
Commit evaluado: `3db148a0b73c7b314ab805c04685c05680e03cc2` — "AtomDoc e InboxNoteDoc ganan conversation_ref; --conv en add atom, message send y list atoms".
Trailer verificado: `Task-Id: task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt`.
El código evaluado coincide con HEAD en `deskops/` y `tests/` (`git diff 3db148a0..HEAD -- deskops tests` vacío).

## Veredicto

La funcionalidad nueva y sus tests pasan, incluidos los cuatro tests pedidos y los goldens de ayuda. Pero **no cumple el Done When**: `deskops doctor --root .` suma dos errores nuevos para AtomDoc e InboxNoteDoc porque el store del desk (`.sldb`) no fue actualizado con `sldb models update` como exige el Scope/Implementation Path p4.

## Evidencia del incumplimiento

`deskops doctor --root .` termina con exit 1 y, en la sección "Errors (the desk is broken)", agrega exactamente:

```text
- AtomDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
- InboxNoteDoc: the model's contract (field schema or __template__) changed since it was indexed: extraction yields something else from the same text — `sldb stores update` re-extracts this model's documents
```

La causa es verificable en el store versionado:

- `.sldb/core/models/AtomDoc.yaml` sigue con `contract_hash: ee1a85c1...`, el hash viejo, mientras el fixture actualizado declara `84cf8be0...`.
- `.sldb/core/models/InboxNoteDoc.yaml` sigue con `contract_hash: 963ba769...`, mientras el fixture actualizado declara `923f97f6...`.
- `grep -rl conversation_ref .sldb` no devuelve ningún archivo: ni los modelos ni los documentos del store conocen el campo nuevo.
- El único cambio `.sldb` del commit es un documento InboxNoteDoc ajeno (`...ack_reason`), no la actualización de metadatos de AtomDoc/InboxNoteDoc que pedía la tarea.

Esto incumple tanto el Scope ("sldb models update de AtomDoc e InboxNoteDoc en el .sldb del repo") como el Done When ("deskops doctor --root . no suma errores por los atoms e inbox existentes"). `sldb stores check --store .sldb` también sale con exit 1, pero por alertas `anchors/doc_lost` preexistentes; no es el motivo del veredicto.

## Tests ejecutados (de a uno, sin correr la suite completa)

Entorno: el `.venv` del checkout está roto en este contenedor (apunta a `/usr/bin/python3.12`, ausente; el `python3` real es 3.11). Instalé con `uv` un CPython 3.12.16 en `/tmp/deskops-test-venv` y ahí las dependencias del proyecto, pytest y pytest-xdist. No se modificó el repo para esto.

```text
TMPDIR=/tmp .../python -m pytest -q -p no:cacheprovider tests/test_atoms_cli.py              -> 7 passed
TMPDIR=/tmp .../python -m pytest -q -p no:cacheprovider tests/test_message_cli.py           -> 18 passed
TMPDIR=/tmp .../python -m pytest -q -p no:cacheprovider tests/test_model_contract_snapshot.py -> 2 passed
TMPDIR=/tmp .../python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py        -> 7 passed
TMPDIR=/tmp .../python -m pytest -q -p no:cacheprovider tests/test_model_validators.py      -> 14 passed
TMPDIR=/tmp .../python -m pytest -q -p no:cacheprovider tests/test_command_registry.py      -> 3 passed
TMPDIR=/tmp .../python -m pytest -q -p no:cacheprovider tests/test_operational.py           -> 8 passed
TMPDIR=/tmp .../python -m pytest -q -p no:cacheprovider tests/test_message_delivery.py      -> 9 passed
TMPDIR=/tmp .../python -m pytest -q -p no:cacheprovider tests/test_atom_folder_axis.py      -> 13 passed
TMPDIR=/tmp .../python -m pytest -q -p no:cacheprovider tests/test_cli_grammar.py           -> 2 passed
TMPDIR=/tmp .../python -m pytest -q -p no:cacheprovider tests/test_cli_contract.py          -> 8 passed
TMPDIR=/tmp .../python -m pytest -q -p no:cacheprovider tests/test_registry_robustness.py   -> 8 passed
TMPDIR=/tmp .../python -m pytest -q -p no:cacheprovider tests/test_doctor_model_registration.py tests/test_doctor_sldb_layout.py -> 33 passed
```

Los cuatro tests nuevos (`test_add_atom_with_conv_writes_conversation_ref`, `test_list_atoms_filters_by_conv`, `test_add_atom_refuses_duplicate_conv`, `test_send_with_conv_writes_conversation_ref`) pasan y el comportamiento observable coincide con el Goal: `--conv` se escribe, el filtro por hilo respeta `ref == hilo` o `hilo/...`, el duplicado exacto se rechaza con stderr y exit 1, y las ayudas se regeneraron.

## Corrección necesaria

Desde la raíz del worktree, ejecutar y commitear el resultado de:

```text
sldb models update AtomDoc --store .sldb --pythonpath .
sldb models update InboxNoteDoc --store .sldb --pythonpath .
```

y verificar que `deskops doctor --root .` ya no reporte los dos errores de contrato de AtomDoc/InboxNoteDoc.
