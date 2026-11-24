---
sldb:
  by: agent
  at: '2026-11-24T17:35:36Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDocsDoc:task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use@sha256:1defaf6a2f2ddea2a977e0473ad1065730d76bb9dd4206e6340bd076cbe30471
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261117-120232/context-review/task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use/preflight/193b3b70799bb1f0b6454d3edff95da5adfa4059cdb6e8d08dc3588e4c5983e1/attempt-1
input_sha256: 193b3b70799bb1f0b6454d3edff95da5adfa4059cdb6e8d08dc3588e4c5983e1
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: a35936161c61ddc7d8db0e2974de81f83fd4471397564010ed17163a912dbd23
output_sha256: 464103d84b20a60da6f24423c066539d32259ab6903cfb59b6476dd97864e70a
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Precisiones del coordinador (preflight 1 y bundle 1): (1) Se editan solo
  archivos de deskops (AGENTS.md, README.md y .opencode/ de este repo); el repo IR
  no se toca. (2) Redaccion: ''use-specir (skill del repo IR, skills/use-specir/SKILL.md)''.
  (3) El criterio es el grep del token use-spec2viz: no debe quedar en AGENTS.md,
  README.md ni .opencode; menciones historicas de spec2viz sin ese token (la seccion
  ''Spec2viz Boundary'' del README, nombres de atomos) se quedan. (4) El titulo del
  SKILL.md movido puede cambiar para no usar el token (por ejemplo ''use-specir (antes
  la skill de spec2viz de opencode)''); el resto de su contenido no cambia. (5) La
  linea del README que describe references/spec2viz-cli.md pasa a describirla como
  remision a use-specir. (6) Si el grep encuentra el token en otras skills de .opencode,
  se cambian tambien (entran en alcance) y se dice. (7) El ejecutor no commitea: commit
  y cierre los hace el coordinador.'
# ISO 8601 timestamp
created_at: '2026-11-17T12:02:51.413565+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T12:10:02.896667+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261117-120232/context-review/task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use/preflight/193b3b70799bb1f0b6454d3edff95da5adfa4059cdb6e8d08dc3588e4c5983e1/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Precisiones del coordinador (preflight 1 y bundle 1): (1) Se editan solo archivos de deskops (AGENTS.md, README.md y .opencode/ de este repo); el repo IR no se toca. (2) Redaccion: 'use-specir (skill del repo IR, skills/use-specir/SKILL.md)'. (3) El criterio es el grep del token use-spec2viz: no debe quedar en AGENTS.md, README.md ni .opencode; menciones historicas de spec2viz sin ese token (la seccion 'Spec2viz Boundary' del README, nombres de atomos) se quedan. (4) El titulo del SKILL.md movido puede cambiar para no usar el token (por ejemplo 'use-specir (antes la skill de spec2viz de opencode)'); el resto de su contenido no cambia. (5) La linea del README que describe references/spec2viz-cli.md pasa a describirla como remision a use-specir. (6) Si el grep encuentra el token en otras skills de .opencode, se cambian tambien (entran en alcance) y se dice. (7) El ejecutor no commitea: commit y cierre los hace el coordinador.
