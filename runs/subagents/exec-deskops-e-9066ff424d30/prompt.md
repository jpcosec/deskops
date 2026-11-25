Task: task-deskops-add-adr-crea-un-registro-de-decision-con-estado-contexto-decision-consecuencias-y-a-cual-ree
Title: deskops add adr crea un registro de decisión con estado, contexto, decisión, consecuencias y a cuál reemplaza, y deskops list adrs muestra los vigentes
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-code] TaskCodeDoc:task-deskops-add-adr-crea-un-registro-de-decision-con-estado-contexto-decision-consecuencias-y-a-cual-ree: Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight") (seen: {}) (witness: ReviewDoc:review-task-deskops-add-adr-crea-un-registro-de-decision-con-estado-contexto-decision-consecuencias-y-a-cual-ree-bundle-1 {"anchor_state":"changed"})

---
sldb:
  by: agent
  at: '2026-11-25T18:04:32Z'
  authority: generated
  via: save_document_payload
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

Aclaraciones de la revisión: IR está en /mnt/ssd/proyectos/SLDB_1/IR y sldb en /mnt/ssd/proyectos/SLDB_1/sldb (leer sus ADR: sldb/docs/architecture/*.md con Status, e IR/docs/decisiones/paridad-por-capacidades.md). Antes de crear un tipo, mirar los artefactos existentes de deskops (TaskDecisionDoc, AtomDoc, FAQ); cambio menor = agregar campos opcionales sin romper documentos existentes; si no basta, se crea el tipo y el porqué va en el commit y en result-summary. Estados: propuesto, aceptado, reemplazado; vigente = aceptado y no reemplazado. 'add adr --supersedes <id>' pone el anterior en reemplazado y guarda el vínculo en ambos. CLI: deskops add adr, deskops list adrs [--all], deskops show adr <id>, deskops edit adr <id> <campo> <valor>, como los demás artefactos. task.decision cita un ADR por su id en references; closeout verify lo acepta como documento de cierre. Manual del operador = docs/ de deskops donde se documentan los demás verbos add. tests/test_adr_artifact.py cubre add, list (vigentes y --all), supersedes y la cita desde un task.decision.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_adr_artifact.py
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

deskops add adr crea el registro con estado propuesto, aceptado o reemplazado. Marcar que un ADR reemplaza a otro cambia el estado del anterior. deskops list adrs muestra por defecto solo los vigentes. Quedan cargados como primeros registros los cinco del 2026-11-25: cuatro de sldb/docs/architecture/ (mechanism-in-sldb-content-in-specir, pron-is-archived, one-command-taxonomy-served-by-fastmcp, surface-is-an-editor-contract) y IR/docs/decisiones/paridad-por-capacidades.md. El manual del operador describe el flujo.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-deskops-add-adr-crea-un-registro-de-decision-con-estado-contexto-decision-consecuencias-y-a-cual-ree"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-9066ff424d30"

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-9066ff424d30`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-9066ff424d30

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
