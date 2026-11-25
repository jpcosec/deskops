FILE:desk/tasks/task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt.md
---
sldb:
  by: agent
  at: '2026-11-23T04:38:53Z'
  authority: generated
  via: create_document
id: task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261123-024325-suggestion-campo-propio-para-la-referencia-de-conversacion-scion-en-atoms-y-notas.md
depends_on: []
pills: []
files:
- deskops/models/atom.py
- deskops/models/inbox.py
- deskops/cli/commands/atoms.py
- deskops/cli/commands/message.py
- tests/test_atoms_cli.py
- tests/test_message_cli.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# AtomDoc e InboxNoteDoc ganan conversation_ref, add atom y message send aceptan --conv y list atoms filtra por --conv

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-024325 (hilo #acuerdos-sldb1 del proyecto scion wf-desks, encargo de JP vía scion-coordination): hoy la referencia conv/#hilo de un acuerdo va en --provenance y en el texto del atom (así lo hace /mnt/ssd/proyectos/wf-desks/bin/desk-prompt.sh), y no se pueden listar los acuerdos de una conversación. Se pide un campo propio.

## Goal

_Describe the concrete result this task must produce._

(1) AtomDoc (deskops/models/atom.py) e InboxNoteDoc (deskops/models/inbox.py) ganan conversation_ref: str | None (por defecto None), con la forma "<hilo>/<id de mensaje>" o solo "<hilo>" (por ejemplo "#acuerdos-sldb1/1234"); vacío no se escribe. (2) deskops add atom --conv <ref> y deskops message send --conv <ref> lo llenan. (3) deskops list atoms --conv <hilo> lista solo los atoms cuyo conversation_ref es ese hilo o empieza por "<hilo>/"; con --format json incluye el campo. (4) deskops add atom con un --conv que ya tiene otro atom avisa en stderr "ya existe <atom id> con conversation_ref <ref>" y no crea un duplicado (sale con código 1).

## Scope

_State what is in scope and what is out of scope._

Entra: los dos modelos, deskops/cli/commands/atoms.py, deskops/cli/commands/message.py, los goldens de contrato y de ayuda, sldb models update de los dos modelos en el store del desk, tests/test_atoms_cli.py y tests/test_message_cli.py. No entra: un verbo nuevo add agreement (el campo cubre el pedido), migrar los atoms viejos que tienen la referencia en provenance.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_atoms_cli.py: test_add_atom_with_conv_writes_conversation_ref, test_list_atoms_filters_by_conv, test_add_atom_refuses_duplicate_conv. p2: test en tests/test_message_cli.py: test_send_with_conv_writes_conversation_ref. p3: implementar. p4: goldens y sldb models update AtomDoc e InboxNoteDoc en .sldb. p5: suite con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_atoms_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_model_contract_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los cuatro tests nuevos pasan, deskops doctor --root . no suma errores por los atoms e inbox existentes (que no traen el campo), y sldb stores check --store .sldb no suma errores nuevos.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

