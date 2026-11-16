FILE:desk/tasks/task-runtime-template-el-coordinador-lanza-hijos-con-el-harness-auth-del-template-default-oauth-token-no.md
---
sldb:
  by: agent
  at: '2026-11-16T02:04:51Z'
  authority: generated
  via: save_document_payload
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

El auth de 'scion start' que arma deskops sale del template, nunca de un api-key fijo. (1) scion_start_argv(identity, *, prompt, project, workspace, template, harness_auth='oauth-token') en deskops/runtime/scion.py: harness_auth se valida contra la constante HARNESS_AUTH_TYPES del mismo módulo (api-key, oauth-token, auth-file, vertex-ai; ValueError si no está); su default es DEFAULT_HARNESS_AUTH = HARNESS_AUTH['claude'] = 'oauth-token', el mismo que pone 'deskops runtime template' en auth_selectedType de un template claude; harness_auth=None omite --harness-auth y deja decidir al template del hijo. (2) _render_coordinator_agents_md renderiza un solo archivo, el agents.md del coordinador, que contiene los dos ejemplos 'scion start' (executor y tester); recibe child_auth y escribe '--harness-auth <child_auth>' en ambos. Precedencia de child_auth, calculada en scion_template_files: el valor del flag --harness-auth de 'deskops runtime template' (parámetro harness_auth) si se pasó; si no, HARNESS_AUTH.get(harness) (el mismo valor que queda en auth_selectedType del template generado); si el harness no tiene default (no claude), DEFAULT_HARNESS_AUTH. No se lee ningún template persistido. RuntimeProfileDoc no tiene campo de auth: no se agrega en esta tarea.

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

Ningún texto ni argv generado por deskops contiene '--harness-auth api-key' salvo que se pida api-key explícitamente; scion_start_argv sin harness_auth da oauth-token y con harness_auth=None no lleva --harness-auth; el coordinador generado con --harness-auth auth-file escribe auth-file en sus dos scion start y sin el flag escribe oauth-token. Tests: se ajustan los dos tests existentes que afirmaban api-key (test_start_argv_carries_explicit_project_workspace_auth_and_labels, test_context_emits_environment_volume_and_concrete_examples) y se agrega uno nuevo; todos sin mocks (llaman funciones y el CLI real con archivos en tmp_path); tests/test_scion_runtime.py en verde.

FILE:instruccion
Cold-bundle de la tarea task-runtime-template-el-coordinador-lanza-hijos-con-el-harness-auth-del-template-default-oauth-token-no: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py
- grep -n 'harness-auth api-key' deskops/runtime/scion.py da vacío

