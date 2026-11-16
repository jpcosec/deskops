---
sldb:
  by: agent
  at: '2026-11-16T02:06:53Z'
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

deskops/runtime/scion.py (scion_start_argv, scion_template_files, _render_coordinator_agents_md; HARNESS_AUTH = {'claude': 'oauth-token'} y HARNESS_AUTH_TYPES ya existen en ese módulo, se agrega DEFAULT_HARNESS_AUTH = HARNESS_AUTH['claude']), tests/test_scion_runtime.py y el cuerpo del RoleDoc desk/roles/deskops-supervisor.md (su línea 'Use explicit Scion dispatch flags' dice '--harness-auth api-key'; se cambia con deskops edit role a '--harness-auth <el auth del template; oauth-token por defecto>'). Sin cambios en el modelo RuntimeProfileDoc, en el CLI (--harness-auth ya existe) ni en los agents.md de executor y tester.

## Implementation Path

_Outline the expected implementation route or affected surface._

deskops/runtime/scion.py

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py
- grep -n 'harness-auth api-key' deskops/runtime/scion.py da vacío

## Done When

_Name the observable condition that makes the task complete._

En el código, ningún argv ni texto generado contiene '--harness-auth api-key' (el literal no aparece en scion.py; api-key solo sale si el llamador pasa harness_auth='api-key'). scion_start_argv sin harness_auth da '--harness-auth oauth-token'; con harness_auth=None no lleva --harness-auth; con un valor fuera de HARNESS_AUTH_TYPES lanza ValueError. El child_auth del coordinador nunca es None: es harness_auth, si no HARNESS_AUTH.get(harness), si no DEFAULT_HARNESS_AUTH. El coordinador generado con --harness-auth auth-file escribe auth-file en sus dos scion start y sin el flag escribe oauth-token. Tests: se ajustan los dos que afirmaban api-key (test_start_argv_carries_explicit_project_workspace_auth_and_labels, test_context_emits_environment_volume_and_concrete_examples) y se agrega test_start_auth_follows_the_template_never_a_fixed_api_key, que cubre: argv con auth-file, argv con None sin flag, argv con 'password' -> ValueError, agents.md del coordinador con None y con auth-file (2 apariciones cada uno, sin api-key) y el CLI real 'deskops runtime template role-deskops-supervisor --mode coordinator --harness-auth auth-file --out <tmp>'. Todos sin mocks; tests/test_scion_runtime.py en verde. El cuerpo de desk/roles/deskops-supervisor.md ya no dice '--harness-auth api-key'.
