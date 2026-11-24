---
sldb:
  by: agent
  at: '2026-11-24T02:19:12Z'
  authority: generated
  via: save_document_payload
id: task-jp-decide-como-se-alimenta-deskops-atoms-split-por-el-cli-opcion-a-b-o-c
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/services/atoms.py
- tests/test_atoms_split.py
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-atoms-split-no-se-puede-alimentar-por-el-cli-desde-cc35a-sldb-rechaza-encabezados-en-el-field.md
---

# JP decide como se alimenta deskops atoms split por el CLI (opcion a, b o c)

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer. `deskops atoms split` parte un atomo por los encabezados de su answer (deskops/services/atoms.py:320 y 572), pero desde CC35a toda escritura pasa por sldb.api.transaction y sldb rechaza encabezados dentro de un field como ruido estructural; tests/test_atoms_split.py pasa solo porque escribe el atomo a mano (linea 41). La demo de split se quito del manual el 2026-11-09 (decision revisable).

## Goal

_Describe the concrete result this task must produce._

JP elige: (a) split recibe las partes por flags sin encabezados (p. ej. `--part a="texto"`), cambia la gramatica del CLI y sus goldens; (b) un modelo de atomo con secciones declaradas como campos; (c) dejar split como esta, inalcanzable por el CLI, o retirarlo. El coordinador del plan recomendo (a), que choca con el invariante 2 de alcance.md de deskops-como-config. Con la eleccion se crea la tarea de codigo.

## Scope

_State what is in scope and what is out of scope._

Entra: la decision y el alta de la tarea que la implementa. No entra: implementar.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Presentar las opciones a JP. 2) Registrar el recibo owner. 3) Crear la tarea de codigo de la opcion elegida.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops list tasks --root . (aparece la tarea de la opcion elegida, o el retiro de split)

## Done When

_Name the observable condition that makes the task complete._

La opcion elegida por JP esta registrada y existe la tarea que la implementa.
