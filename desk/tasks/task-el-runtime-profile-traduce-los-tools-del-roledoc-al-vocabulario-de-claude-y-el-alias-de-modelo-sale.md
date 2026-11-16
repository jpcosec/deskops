---
sldb:
  by: agent
  at: '2026-11-16T06:03:30Z'
  authority: generated
  via: save_document_payload
id: task-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-el-alias-de-modelo-sale
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-002453-suggestion-piloto-scion-fase-1-brechas-del-coordinador-y-del-ejecutor-claude-en-contenedor.md
depends_on: []
pills: []
files:
- deskops/materializers/runtime_profiles.py
- deskops/runtime/scion.py
- tests/test_runtime_profiles.py
- tests/test_scion_runtime.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# El runtime profile traduce los tools del RoleDoc al vocabulario de claude y el alias de modelo sale del RoleDoc

## Rationale

_Explain why this task exists or the business driver behind it._

Nota del piloto scion fase 1 (2026-11-16), brechas 2 y 5. (2) Los tools del RoleDoc estan en vocabulario pi (read, grep, find, ls, bash) y pasan tal cual a --allowedTools de claude, donde no son nombres validos. (5) El template pone el alias de modelo 'medium' (en el harness claude es sonnet) aunque el RoleDoc pide opus.

## Goal

_Describe the concrete result this task must produce._

Cuando el RuntimeProfileDoc tiene kind claude, build_agent_spec_args (deskops/materializers/runtime_profiles.py) traduce los tools del RoleDoc: read->Read, grep->Grep, find->Glob, ls->Glob, bash->Bash, edit->Edit, write->Write, en el orden de primera aparicion y sin duplicados; un tool sin traduccion levanta ValueError("tool '<nombre>' has no translation for harness claude"). Para otros kind no cambia nada. El test existente test_build_agent_spec_args_repeat_joins_tools de tests/test_runtime_profiles.py codifica el comportamiento viejo y se actualiza para esperar [Read, Grep, Glob, Bash]. Alias de modelo: scion solo acepta MODEL_SIZE_ALIASES = small, medium, large, extra-large (deskops/runtime/scion.py:51). Si no se pasa un alias explicito, se deriva de RoleDoc.model: contiene 'opus' -> large, 'sonnet' -> medium, 'haiku' -> small (subcadena, sin distinguir mayusculas); sin coincidencia -> DEFAULT_MODEL_ALIAS (medium) y el scion-agent.yaml generado lleva el comentario '# model alias medium: no mapping for RoleDoc.model <valor>'. Un alias explicito siempre gana sobre el derivado.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/materializers/runtime_profiles.py (alrededor de las lineas 78-80), deskops/runtime/scion.py (DEFAULT_MODEL_ALIAS alrededor de 53-55 y el comentario de RoleDoc.model alrededor de 421-427), tests/test_runtime_profiles.py y tests/test_scion_runtime.py. No entra: cambiar los RoleDoc del desk, el harness pi, el repo scion.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Tabla TOOL_NAMES_BY_HARNESS en runtime_profiles.py y su aplicacion cuando el harness es claude. 2) Funcion model_alias_for(role_model) en scion.py con la tabla de arriba. 3) Tests: un RoleDoc con tools [read, grep, find, ls, bash] da --allowedTools Read,Grep,Glob,Bash para claude (sin duplicados); un tool desconocido falla con mensaje; RoleDoc con model anthropic/claude-opus-4-8 da alias opus; un modelo sin mapeo da el alias por defecto y el comentario.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_runtime_profiles.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_scion_runtime.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los casos del paso 3 pasan; para el harness pi los tests existentes siguen verdes sin cambios.
