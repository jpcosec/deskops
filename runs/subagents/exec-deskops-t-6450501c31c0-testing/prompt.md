Task: task-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-puede-redirigir-por-entorno-y-los-tests-del-cli-n
Title: La limpieza de pytest-of-scion en dispatch reap se puede redirigir por entorno y los tests del CLI no tocan el /dev/shm real
Status: active
Current node: ritual-testing
Task type: task.debug
Effective atoms:
- atom-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-redirige-por-entorno-y-los-tests-del-cli-no-tocan
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-23T15:11:49Z'
  authority: generated
  via: save_document_payload
id: task-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-puede-redirigir-por-entorno-y-los-tests-del-cli-n
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- deskops/dispatch.py
- tests/test_dispatch.py
- f7772acdee9f620051ad4551b48fc24c294173cd
depends_on: []
pills: []
files:
- deskops/dispatch.py
- tests/test_dispatch.py
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-redirige-por-entorno-y-los-tests-del-cli-no-tocan
---

# La limpieza de pytest-of-scion en dispatch reap se puede redirigir por entorno y los tests del CLI no tocan el /dev/shm real

## Rationale

_Explain why this task exists or the business driver behind it._

El integrate 20261123T114518Z fallo en tests/test_dispatch.py::test_reap_scion_error_continues_and_fails: el reap del CLI en subproceso imprimio 'limpieza: /dev/shm/pytest-of-scion' porque SCION_PYTEST_TMP es una constante que el subproceso no ve parcheada; ademas borra el directorio real del host durante la suite. Viene de 0a40890c (task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt).

## Goal

_Describe the concrete result this task must produce._

dispatch reap toma la ruta de limpieza de la variable de entorno DESKOPS_SCION_PYTEST_TMP si esta definida (por defecto /dev/shm/pytest-of-scion), y el fixture Env de tests/test_dispatch.py la apunta a un directorio dentro de tmp_path, asi ningun test toca el /dev/shm real y la salida no depende del host.

## Scope

_State what is in scope and what is out of scope._

deskops/dispatch.py y tests/test_dispatch.py.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. En dispatch.py resolver la ruta con os.environ.get('DESKOPS_SCION_PYTEST_TMP', SCION_PYTEST_TMP) al limpiar. 2. En el fixture Env de tests/test_dispatch.py fijar DESKOPS_SCION_PYTEST_TMP a tmp_path/'pytest-of-scion'. 3. Ajustar los tests de limpieza para usar esa ruta. 4. Test: con un /dev/shm/pytest-of-scion real presente, test_reap_scion_error_continues_and_fails no imprime limpieza.

## Validation

_List the checks required before this task can close._

- mkdir -p /dev/shm/pytest-of-scion && pytest -q tests/test_dispatch.py && test -d /dev/shm/pytest-of-scion

## Done When

_Name the observable condition that makes the task complete._

pytest -q tests/test_dispatch.py pasa con un directorio /dev/shm/pytest-of-scion presente en el host y ese directorio sigue existiendo despues.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-la-limpieza-de-pytest-of-scion-en-dispatch-reap-se-puede-redirigir-por-entorno-y-los-tests-del-cli-n"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.
