---
sldb:
  by: agent
  at: '2026-11-23T05:10:34Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt-bundle-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
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
run_dir: runs/subagents/20261123-050904/context-review/task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt/bundle/c74788c95cdba4463e3292e3c98b975a4d9bdbd1dfce3fc6408049ba72ea3a59/attempt-1
input_sha256: c74788c95cdba4463e3292e3c98b975a4d9bdbd1dfce3fc6408049ba72ea3a59
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: cdf0bcb12ef0a61c89559acdfde698cc37c6fe6c3594c437ef35a84961db520f
output_sha256: dfdd1c282e87c717c28e6851c181fbc287139efd6555a35fbefddbf49614c5d8
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del bundle-2:

  1) Sin validacion de forma: conversation_ref es str | None sin pattern (la forma
  "<hilo>/<id>" es convencion, no contrato); solo se hace strip y vacio = no se escribe.
  Asi el hash de contrato cambia solo por el campo nuevo.

  2) Plantillas: si, las dos ganan una linea opcional junto a las otras opcionales,
  con el marcador conversation_ref: ⸢optrev•conversation_ref⸥ (AtomDoc despues de
  provenance: ⸢optrev•provenance⸥; InboxNoteDoc despues de ack_reason: ⸢optrev•ack_reason⸥),
  mismo patron que los campos opcionales existentes.

  3) El texto de list atoms no cambia (_format_artifact_list, "<id> | <titulo>");
  solo --format json/yaml lo incluye, porque el payload sale del modelo.

  4) En el mensaje de duplicado <ref> es el valor normalizado (tras strip), que es
  el que se compara y el que esta guardado: "ya existe <atom id> con conversation_ref
  <ref>".

  5) /mnt/ssd/proyectos/wf-desks/bin/desk-prompt.sh solo se cita en el Rationale como
  ejemplo del uso actual; no se toca (otro repo, fuera de files y scope).

  Commit desde el worktree que dispatch le da al ejecutor, con git commit -- <rutas>
  y el trailer en el cuerpo:

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
created_at: '2026-11-23T05:09:24.134563+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T05:10:27.250503+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Bundle review of task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261123-050904/context-review/task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt/bundle/c74788c95cdba4463e3292e3c98b975a4d9bdbd1dfce3fc6408049ba72ea3a59/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del bundle-2:
1) Sin validacion de forma: conversation_ref es str | None sin pattern (la forma "<hilo>/<id>" es convencion, no contrato); solo se hace strip y vacio = no se escribe. Asi el hash de contrato cambia solo por el campo nuevo.
2) Plantillas: si, las dos ganan una linea opcional junto a las otras opcionales, con el marcador conversation_ref: ⸢optrev•conversation_ref⸥ (AtomDoc despues de provenance: ⸢optrev•provenance⸥; InboxNoteDoc despues de ack_reason: ⸢optrev•ack_reason⸥), mismo patron que los campos opcionales existentes.
3) El texto de list atoms no cambia (_format_artifact_list, "<id> | <titulo>"); solo --format json/yaml lo incluye, porque el payload sale del modelo.
4) En el mensaje de duplicado <ref> es el valor normalizado (tras strip), que es el que se compara y el que esta guardado: "ya existe <atom id> con conversation_ref <ref>".
5) /mnt/ssd/proyectos/wf-desks/bin/desk-prompt.sh solo se cita en el Rationale como ejemplo del uso actual; no se toca (otro repo, fuera de files y scope).
Commit desde el worktree que dispatch le da al ejecutor, con git commit -- <rutas> y el trailer en el cuerpo:
Task-Id: task-atomdoc-e-inboxnotedoc-ganan-conversation-ref-add-atom-y-message-send-aceptan-conv-y-list-atoms-filt

Base comun: Hechos verificados (HEAD 40964f50): add atom genera sus flags de los campos del modelo en _add_subject_commands (deskops/cli/registry.py, linea 120; flag = "--" + nombre con guiones, CliFieldMeta.cli_option en deskops/cli/model_introspection.py linea 36) y no tiene --format (tests/fixtures/golden/help/deskops_add_atom.txt); list atoms: _list_subject_commands (registry.py linea 204) y OperationsCLI (deskops/cli/commands/operations.py linea 140) -> DeskopsOperations.list_atoms (deskops/operations.py linea 244) -> AtomsService.list_atoms (deskops/services/atoms.py linea 237); el texto de list lo da _format_artifact_list (operations.py linea 299): "<id> | <titulo>". message send: Command ("message", "send") en registry.py linea 651; _deliver_note en deskops/cli/commands/message.py linea 72. Las plantillas usan marcadores opcionales: provenance: ⸢optrev•provenance⸥ en AtomDoc; sender_project: ⸢optrev•sender_project⸥ y ack_reason: ⸢optrev•ack_reason⸥ en InboxNoteDoc. --update-golden existe: lo declara tests/conftest.py (pytest_addoption, linea 37). El contrato vive en tests/fixtures/model_contract_hashes.json (tests/test_model_contract_snapshot.py).
