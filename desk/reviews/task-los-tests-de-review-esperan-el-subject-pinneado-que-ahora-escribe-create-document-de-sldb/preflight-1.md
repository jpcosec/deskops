---
sldb:
  by: agent
  at: '2026-11-24T18:16:28Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb@sha256:776ea5911a33d5951e9bcdc897af2d3a350785b9fd17847e88a60d3ed4f4b90e
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261116-213327/context-review/task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb/preflight/4a8b55cdee6acfd827b5457c64e5a8f90c3be71e77e4bdc88bda988679426f6e/attempt-1
input_sha256: 4a8b55cdee6acfd827b5457c64e5a8f90c3be71e77e4bdc88bda988679426f6e
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: 0f89183899d737fb138b0418f260b7c33f96a236050c2c09da6e598f548a12ab
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Precisiones del coordinador (preflight 1): (1) La aserccion modelo es la
  que hoy hace re.fullmatch(r"doc:TaskCodeDoc:task-x@sha256:[0-9a-f]{64}", doc["subject"])
  dentro de test_subject_is_pinned_and_the_anchor_is_intact (linea 266 en origin/main
  ee9bc3cd). (2) En test_a_short_selector_keys_and_anchors_receipts_on_the_full_task_id
  el id del ancla es el id COMPLETO de la tarea (la variable full del test), nunca
  el selector corto: el test existe justo para eso. (3) El alcance son exactamente
  las aserciones de igualdad sobre subject que hoy fallan (lineas 261, 363 y 371 de
  test_review_record.py y 165 de test_review_command.py en ee9bc3cd); un subject de
  otro modelo o id no se toca. (4) Redaccion libre del ejecutor, una o dos frases:
  sldb pinnea __doc_anchors__ al crear (create_document, desde sldb 477d1bc0) y al
  guardar; solo ese docstring.'
# ISO 8601 timestamp
created_at: '2026-11-16T21:33:40.589241+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T21:34:04.826632+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261116-213327/context-review/task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb/preflight/4a8b55cdee6acfd827b5457c64e5a8f90c3be71e77e4bdc88bda988679426f6e/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Precisiones del coordinador (preflight 1): (1) La aserccion modelo es la que hoy hace re.fullmatch(r"doc:TaskCodeDoc:task-x@sha256:[0-9a-f]{64}", doc["subject"]) dentro de test_subject_is_pinned_and_the_anchor_is_intact (linea 266 en origin/main ee9bc3cd). (2) En test_a_short_selector_keys_and_anchors_receipts_on_the_full_task_id el id del ancla es el id COMPLETO de la tarea (la variable full del test), nunca el selector corto: el test existe justo para eso. (3) El alcance son exactamente las aserciones de igualdad sobre subject que hoy fallan (lineas 261, 363 y 371 de test_review_record.py y 165 de test_review_command.py en ee9bc3cd); un subject de otro modelo o id no se toca. (4) Redaccion libre del ejecutor, una o dos frases: sldb pinnea __doc_anchors__ al crear (create_document, desde sldb 477d1bc0) y al guardar; solo ese docstring.
