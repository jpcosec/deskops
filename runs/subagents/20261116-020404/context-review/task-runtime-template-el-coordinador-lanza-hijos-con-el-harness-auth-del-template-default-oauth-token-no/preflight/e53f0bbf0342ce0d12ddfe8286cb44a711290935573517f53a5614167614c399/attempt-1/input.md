FILE:desk/tasks/task-runtime-template-el-coordinador-lanza-hijos-con-el-harness-auth-del-template-default-oauth-token-no.md
---
sldb:
  by: agent
  at: '2026-11-16T02:03:49Z'
  authority: generated
  via: create_document
id: task-runtime-template-el-coordinador-lanza-hijos-con-el-harness-auth-del-template-default-oauth-token-no
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-runtime-template-el-coordinador-lanza-hijos-con-harness-auth-api-key-fijo.md
---

# runtime template: el coordinador lanza hijos con el harness-auth del template (default oauth-token), no api-key fijo

## Rationale

_Explain why this task exists or the business driver behind it._

Piloto scion en IR (reports/scion-piloto-ir-20261115.md): scion_start_argv y el agents.md del coordinador escriben 'scion start ... --harness-auth api-key' fijo. Un hijo claude con suscripción (CLAUDE_CODE_OAUTH_TOKEN = oauth-token, o CLAUDE_AUTH = auth-file) no arranca así: pide ANTHROPIC_API_KEY. Bloquea la fase 1 del piloto.

## Goal

_Describe the concrete result this task must produce._

El auth de 'scion start' que arma deskops sale del template: scion_start_argv recibe harness_auth (validado contra HARNESS_AUTH_TYPES) y, sin valor, usa oauth-token, el mismo default que 'deskops runtime template' para claude (HARNESS_AUTH). El agents.md del coordinador escribe en los dos 'scion start' (executor y tester) el auth resuelto del template del coordinador (--harness-auth si se pasó; si no, el default del harness, oauth-token). RuntimeProfileDoc no tiene campo de auth: no se agrega en esta tarea.

## Scope

_State what is in scope and what is out of scope._

deskops/runtime/scion.py (scion_start_argv, scion_template_files, _render_coordinator_agents_md) y tests/test_scion_runtime.py. Sin cambios en el modelo RuntimeProfileDoc, en el CLI (--harness-auth ya existe) ni en los otros agents.md.

## Implementation Path

_Outline the expected implementation route or affected surface._

deskops/runtime/scion.py

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py
- grep -n 'harness-auth api-key' deskops/runtime/scion.py da vacío

## Done When

_Name the observable condition that makes the task complete._

Ningún texto ni argv generado por deskops contiene '--harness-auth api-key' salvo que se pida api-key explícitamente; scion_start_argv sin harness_auth da oauth-token; el coordinador generado con --harness-auth auth-file escribe auth-file en sus dos scion start; tests reales sin mocks en tests/test_scion_runtime.py en verde.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-runtime-template-el-coordinador-lanza-hijos-con-el-harness-auth-del-template-default-oauth-token-no: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

