FILE:desk/tasks/task-deskops-review-puede-correr-con-un-runtimeprofiledoc-de-claude-cuando-pi-no-esta-disponible.md
---
sldb:
  by: agent
  at: '2026-11-16T05:00:47Z'
  authority: generated
  via: save_document_payload
id: task-deskops-review-puede-correr-con-un-runtimeprofiledoc-de-claude-cuando-pi-no-esta-disponible
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-002453-suggestion-piloto-scion-fase-1-brechas-del-coordinador-y-del-ejecutor-claude-en-contenedor.md
depends_on: []
pills:
- desk/contexts/pill-zero-context-preflight-precedes-executor.md
files:
- deskops/services/review.py
- tests/test_review_command.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
- atom-cheap-zero-context-reviews-test-the-brief-recursively
---

# deskops review puede correr con un RuntimeProfileDoc de claude cuando pi no esta disponible

## Rationale

_Explain why this task exists or the business driver behind it._

Nota del piloto scion fase 1 (2026-11-16), brecha 1: la imagen scion-claude no trae pi, asi que el coordinador dentro del contenedor no puede correr `deskops review preflight/bundle` (engine por defecto runtime-pi-deepseek-flash); hoy los corre el supervisor en el host. deskops/services/review.py arma el argv solo para pi (`binary or 'pi'` y el input como `@<ruta>`).

## Goal

_Describe the concrete result this task must produce._

`deskops review preflight|bundle|node --engine <perfil>` funciona con un RuntimeProfileDoc cuyo binario es claude: el argv usa el modo no interactivo de claude (-p), el modelo del perfil, el system prompt del revisor, sin tools, sin sesion persistida y sin cargar contexto, skills ni MCP del usuario, y el input se entrega por stdin o por archivo segun lo que acepte claude. El manifest registra binario, modelo y flags de aislamiento igual que con pi. El default sigue siendo runtime-pi-deepseek-flash.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/review.py (armado del argv, alrededor de las lineas 166-186), el RuntimeProfileDoc runtime-claude del desk de deskops si hay que ajustar sus campos (con `deskops edit runtime-profile`), tests/test_review_command.py. Se fijan los flags exactos leyendo `claude --help` en robocop2. No entra: instalar pi en la imagen (lo pide la nota al repo scion), cambiar el ritual context-review, elegir el modelo por defecto. Precisiones del preflight 1: claude esta instalado en robocop2 y el ejecutor corre ahi (claude --help para los flags). El input va por stdin (no @ruta). Si runtime-claude no existe o le falta binary/model, se completa con deskops edit runtime-profile (binary claude, model haiku) y si no existe se crea con deskops add runtime-profile. Desk sandbox = un directorio en /dev/shm con git init y deskops init, borrado al terminar. La evidencia de la corrida manual es el run_dir que imprime el comando (manifest.json, output.md) citado en el informe; se acepta si output.md trae las secciones REFORMULACION, AMBIGUEDADES y DRY-RUN. tests/test_review_doc.py solo se corre, no se modifica.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer review.py:150-200 y el modelo RuntimeProfileDoc. 2) Rama por binario: pi (actual) y claude (argv nuevo). 3) Test unitario del argv para un perfil claude (sin llamar al modelo): contiene -p, --model <m>, el system prompt, la desactivacion de tools y no contiene @<ruta>. 4) Prueba manual una vez en robocop2: `deskops review preflight <tarea de prueba> --engine runtime-claude --root .` en un desk sandbox, guardando la salida del run como evidencia.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El test del argv claude pasa; la corrida manual del paso 4 deja un recibo con engine runtime-claude y output con las secciones del revisor.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-review-puede-correr-con-un-runtimeprofiledoc-de-claude-cuando-pi-no-esta-disponible: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

