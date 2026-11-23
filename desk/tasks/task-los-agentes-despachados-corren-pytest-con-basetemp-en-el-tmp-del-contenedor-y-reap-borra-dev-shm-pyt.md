---
sldb:
  by: agent
  at: '2026-11-23T04:39:09Z'
  authority: generated
  via: create_document
id: task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261123-024315-unclear-sin-dueno-nadie-limpia-dev-shm-pytest-of-scion.md
depends_on: []
pills: []
files:
- deskops/dispatch.py
- tests/test_dispatch.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Los agentes despachados corren pytest con basetemp en el /tmp del contenedor y reap borra /dev/shm/pytest-of-scion cuando no queda ningún agente vivo

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-024315 (handoff de scion-coordination, 2026-11-23, "SIN DUENO"): los ejecutores y testers despachados dejan /dev/shm/pytest-of-scion (5.9 GB el 2026-11-22) y lo borra a mano el coordinador de SLDB_1. Causa: las líneas de validación de las tareas llevan TMPDIR=/dev/shm y el /dev/shm del host está montado en el contenedor, así que el basetemp por defecto de pytest (pytest-of-<usuario>, usuario scion) cae en el host. El dueño es deskops porque dispatch arma el encargo (_role_instructions en deskops/dispatch.py) y reap borra a los agentes. La parte del host (pytest-of-robocop del integrate) va en la tarea hermana de integrate con --basetemp.

## Goal

_Describe the concrete result this task must produce._

(1) El prompt que escribe deskops dispatch start para executor y tester (deskops/dispatch.py, _role_instructions / _base_instructions) incluye una sección "Temporales de pytest" que pide exportar PYTEST_ADDOPTS="--basetemp=/tmp/pytest-<nombre del agente>" antes de cualquier pytest (el /tmp del contenedor muere con el agente), con el nombre real del agente. (2) deskops dispatch reap, después de borrar agentes, si _list_agents no muestra ningún agente con phase running en el proyecto, borra el directorio de temporales de pytest de scion (constante SCION_PYTEST_TMP = /dev/shm/pytest-of-scion, parcheable en tests) e imprime "limpieza: <ruta>"; si queda alguno vivo, no lo toca.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/dispatch.py y tests/test_dispatch.py. No entra: los RoleDoc, los templates de scion, las líneas de validación de las tareas existentes, el basetemp de integrate (tarea hermana).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_dispatch.py con scion falso: test_prompt_sets_pytest_basetemp_in_container_tmp (executor y tester; el prompt nombra --basetemp=/tmp/pytest-<agente>), test_reap_cleans_scion_pytest_tmp_when_no_agent_is_alive (la carpeta parcheada desaparece), test_reap_keeps_scion_pytest_tmp_while_an_agent_runs. p2: implementar. p3: suite con -n 4. p4: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_dispatch.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los tres tests nuevos pasan y los tests existentes de tests/test_dispatch.py siguen verdes.
