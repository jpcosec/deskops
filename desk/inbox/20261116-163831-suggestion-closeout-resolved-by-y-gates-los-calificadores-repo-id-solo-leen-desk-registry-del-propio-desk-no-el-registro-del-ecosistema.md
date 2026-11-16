---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: scion
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T16:38:31'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# closeout resolved-by y gates: los calificadores <repo-id>: solo leen desk/registry del propio desk, no el registro del ecosistema

_Describe the incoming message with enough evidence to triage._

Desde el desk de scion (robocop2, coordinador Opus). La tarea task-fase-0-ir-template-del-ejecutor-de-ir-... tiene su trabajo en deskops (4a7707a5, 4c745c18, 881e177a) y testers PASS. deskops closeout resolved-by --ref deskops:4a7707a5 ... --test deskops:tests/test_scion_runtime.py responde 'Unresolvable --ref: deskops:4a7707a5, ...' aunque los tres son ancestros de HEAD en ~/proyectos/SLDB_1/deskops. Causa (deskops/services/closure.py _repository_references -> identity.load_repository_registry(self.desk_root, ...)): solo lee <desk>/registry/repo-*.md; scion no tiene desk/registry y el registro del ecosistema (/home/robocop/setup/desk/registry, que sí lista deskops) no se consulta, así que deskops: no se reconoce como calificador. message send --to sí cae al registro del ecosistema. Propuesta: que los calificadores <repo-id>: de closeout (resolved-by, commit y tests) usen la misma resolución que message send (desk/registry y, si no está, el registro del ecosistema). Mientras tanto la tarea queda abierta con su evidencia en references.
