---
sldb:
  by: agent
  at: '2026-11-23T19:15:53Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-deskops-trae-un-roledoc-desk-identity-instalable-en-cualquier-desk-y-runtime-template-lo-materializa-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-deskops-trae-un-roledoc-desk-identity-instalable-en-cualquier-desk-y-runtime-template-lo-materializa@sha256:21f9ddc80ef72c6339bd16207588899b123ebfb98edaf45831c7bef54e964ed1
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261123-045152/context-review/task-deskops-trae-un-roledoc-desk-identity-instalable-en-cualquier-desk-y-runtime-template-lo-materializa/preflight/a3cfac5a505d63db59523d2067766c699f0ff626fd37f0bd9f0ca22d59127ebf/attempt-1
input_sha256: a3cfac5a505d63db59523d2067766c699f0ff626fd37f0bd9f0ca22d59127ebf
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 360d434205ed329af50ee52298923f933928f31cdfdcc572e1fbe7aa27f4704e
output_sha256: f9631ee5bb659fc4edc16954bfaf379246fd9df5f32d2ea7c1ff0b5e91b8c07b
# pending | accepted | rejected | incomplete
verdict: rejected
reason: 'Rechazada: la tarea no fijaba donde vive el RoleDoc (dentro de deskops/data/templates
  lo sembraria seed_desk como semilla gestionada), ni el texto del cuerpo (el texto
  base de Governance esta en /srv/wt/..., fuera de los montajes del ejecutor), ni
  que deskops init tambien debe instalarlo (si no, todo desk recien creado dejaria
  de estar ''up to date'' y fallan los tests de scaffold), ni los goldens de scaffold
  y ayuda, ni el mensaje nuevo de --mode, ni la precondicion del Done When. Se corrigieron
  scope, implementation_path, files y done_when con hechos verificados (add role escribe
  desk/roles/role-<name>.md con id role-<name>; --mode es choices en deskops/cli/registry.py
  y ValueError en deskops/runtime/scion.py linea 384). Se repite la review.'
# ISO 8601 timestamp
created_at: '2026-11-23T04:52:07.355069+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-23T05:15:58.706512+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-deskops-trae-un-roledoc-desk-identity-instalable-en-cualquier-desk-y-runtime-template-lo-materializa

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261123-045152/context-review/task-deskops-trae-un-roledoc-desk-identity-instalable-en-cualquier-desk-y-runtime-template-lo-materializa/preflight/a3cfac5a505d63db59523d2067766c699f0ff626fd37f0bd9f0ca22d59127ebf/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict rejected: Rechazada: la tarea no fijaba donde vive el RoleDoc (dentro de deskops/data/templates lo sembraria seed_desk como semilla gestionada), ni el texto del cuerpo (el texto base de Governance esta en /srv/wt/..., fuera de los montajes del ejecutor), ni que deskops init tambien debe instalarlo (si no, todo desk recien creado dejaria de estar 'up to date' y fallan los tests de scaffold), ni los goldens de scaffold y ayuda, ni el mensaje nuevo de --mode, ni la precondicion del Done When. Se corrigieron scope, implementation_path, files y done_when con hechos verificados (add role escribe desk/roles/role-<name>.md con id role-<name>; --mode es choices en deskops/cli/registry.py y ValueError en deskops/runtime/scion.py linea 384). Se repite la review.
