---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-23T03:45:22'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# dispatch no se puede partir entre config.json y config.local.json: el proyecto y los roles no quedan versionados

_Describe the incoming message with enough evidence to triage._

Sale de la segunda consulta al concilio (acta en heyantonia/Governance, docs/diagnostico-vsm-2026-11-19/concilio/acta-2026-11-23-despacho-y-namespaces.md; pi y codex lo pidieron por separado). Hoy DeskConfig.load fusiona desk/config.json con desk/config.local.json y valida el resultado, y DispatchConfig exige juntos project, workspace, templates_dir, context_file y roles (deskops/config.py:61-66 y 106-116 en a7694665). Efecto: un bloque dispatch parcial en el archivo versionado hace fallar la carga de la configuración en toda máquina que no tenga el archivo local, así que para un desk de heyantonia dispatch tiene que ir entero en config.local.json y en el repo no queda escrito con qué proyecto de scion ni con qué roles se despacha ese desk. Pedido: poder versionar la parte portable (project, roles de executor y tester con su harness y model_alias, roles_root, quick_gates) y dejar en el archivo local solo lo de la máquina (workspace, templates_dir, context_file, harness_auth, env_config); que cualquier clon pueda cargar la configuración, y que solo 'dispatch start' exija las rutas locales resueltas. Calza con la tarea hermana de rutas y credenciales de máquina que ya está en este desk; puede ser parte de ella. Mientras no exista, Governance configura el piloto (shared_llm-gateway) con dispatch entero en config.local.json de robocop 2.
