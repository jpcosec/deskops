Task: task-un-solo-vocabulario-de-tags-semanticos-en-deskops-padres-declarados-en-sldb-add-sin-duplicados-y-mig
Title: Un solo vocabulario de tags semanticos en deskops: padres declarados en sldb, add sin duplicados y migracion por CLI
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-code] TaskCodeDoc:task-un-solo-vocabulario-de-tags-semanticos-en-deskops-padres-declarados-en-sldb-add-sin-duplicados-y-mig: Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "bundle") (seen: {}) (witness: ReviewDoc:review-task-un-solo-vocabulario-de-tags-semanticos-en-deskops-padres-declarados-en-sldb-add-sin-duplicados-y-mig-bundle-1 {"verdict":"pending"})

---
sldb:
  by: agent
  at: '2026-11-23T17:32:00Z'
  authority: generated
  via: save_document_payload
id: task-un-solo-vocabulario-de-tags-semanticos-en-deskops-padres-declarados-en-sldb-add-sin-duplicados-y-mig
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261123-142641-suggestion-jp-arreglar-el-store-sem-ntico-de-deskops-dos-vocabularios-de-tags.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Un solo vocabulario de tags semanticos en deskops: padres declarados en sldb, add sin duplicados y migracion por CLI

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-142641-suggestion-jp-arreglar-el-store-sem-ntico-de-deskops-dos-vocabularios-de-tags (JP 2026-11-23, MUY importante): el store semantico de deskops mezcla tags de modelo con puntos y jerarquia (workspace.desk.atoms, type.workflow.task, layer.topology) con tags libres con dos puntos en el frontmatter, planos y sin padres en .sldb_cache/semantic_dag.yaml (workspace:desk 792 docs, system:deskops 537, artifact:task, topic:*, pill-type:*, host:*, runtime:*, layer:cli), con duplicados (workspace:desk/workspace.desk, artifact:task/type.workflow.task, layer:*/layer.*), nombres de clase como tag (TaskDoc, PrimitiveDoc, OperationalArtifactDoc) y sueltos (ci/cd, demo). El lector de surface agrupa por semantica y depende de esto.

## Goal

_Describe the concrete result this task must produce._

deskops tiene un vocabulario unico de tags semanticos: cada tag libre que sobrevive tiene padre declarado con sldb semantic parent o es equivalente declarado (sldb semantic equivalent) del tag de modelo; deskops add y deskops edit dejan de escribir los duplicados; los documentos existentes del desk de deskops quedan migrados por CLI; .sldb_cache/semantic_dag.yaml ya no tiene tags planos sin padre salvo los que el informe justifique.

## Scope

_State what is in scope and what is out of scope._

Entra: inventario de tags (sldb semantic / store de deskops), tabla de mapeo vieja->nueva en el informe, cambios en los templates o validadores de deskops que escriben tags, comando o paso de migracion por CLI y su ejecucion sobre el desk de deskops, tests. Si a sldb le falta una operacion para migrar tags en bloque: no se edita .sldb a mano; se deja nota a sldb con deskops message send --to sldb y se migra lo que el CLI permita. Fuera: otros desks (se migran despues con el mismo comando) y el lector de surface.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventariar tags con sldb semantic y el store de deskops; contar documentos por tag. 2) Proponer en result-summary.md la tabla de mapeo (que tag queda, padre, equivalente, cual se borra) siguiendo los tags de modelo con puntos como canonicos. 3) Declarar padres y equivalentes con sldb semantic parent/equivalent. 4) Ajustar deskops add/edit (templates y validadores de tags) para no escribir duplicados ni nombres de clase como tag, con tests. 5) Migrar los documentos del desk por CLI (deskops edit o comando nuevo) y regenerar el cache semantico. 6) Medir antes y despues: tags planos sin padre en semantic_dag.yaml.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp pytest -q de los tests tocados; deskops doctor --root .; conteo de tags sin padre en .sldb_cache/semantic_dag.yaml antes y despues

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan; deskops add task/atom/pill de prueba no escribe tags duplicados; el informe muestra la tabla de mapeo y el conteo antes/despues de tags planos sin padre, con el despues en 0 o justificado; el desk de deskops queda migrado y deskops doctor no suma errores.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-un-solo-vocabulario-de-tags-semanticos-en-deskops-padres-declarados-en-sldb-add-sin-duplicados-y-mig"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-5f0471f4b90c"

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-5f0471f4b90c`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-5f0471f4b90c

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
