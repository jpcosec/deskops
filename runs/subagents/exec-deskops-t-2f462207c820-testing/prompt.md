Task: task-readme-y-docs-dejan-de-nombrar-spec-artifacts-spec-fields-y-specregistry-borrados-en-cc30
Title: README y docs dejan de nombrar spec/artifacts, spec/fields y SpecRegistry, borrados en CC30
Status: active
Current node: ritual-testing
Task type: task.docs
From drawer: desk/drawer/tasks/task-docs-y-readme-todav-a-nombran-spec-artifacts-y-spec-fields-borrados-en-cc30.md
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-19T17:54:59Z'
  authority: generated
  via: save_document_payload
id: task-readme-y-docs-dejan-de-nombrar-spec-artifacts-spec-fields-y-specregistry-borrados-en-cc30
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
history:
- task_activates
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

Entra solo README.md y lo que haya bajo docs/ (el grep de validacion define el conjunto). Destino de cada mencion: si habla de id_pattern, status_default o tags por artefacto -> los atributos de clase del modelo en deskops/models; si habla de cargar o resolver artefactos -> deskops/doc_access.py; si habla de SpecRegistry o del loader -> se borra la frase y se remite a deskops/models. El mensaje del commit dice 'el .mmd no tiene spec fuente; se edita junto a su .md'. No entra: reescribir los diagramas ni migrarlos a specir. Solo se corre test_operator_manual.py.

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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-readme-y-docs-dejan-de-nombrar-spec-artifacts-spec-fields-y-specregistry-borrados-en-cc30"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.
