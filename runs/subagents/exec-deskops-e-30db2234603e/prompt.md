Task: task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt
Title: AtomDoc e InboxNoteDoc ganan conversation_ref, add atom y message send aceptan --conv y list atoms filtra por --conv
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-23T05:07:56Z'
  authority: generated
  via: save_document_payload
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
- deskops/cli/registry.py
- deskops/cli/commands/operations.py
- deskops/operations.py
- deskops/services/atoms.py
- deskops/cli/commands/message.py
- tests/test_atoms_cli.py
- tests/test_message_cli.py
- tests/fixtures/model_contract_hashes.json
- tests/fixtures/golden/help/deskops_add_atom.txt
- tests/fixtures/golden/help/deskops_list_atoms.txt
- tests/fixtures/golden/help/deskops_message_send.txt
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

Entra: los dos modelos, la superficie real de add atom y list atoms (deskops/cli/registry.py, deskops/cli/commands/operations.py, deskops/operations.py, deskops/services/atoms.py), deskops/cli/commands/message.py, tests/fixtures/model_contract_hashes.json, los goldens de ayuda deskops_add_atom.txt, deskops_list_atoms.txt y deskops_message_send.txt, sldb models update de AtomDoc e InboxNoteDoc en el .sldb del repo, tests/test_atoms_cli.py y tests/test_message_cli.py. No entra: deskops/cli/commands/atoms.py (los alias viejos deskops atoms ... no ganan --conv), un verbo nuevo add agreement (el campo cubre el pedido), migrar los atoms viejos que tienen la referencia en provenance.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_atoms_cli.py (usan main(["add", "atom", "--root", ...]) en proceso, como los existentes): test_add_atom_with_conv_writes_conversation_ref, test_list_atoms_filters_by_conv, test_add_atom_refuses_duplicate_conv. p2: test en tests/test_message_cli.py: test_send_with_conv_writes_conversation_ref. p3: implementar. Superficie real (verificada): deskops add atom NO pasa por deskops/cli/commands/atoms.py (AtomsCLI es "deskops atoms ...", alias viejos); sus flags se generan de los campos del modelo en _add_subject_commands de deskops/cli/registry.py, el payload lo arma parse_artifact_input (deskops/cli/parse_input.py) y el add lo hace OperationsCLI (deskops/cli/commands/operations.py, rama args.command == "add") con doc_access.create_artifact. El campo nuevo genera solo --conversation-ref; --conv se agrega como alias del mismo argumento (flags ("--conversation-ref", "--conv")) en _add_subject_commands. deskops list atoms lo atiende OperationsCLI (rama list atoms) -> DeskopsOperations.list_atoms (deskops/operations.py) -> AtomsService.list_atoms (deskops/services/atoms.py); --conv se declara en _list_subject_commands (registry.py, junto a --axis-value) y se pasa como segundo filtro. message send --conv se declara en el Command ("message", "send") de registry.py (dest conversation_ref) y _deliver_note (deskops/cli/commands/message.py) lo agrega al payload. Semantica: comparacion literal sin normalizar "#"; vacio = None o solo espacios, no se escribe; el filtro de list acepta ref == hilo o ref que empieza por hilo + "/"; duplicado = otro atom con conversation_ref exactamente igual (tras strip), chequeado antes de crear en la rama add de OperationsCLI, mensaje a stderr "ya existe <atom id> con conversation_ref <ref>" y return 1 (add no tiene --format); message send no chequea duplicados; los atoms con la referencia solo en provenance no se listan. p4: contrato y goldens: actualizar AtomDoc e InboxNoteDoc en tests/fixtures/model_contract_hashes.json; regenerar goldens de ayuda con TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py --update-golden (cambian tests/fixtures/golden/help/deskops_add_atom.txt, deskops_list_atoms.txt, deskops_message_send.txt) y revisar el diff; en el store del desk: sldb models update AtomDoc --store .sldb --pythonpath . y sldb models update InboxNoteDoc --store .sldb --pythonpath . desde la raiz del worktree. p5: suite con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_atoms_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_model_contract_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los cuatro tests nuevos pasan, deskops doctor --root . no suma errores por los atoms e inbox existentes (que no traen el campo), y sldb stores check --store .sldb no suma errores nuevos.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-30db2234603e`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-30db2234603e

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
