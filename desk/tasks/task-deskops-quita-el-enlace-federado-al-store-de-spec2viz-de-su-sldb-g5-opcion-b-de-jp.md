---
sldb:
  by: agent
  at: '2026-11-16T16:00:14Z'
  authority: generated
  via: create_document
id: task-deskops-quita-el-enlace-federado-al-store-de-spec2viz-de-su-sldb-g5-opcion-b-de-jp
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-122447-suggestion-deskops-sldb-enlaza-spec2viz-las-pruebas-mcp-de-ir-leen-el-store-real-de-spec2viz-de-forma-transitiva-g5.md
depends_on: []
pills: []
files:
- .sldb/store.yaml
- .sldb/core/store_index.yaml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
---

# deskops quita el enlace federado al store de spec2viz de su .sldb (G5, opcion b de JP)

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de IR del 2026-11-16 (desk/inbox/20261116-122447-suggestion-deskops-sldb-enlaza-spec2viz-las-pruebas-mcp-de-ir-leen-el-store-real-de-spec2viz-de-forma-transitiva-g5.md). deskops/.sldb/store.yaml (links) y .sldb/core/store_index.yaml enlazan spec2viz -> ../spec2viz/.sldb; por eso una sesion sldb mcp que federa el store de deskops abre unos 1233 archivos del store real de spec2viz, y el Done When de la tarea de IR task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opcion-a no se cumple. Decision de JP (opcion b): deskops quita su enlace; G5 ya decidio archivar el store de spec2viz con su repo.

## Goal

_Describe the concrete result this task must produce._

El store de deskops ya no enlaza spec2viz: sin entrada spec2viz en links de .sldb/store.yaml ni en .sldb/core/store_index.yaml, quitada con el CLI de sldb (sldb stores remove spec2viz --store .sldb). sldb stores check, deskops doctor y deskops graph missing no empeoran (mismos hallazgos que antes, salvo los que desaparecen por el enlace), y ningun modelo ni documento de deskops depende del store de spec2viz. Los otros enlaces (sldb, pron, scion) no cambian.

## Scope

_State what is in scope and what is out of scope._

Entra: .sldb/store.yaml y .sldb/core/store_index.yaml (solo via sldb stores remove), y los tests de deskops que se rompan legitimamente porque esperaban ese enlace en el store real. No entra: tocar el repo spec2viz ni archivarlo, quitar menciones a spec2viz en atomos, drawer, tareas o el codigo de deskops/graph/desk_graph.py (la regla de specs tiene su propia tarea), ni los tests que crean un vecino spec2viz en un sandbox (tests/test_doctor_absolute_paths.py usa el nombre como ejemplo y no lee el store real). Si sldb stores remove rechaza porque un modelo de deskops hereda del store de spec2viz, se para y se informa el modelo, sin forzar.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Guardar antes la salida de sldb stores check --store .sldb, deskops doctor --root . y deskops graph missing --root . en el run dir. 2) Buscar con grep 'spec2viz' en .sldb/core/models y .sldb/store.yaml si algun modelo viene de ese store. 3) sldb stores remove spec2viz --store .sldb. 4) Repetir los tres comandos y comparar. 5) Comprobar que sldb stores list --store .sldb ya no muestra spec2viz. 6) Correr los tests de stores y la suite.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && sldb stores list --store .sldb (sin spec2viz)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && sldb stores check --store .sldb (sin hallazgos nuevos respecto de antes)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops doctor --root . y deskops graph missing --root . (sin hallazgos nuevos respecto de antes)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_migrate_desk_stores.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas, cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

sldb stores list no muestra spec2viz, check, doctor y graph missing no tienen hallazgos nuevos y la suite no tiene fallas nuevas.
