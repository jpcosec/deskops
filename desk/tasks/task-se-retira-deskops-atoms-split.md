---
sldb:
  by: agent
  at: '2026-11-25T22:52:38Z'
  authority: generated
  via: save_document_payload
id: task-se-retira-deskops-atoms-split
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- deskops/services/atoms.py
depends_on: []
pills: []
files:
- deskops/services/atoms.py
- deskops/cli/commands/atoms.py
- deskops/cli/registry.py
- deskops/doc_access.py
- deskops/operations.py
- tests/test_transaction.py
- tests/fixtures/golden/help/deskops_atoms_split.txt
- docs/operator-manual.md
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Se retira deskops atoms split

## Rationale

_Explain why this task exists or the business driver behind it._

JP decidió el 25-11 retirarlo: desde CC35a sldb rechaza encabezados dentro de un campo, así que no se puede escribir un átomo con las secciones que split necesita; en el historial de git nadie lo usó nunca. Partir un átomo es crear dos con add atom y redirigir las referencias con rewrite_references de sldb.

## Goal

_Describe the concrete result this task must produce._

deskops atoms split no existe: se borran el comando, split_atom de services/atoms.py, sus tests y sus menciones en docs y skill.

## Scope

_State what is in scope and what is out of scope._

Entra: el comando, la función, los tests y las menciones. Sale: merge, delete y validate de átomos.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Borrar el comando y split_atom. 2) Borrar sus tests. 3) grep de 'atoms split' en docs, skill y AGENTS.md.

## Validation

_List the checks required before this task can close._

- grep -rn 'atoms split\|split_atom' deskops docs .claude AGENTS.md README.md no da resultados
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

No quedan el comando, la función, sus tests ni sus menciones.
