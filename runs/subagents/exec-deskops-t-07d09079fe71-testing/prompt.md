Task: task-closeout-verify-cubre-los-archivos-bajo-un-directorio-target-que-ahora-es-nodo-del-grafo-de-sldb
Title: closeout verify cubre los archivos bajo un directorio target que ahora es nodo del grafo de sldb
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-19T14:40:13Z'
  authority: generated
  via: save_document_payload
id: task-closeout-verify-cubre-los-archivos-bajo-un-directorio-target-que-ahora-es-nodo-del-grafo-de-sldb
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# closeout verify cubre los archivos bajo un directorio target que ahora es nodo del grafo de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Regresión, 2026-11-19. Desde sldb 6f14a3b5, un directorio existente declarado como target de una materialization es un nodo (FileNode, file_kind directory). La materialization deja de ser inválida, y _directory_materialization_targets de deskops/services/closure.py solo mira las inválidas. Resultado: los archivos bajo el directorio ya no reciben link y verify da missing_changed_file_link. Rompe tests/test_materialization_targets_outside_package.py::test_closeout_verify_covers_files_under_a_directory_target (los dos casos): con deskops 7e8492ea pasan con sldb 6f14a3b5^ y fallan con 6f14a3b5. La suite de main está roja y bloquea integrate.

## Goal

_Describe the concrete result this task must produce._

Una materialization cuyo target_identity es un directorio cubre los archivos bajo él (target_covers) tanto si sldb reporta el directorio como missing (sldb viejo) como si es un nodo del grafo (sldb nuevo). Un hermano con prefijo parecido (pkg/subzero.py) sigue sin cubrirse.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/services/closure.py (_changed_file_link_evidence y _directory_materialization_targets o un helper nuevo) y su test en tests/test_materialization_targets_outside_package.py si hace falta ampliarlo. Fuera: sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: correr los dos casos del test con el sldb del venv (el de herramientas, que ya trae 6f14a3b5) y ver el fallo. p2: en closure.py, para cada materialization válida cuyo arista apunta a un nodo de archivo con file_kind directory (o cuyo target_identity declarado es un directorio existente), usar target_covers igual que con las inválidas. p3: los dos casos pasan; agregar un test que lo cubra con el nodo de directorio presente si el actual no lo distingue. p4: CHANGELOG, commit con rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_materialization_targets_outside_package.py

## Done When

_Name the observable condition that makes the task complete._

Los dos casos de test_closeout_verify_covers_files_under_a_directory_target pasan con el sldb actual.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-closeout-verify-cubre-los-archivos-bajo-un-directorio-target-que-ahora-es-nodo-del-grafo-de-sldb"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.
