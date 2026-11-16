FILE:desk/tasks/task-readme-y-docs-dejan-de-nombrar-spec-artifacts-spec-fields-y-specregistry-borrados-en-cc30.md
---
sldb:
  by: agent
  at: '2026-11-16T04:07:22Z'
  authority: generated
  via: save_document_payload
id: task-readme-y-docs-dejan-de-nombrar-spec-artifacts-spec-fields-y-specregistry-borrados-en-cc30
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- README.md
- docs/knowledge-graph/desk-source-graph-vocabulary.md
- docs/diagrams/process/current-agent-workflow-and-automation.md
- docs/diagrams/process/current-agent-workflow-and-automation.mmd
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-docs-y-readme-todav-a-nombran-spec-artifacts-y-spec-fields-borrados-en-cc30.md
---

# README y docs dejan de nombrar spec/artifacts, spec/fields y SpecRegistry, borrados en CC30

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (2026-11-06): CC30 (squash 93cc1943) borro deskops/spec/artifacts, deskops/spec/fields, SpecRegistry, deskops/specs/loader.py y deskops/specs/mermaid.py, y paso id_pattern, status_default y tags a atributos de clase de cada modelo en deskops/models. Siguen nombrados en README.md:90, docs/knowledge-graph/desk-source-graph-vocabulary.md:63, docs/diagrams/process/current-agent-workflow-and-automation.md:63 y su .mmd:29.

## Goal

_Describe the concrete result this task must produce._

Esos archivos remiten a los atributos de clase de los modelos (deskops/models) y a deskops/doc_access.py; el grep de validacion queda vacio. El .mmd no tiene spec fuente (spec2viz se archiva, 80d32903), asi que se edita junto con su .md y el commit lo dice.

## Scope

_State what is in scope and what is out of scope._

Entra: los cuatro archivos citados y cualquier otro que muestre el grep. No entra: reescribir los diagramas ni migrarlos a specir.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr el grep de validacion. 2) Reescribir cada mencion. 3) Volver a correr el grep y los tests de docs.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rn 'spec/artifacts\|spec/fields\|SpecRegistry' README.md docs/
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_operator_manual.py

## Done When

_Name the observable condition that makes the task complete._

El grep no encuentra nada y test_operator_manual pasa.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-readme-y-docs-dejan-de-nombrar-spec-artifacts-spec-fields-y-specregistry-borrados-en-cc30: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

