Task: task-un-solo-vocabulario-de-tags-semanticos-en-deskops-padres-declarados-en-sldb-add-sin-duplicados-y-mig
Title: Un solo vocabulario de tags semanticos en deskops: padres declarados en sldb, add sin duplicados y migracion por CLI
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-23T17:52:01Z'
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
- desk/inbox/20261123-145007-suggestion-jp-precisa-el-store-sem-ntico-apartados-y-filtros-por-sem-ntica-resueltos-por-sldb.md
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

Criterio de JP (nota 20261123-145007-suggestion-jp-precisa-el-store-sem-ntico-apartados-y-filtros-por-sem-ntica-resueltos-por-sldb), demostrable sobre el desk real de deskops y desde el lector de surface: (1) un apartado declarado con una semantica (ejemplo de JP: board.tareas) lista todas las tareas; (2) filtrar por una semantica mas especifica (por ejemplo tareas de UI) devuelve solo esas; (3) ambas consultas se resuelven con el store semantico de sldb (tags, padres, descendientes), sin listas ni filtros propios de deskops. Para eso los tags que escribe deskops pasan a ser tags del store semantico de sldb con padres declarados (sldb semantic parent/equivalent), los duplicados desaparecen y los documentos existentes quedan migrados por CLI.

## Scope

_State what is in scope and what is out of scope._

Regla del workspace: deskops es configuracion sobre sldb y nunca reimplementa lo que sldb tiene. Entra: inventario de tags del desk de deskops y sus documentos; tabla de mapeo a semanticas del store de sldb con padres (board.tareas o equivalente como padre de las tareas, y semanticas hijas como tareas de UI); declaracion con sldb semantic parent/equivalent; cambios en deskops add/edit y sus templates para escribir esas semanticas y no los tags propios con dos puntos; migracion de los documentos existentes por CLI; tests. Si a sldb le falta una operacion (consulta por tag con descendientes, migracion de tags en bloque), no se edita .sldb a mano ni se reimplementa en deskops: va nota a sldb con deskops message send --to sldb. Un intento previo (worktree .worktrees/deskops-e-5f0471f4b90c, sin commit) cambio 23 archivos de modelos y templates en la direccion anterior; se puede consultar pero no se da por bueno. Fuera: el lector de surface y otros desks.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventariar tags con sldb semantic y el store de deskops; contar documentos por tag. 2) Proponer en result-summary.md la tabla de mapeo (que tag queda, padre, equivalente, cual se borra) siguiendo los tags de modelo con puntos como canonicos. 3) Declarar padres y equivalentes con sldb semantic parent/equivalent. 4) Ajustar deskops add/edit (templates y validadores de tags) para no escribir duplicados ni nombres de clase como tag, con tests. 5) Migrar los documentos del desk por CLI (deskops edit o comando nuevo) y regenerar el cache semantico. 6) Medir antes y despues: tags planos sin padre en semantic_dag.yaml.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp pytest -q de los tests tocados; deskops doctor --root .; conteo de tags sin padre en .sldb_cache/semantic_dag.yaml antes y despues

## Done When

_Name the observable condition that makes the task complete._

Sobre el desk real: una consulta de sldb por la semantica del apartado (board.tareas o la que el informe fije como equivalente) devuelve todas las tareas trackeadas, y una por una semantica hija (tareas de UI) devuelve solo esas; sldb semantic show de esas semanticas muestra padres e hijos; el informe trae los comandos y sus salidas; deskops no agrega listas ni filtros propios; si a sldb le falta una operacion (consulta por tag con descendientes, migracion en bloque) queda nota a sldb y lo no resuelto se lista; deskops doctor no suma errores.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-un-solo-vocabulario-de-tags-semanticos-en-deskops-padres-declarados-en-sldb-add-sin-duplicados-y-mig"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-e558315aff21"

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-e558315aff21`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-e558315aff21

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
