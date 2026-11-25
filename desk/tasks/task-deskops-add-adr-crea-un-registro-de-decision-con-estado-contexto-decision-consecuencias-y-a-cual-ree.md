---
sldb:
  by: agent
  at: '2026-11-25T19:24:35Z'
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

# atom.adr: una decisión aceptada es un átomo que responde el porqué, con contexto, consecuencias, a cuál reemplaza y a qué aplica

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de JP (2026-11-25): "es en extremo importante empezar a entrar a documentar ADRs en deskops". Ese día se revirtió dos veces la misma decisión sobre la interfaz de specIR, y JP daba pron por retirado cuando el único registro (un ADR en Markdown dentro de sldb, de septiembre) decía otra cosa y nadie lo encontró. Hoy una decisión queda repartida entre un átomo, un task.decision, un review dispose y documentos sueltos en docs/ de cada repo, y nada lista las decisiones vigentes ni cuál reemplazó a cuál.

## Goal

_Describe the concrete result this task must produce._

Que una decisión de arquitectura aceptada sea un subtipo de átomo, atom.adr, modelado como los tipos de tarea. Una decisión pendiente no es un átomo: es una tarea task.decision, que cierra citando el atom.adr. Propuesta deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md (JP, 2026-11-25).

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/models/ (AtomAdrDoc y un registro ATOM_TYPE_MODELS como TASK_TYPE_MODELS), deskops add atom con --atom-type, el filtro por tipo y estado al listar átomos, el tipo de relación supersedes, las reglas sembradas en deskops/data/rules/, la materialización del ADR a Markdown y el manual del operador. Fuera: cambiar AtomDoc (su contrato y su hash no se tocan: el subtipo solo agrega), una interfaz, migrar decisiones anteriores a las cinco del 2026-11-25, federar ADR entre desks.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer deskops/models/task_types.py (un tipo es un modelo; un subtipo solo agrega; las compuertas son RuleDoc sembradas) y deskops/models/atom.py. AtomAdrDoc(AtomDoc) responde why, con la decisión como respuesta; agrega decided_on, decided_by y las secciones context, consequences y alternatives (opcional; lo descartado va aquí). Dos estados: accepted y superseded. El reemplazo es una arista supersedes de ADR a ADR; crearla deja al anterior en superseded, y una RuleDoc exige que ningún accepted tenga una supersedes entrante de otro accepted. Otra RuleDoc exige recibo de owner para crearlo. A qué aplica va en el campo común de punteros si ya existe (tarea de punteros de este desk); si no, en references, sin inventar tags. Un task.decision cierra citándolo con la evidencia atom que ya existe. El Markdown en docs/ es una materialización (deskops materialize).

Aclaraciones de la revisión: AtomAdrDoc va en un módulo propio (deskops/models/adr.py) que importa AtomDoc; no editar atom.py, porque la tarea de punteros (task-atomos-pills-y-tareas-guardan-el-donde-...) corre en paralelo sobre ese archivo. Punteros: si al empezar AtomDoc ya tiene el campo pointers (está en main), usarlo; si no, references; no esperar. Los cinco ADR: /mnt/ssd/proyectos/SLDB_1/sldb/docs/architecture/{mechanism-in-sldb-content-in-specir,pron-is-archived,one-command-taxonomy-served-by-fastmcp,surface-is-an-editor-contract}.md y /mnt/ssd/proyectos/SLDB_1/IR/docs/decisiones/paridad-por-capacidades.md (más sldb-absorbs-kgdb.md como el reemplazado). Recibo de owner: el mismo de task.decision (deskops review record --kind owner; dispose accepted solo JP); la RuleDoc exige un ReviewDoc kind owner accepted cuyo sujeto es el ADR. Reemplazo parcial: arista supersedes con atributo opcional section; con section, el anterior sigue accepted y la RuleDoc de 'sin supersedes entrante' ignora las parciales. Reglas: dos RuleDoc nuevas en deskops/data/rules/ (la de supersedes y la de owner), nombradas como las existentes. El filtro 'solo accepted' es solo de deskops list atoms --type atom.adr (o el verbo que use el listado de tipos); --all muestra todos; el listado general no cambia. tests/test_adr_artifact.py se crea. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_adr_artifact.py
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

deskops add atom --atom-type atom.adr crea el registro; sin recibo de owner la regla lo rechaza. Declarar que reemplaza a otro deja al anterior en superseded y la regla de consistencia pasa. Listar los de tipo atom.adr muestra por defecto solo los accepted. Un task.decision cierra citando un atom.adr. Materializarlo produce un Markdown con Status, Date, Decision Maker, Supersedes, Context, Decision y Consequences. El hash del contrato de AtomDoc no cambia. Quedan cargados los cinco ADR del 2026-11-25 (cuatro de sldb/docs/architecture/ y IR/docs/decisiones/paridad-por-capacidades.md), con pron-is-archived reemplazando la sección de pron de sldb-absorbs-kgdb. El manual del operador describe el flujo.
