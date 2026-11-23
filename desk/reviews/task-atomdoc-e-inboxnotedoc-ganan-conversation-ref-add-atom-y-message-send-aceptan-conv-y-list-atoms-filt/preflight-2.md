---
sldb:
  by: agent
  at: '2026-11-23T05:10:19Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt-preflight-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt@sha256:2c0b281a30d094388d3260acaa3d952b13a71f1470824e12c036394c5e026d6c
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261123-050835/context-review/task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt/preflight/3783d6e6ee69c392e4aaab35f93153ae9134b3375eb11246b370f6232eb2e784/attempt-1
input_sha256: 3783d6e6ee69c392e4aaab35f93153ae9134b3375eb11246b370f6232eb2e784
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: a64d5f5139e94f6d13fa076da51fe6f2128bb106fbe41fdc01760cc4ef3f9238
output_sha256: 53d6f6e0cdf10badb8ac587f40dc6e4a7a579afa69f689c02f2eedb9688518d9
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones de la preflight-2 (la tarea ya trae files, scope e
  implementation_path corregidos):

  1) message send acepta los dos nombres, igual que add atom: A(("--conversation-ref",
  "--conv"), dest="conversation_ref", ...) en el Command ("message", "send") de deskops/cli/registry.py.
  Asi la ayuda es simetrica.

  2) sldb models update AtomDoc|InboxNoteDoc --store .sldb --pythonpath . actualiza
  el modelo registrado y re-extrae los documentos del modelo en el indice; no reescribe
  los .md. El campo va en la plantilla con marcador opcional (⸢optrev•conversation_ref⸥),
  asi que un atom o una nota viejos sin la linea leen conversation_ref = None y no
  cambian en disco.

  3) --update-golden existe: tests/conftest.py lo declara en pytest_addoption (linea
  37) y tests/test_output_goldens.py lo documenta en su docstring (linea 8). Comando:
  TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
  --update-golden.

  4) Vacio (None o solo espacios) no se escribe en add atom ni en message send. En
  list atoms, --conv vacio o solo espacios equivale a no filtrar (se trata como ausente).

  5) El duplicado es global: cualquier atom del desk (todo lo que devuelve list_artifacts("artifact.atom"),
  es decir todo desk/atoms) con conversation_ref igual tras strip, sea del hilo que
  sea.

  Commit desde el worktree que dispatch le da al ejecutor, con git commit -- <rutas>
  (las de files mas .sldb/core/models/AtomDoc.yaml, .sldb/core/models/InboxNoteDoc.yaml
  y el indice que toque sldb models update) y el trailer en el cuerpo:

  Task-Id: task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt


  Base comun: Hechos verificados (HEAD 40964f50): add atom genera sus flags de los
  campos del modelo en _add_subject_commands (deskops/cli/registry.py, linea 120;
  flag = "--" + nombre con guiones, CliFieldMeta.cli_option en deskops/cli/model_introspection.py
  linea 36) y no tiene --format (tests/fixtures/golden/help/deskops_add_atom.txt);
  list atoms: _list_subject_commands (registry.py linea 204) y OperationsCLI (deskops/cli/commands/operations.py
  linea 140) -> DeskopsOperations.list_atoms (deskops/operations.py linea 244) ->
  AtomsService.list_atoms (deskops/services/atoms.py linea 237); el texto de list
  lo da _format_artifact_list (operations.py linea 299): "<id> | <titulo>". message
  send: Command ("message", "send") en registry.py linea 651; _deliver_note en deskops/cli/commands/message.py
  linea 72. Las plantillas usan marcadores opcionales: provenance: ⸢optrev•provenance⸥
  en AtomDoc; sender_project: ⸢optrev•sender_project⸥ y ack_reason: ⸢optrev•ack_reason⸥
  en InboxNoteDoc. --update-golden existe: lo declara tests/conftest.py (pytest_addoption,
  linea 37). El contrato vive en tests/fixtures/model_contract_hashes.json (tests/test_model_contract_snapshot.py).'
# ISO 8601 timestamp
created_at: '2026-11-23T05:08:48.284572+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T05:10:11.743350+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261123-050835/context-review/task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt/preflight/3783d6e6ee69c392e4aaab35f93153ae9134b3375eb11246b370f6232eb2e784/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones de la preflight-2 (la tarea ya trae files, scope e implementation_path corregidos):
1) message send acepta los dos nombres, igual que add atom: A(("--conversation-ref", "--conv"), dest="conversation_ref", ...) en el Command ("message", "send") de deskops/cli/registry.py. Asi la ayuda es simetrica.
2) sldb models update AtomDoc|InboxNoteDoc --store .sldb --pythonpath . actualiza el modelo registrado y re-extrae los documentos del modelo en el indice; no reescribe los .md. El campo va en la plantilla con marcador opcional (⸢optrev•conversation_ref⸥), asi que un atom o una nota viejos sin la linea leen conversation_ref = None y no cambian en disco.
3) --update-golden existe: tests/conftest.py lo declara en pytest_addoption (linea 37) y tests/test_output_goldens.py lo documenta en su docstring (linea 8). Comando: TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py --update-golden.
4) Vacio (None o solo espacios) no se escribe en add atom ni en message send. En list atoms, --conv vacio o solo espacios equivale a no filtrar (se trata como ausente).
5) El duplicado es global: cualquier atom del desk (todo lo que devuelve list_artifacts("artifact.atom"), es decir todo desk/atoms) con conversation_ref igual tras strip, sea del hilo que sea.
Commit desde el worktree que dispatch le da al ejecutor, con git commit -- <rutas> (las de files mas .sldb/core/models/AtomDoc.yaml, .sldb/core/models/InboxNoteDoc.yaml y el indice que toque sldb models update) y el trailer en el cuerpo:
Task-Id: task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt

Base comun: Hechos verificados (HEAD 40964f50): add atom genera sus flags de los campos del modelo en _add_subject_commands (deskops/cli/registry.py, linea 120; flag = "--" + nombre con guiones, CliFieldMeta.cli_option en deskops/cli/model_introspection.py linea 36) y no tiene --format (tests/fixtures/golden/help/deskops_add_atom.txt); list atoms: _list_subject_commands (registry.py linea 204) y OperationsCLI (deskops/cli/commands/operations.py linea 140) -> DeskopsOperations.list_atoms (deskops/operations.py linea 244) -> AtomsService.list_atoms (deskops/services/atoms.py linea 237); el texto de list lo da _format_artifact_list (operations.py linea 299): "<id> | <titulo>". message send: Command ("message", "send") en registry.py linea 651; _deliver_note en deskops/cli/commands/message.py linea 72. Las plantillas usan marcadores opcionales: provenance: ⸢optrev•provenance⸥ en AtomDoc; sender_project: ⸢optrev•sender_project⸥ y ack_reason: ⸢optrev•ack_reason⸥ en InboxNoteDoc. --update-golden existe: lo declara tests/conftest.py (pytest_addoption, linea 37). El contrato vive en tests/fixtures/model_contract_hashes.json (tests/test_model_contract_snapshot.py).
