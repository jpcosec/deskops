FILE:desk/tasks/task-deskops-add-adr-crea-un-registro-de-decision-con-estado-contexto-decision-consecuencias-y-a-cual-ree.md
---
sldb:
  by: agent
  at: '2026-11-25T17:45:24Z'
  authority: generated
  via: create_document
id: task-deskops-add-adr-crea-un-registro-de-decision-con-estado-contexto-decision-consecuencias-y-a-cual-ree
status: draft
summary: ''
tags: []
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
---

# deskops add adr crea un registro de decisión con estado, contexto, decisión, consecuencias y a cuál reemplaza, y deskops list adrs muestra los vigentes

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de JP (2026-11-25): "es en extremo importante empezar a entrar a documentar ADRs en deskops". Ese día se revirtió dos veces la misma decisión sobre la interfaz de specIR, y JP daba pron por retirado cuando el único registro (un ADR en Markdown dentro de sldb, de septiembre) decía otra cosa y nadie lo encontró. Hoy una decisión queda repartida entre un átomo, un task.decision, un review dispose y documentos sueltos en docs/ de cada repo, y nada lista las decisiones vigentes ni cuál reemplazó a cuál.

## Goal

_Describe the concrete result this task must produce._

Que una decisión de arquitectura sea un artefacto modelado del desk, que se crea y se lista por CLI y que sabe a qué decisión anterior reemplaza.

## Scope

_State what is in scope and what is out of scope._

Dentro: un tipo de artefacto nuevo con su modelo, add, list, show y edit; la relación de reemplazo; que un task.decision pueda citar un ADR como su documento de cierre. Fuera: una interfaz, migrar decisiones antiguas más allá de las cinco de la lista.

## Implementation Path

_Outline the expected implementation route or affected surface._

Antes de modelar, leer cómo registran decisiones hoy task.decision (deskops/models/task_types.py), los átomos de decisión y deskops review dispose, y dejar escrito en la tarea por qué ninguno cubre contexto, alternativas y reemplazo. Si uno de ellos lo cubre con un cambio menor, se extiende ese y no se crea un tipo. El formato de partida es el de sldb/docs/architecture/sldb-absorbs-kgdb.md.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_adr_artifact.py
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

deskops add adr crea el registro con estado propuesto, aceptado o reemplazado. Marcar que un ADR reemplaza a otro cambia el estado del anterior. deskops list adrs muestra por defecto solo los vigentes. Quedan cargados como primeros registros los cinco del 2026-11-25: cuatro de sldb/docs/architecture/ (mechanism-in-sldb-content-in-specir, pron-is-archived, one-command-taxonomy-served-by-fastmcp, surface-is-an-editor-contract) y IR/docs/decisiones/paridad-por-capacidades.md. El manual del operador describe el flujo.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-add-adr-crea-un-registro-de-decision-con-estado-contexto-decision-consecuencias-y-a-cual-ree: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

