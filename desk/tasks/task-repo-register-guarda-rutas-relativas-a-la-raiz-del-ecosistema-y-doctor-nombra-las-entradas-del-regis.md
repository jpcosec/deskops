---
sldb:
  by: agent
  at: '2026-11-16T06:16:31Z'
  authority: generated
  via: save_document_payload
id: task-repo-register-guarda-rutas-relativas-a-la-raiz-del-ecosistema-y-doctor-nombra-las-entradas-del-regis
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-012947-suggestion-registro-del-ecosistema-con-rutas-de-otra-m-quina-lo-de-sldb-est-resuelto-a2bfdf91-queda-doctor-en-deskops.md
depends_on: []
pills: []
files:
- deskops/cli/commands/repo.py
- deskops/doc_access.py
- deskops/cli/commands/doctor.py
- tests/test_repo_identity.py
- tests/test_registry_robustness.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# repo register guarda rutas relativas a la raiz del ecosistema y doctor nombra las entradas del registro que no resuelven

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de sldb del 2026-11-16 (de una nota de mepu): el registro del ecosistema guarda rutas absolutas de la maquina que registra (desde robocop2 queda /mnt/ssd/..., que se rompe en la laptop; en ~/setup/desk/registry varias entradas apuntan a /home/jp/... que no existe en robocop2). sldb ya lo corrigio en su propio registro (a2bfdf91: path ., ../deskops, ../UIs/graph_ui). En deskops quedan dos cosas: deskops repo register (deskops/cli/commands/repo.py, metodo register alrededor de la linea 32) guarda la ruta absoluta, y deskops doctor solo dice 'the linked store is missing' cuando una entrada del registro no resuelve.

## Goal

_Describe the concrete result this task must produce._

(1) `deskops repo register` guarda en path la ruta relativa a la raiz del repo que contiene el registro donde escribe (desk/registry del desk, o ~/setup/desk/registry para el del ecosistema, con ~ expandido solo al resolver), y acepta leer entradas viejas con ruta absoluta o con ~. (2) `deskops doctor` reporta, por cada entrada del registro del desk cuyo path no resuelve en esta maquina, un hallazgo con el id del repo, el path guardado y la ruta resuelta, ademas del mensaje actual del store enlazado.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/commands/repo.py, deskops/doc_access.py (registered_repositories, alrededor de la linea 934) o el modulo que resuelva rutas del registro, deskops/cli/commands/doctor.py y tests (tests/test_repo_identity.py, tests/test_registry_robustness.py). No entra: reescribir entradas existentes de ~/setup (lo hace su dueño con el CLI nuevo), cambiar el formato de RepositoryDoc. Precisiones del preflight 1: la ruta se calcula con os.path.relpath(destino, raiz del repo que contiene el directorio del registro): para desk/registry, la raiz del repo del desk; para ~/setup/desk/registry, ~/setup. La expansion de ~ y la resolucion de rutas relativas la hace la funcion que ya resuelve el registro (resolve_registered_root en deskops/identity.py), para todo lector. doctor cubre solo el registro del desk (desk/registry). El hallazgo es una alerta (no cambia el rc de doctor) con: id del repo, path guardado y ruta absoluta intentada. tests/test_message_ecosystem_registry.py solo se corre.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer repo.py, registered_repositories y deskops/identity.py (resolve_registered_root). 2) register calcula os.path.relpath(destino, raiz_del_registro). 3) doctor recorre registered_repositories y agrega el hallazgo. 4) Tests: register desde un sandbox guarda ruta relativa; una entrada con ruta absoluta inexistente da el hallazgo en doctor; una entrada vieja absoluta valida sigue resolviendo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_repo_identity.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_registry_robustness.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_ecosystem_registry.py (solo se corre)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas = cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los tres casos del paso 4 pasan y los tests de registro existentes siguen verdes.
