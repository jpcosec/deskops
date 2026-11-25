---
sldb:
  by: agent
  at: '2026-11-25T17:03:31Z'
  authority: generated
  via: create_document
id: task-jp-decide-si-deskops-pasa-a-ser-un-plugin-de-sldb-modelos-reglas-vistas-y-ritos-como-datos-del-store
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/tasks/task-cc51-docs-config-vs-code-md-con-la-medicion-de-lineas-de-codigo-frente-a-configuracion-y-el-inventar.md
- desk/tasks/task-jp-fija-n-la-meta-de-lineas-de-python-de-deskops-que-exige-cc51.md
- desk/tasks/task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph.md
depends_on: []
pills: []
files: []
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# JP decide si deskops pasa a ser un plugin de sldb (modelos, reglas, vistas y ritos como datos del store) y qué queda como código propio

## Rationale

_Explain why this task exists or the business driver behind it._

JP, 25-11: 'esto debería ser básicamente un plugin sobre sldb, creo que estamos fallando ahí'. Hoy deskops tiene 27.236 líneas de Python en 117 archivos (sldb tiene 56.370). Lo más grande es código de workflow que podría ser datos de sldb: cli/registry.py 2151, services/closure.py 1989 (gates de cierre), workspace.py 1107, services/review.py 1104, doc_access.py 1066, services/atoms.py 1013, lifecycle.py 576. AGENTS.md del workspace ya dice que todo lo modelado es dato en un store de sldb, chequeado por reglas.

## Goal

_Describe the concrete result this task must produce._

Una decisión escrita de JP: qué partes de deskops pasan a ser modelos, reglas, ViewDocs y ritos declarados en el store (y qué pide eso a sldb, por su inbox), qué queda como código (dispatch/scion, git, CLI delgado) y en qué orden se migra.

## Scope

_State what is in scope and what is out of scope._

Entra: el inventario por módulo (dato de sldb vs código propio), lo que falta en sldb para soportarlo (registro de comandos/extensiones, H9 de vistas en stores enlazados, gates como reglas) y la decisión. Sale: implementar la migración; cada pieza será su propia tarea. Relacionadas: CC51 (config vs code), JP fija N, deskops usa las APIs públicas de sldb y borra sus rodeos, Governance: interfaz MCP y UI.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventario por módulo con una columna de 'existe en sldb hoy / falta en sldb / es de deskops'. 2) Pedidos a sldb por deskops message send --to sldb --kind unclear para lo que falte. 3) JP elige el corte y el orden. 4) Las tareas CC51 y 'JP fija N' se reescriben con esa meta.

## Validation

_List the checks required before this task can close._

- La decisión de JP queda registrada en esta tarea y en un átomo, y existen las tareas o pedidos a sldb que salen de ella

## Done When

_Name the observable condition that makes the task complete._

JP decidió el corte deskops/sldb y cada pieza a migrar tiene tarea o pedido en el inbox de sldb.
