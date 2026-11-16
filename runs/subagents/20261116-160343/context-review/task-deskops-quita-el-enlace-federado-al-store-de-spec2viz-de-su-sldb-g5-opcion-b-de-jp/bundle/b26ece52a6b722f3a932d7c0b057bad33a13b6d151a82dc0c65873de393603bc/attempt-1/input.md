FILE:desk/tasks/task-deskops-quita-el-enlace-federado-al-store-de-spec2viz-de-su-sldb-g5-opcion-b-de-jp.md
---
sldb:
  by: agent
  at: '2026-11-16T16:03:07Z'
  authority: generated
  via: save_document_payload
id: task-deskops-quita-el-enlace-federado-al-store-de-spec2viz-de-su-sldb-g5-opcion-b-de-jp
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-122447-suggestion-deskops-sldb-enlaza-spec2viz-las-pruebas-mcp-de-ir-leen-el-store-real-de-spec2viz-de-forma-transitiva-g5.md
- desk/inbox/20261116-130201-suggestion-g5-opci-n-b-decisi-n-de-jp-deskops-quita-su-enlace-al-store-de-spec2viz-ir-espera-con-un-espejo.md
depends_on: []
pills: []
files:
- .sldb/store.yaml
- .sldb/core/store_index.yaml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
---

# deskops quita el enlace federado al store de spec2viz de su .sldb (G5, opcion b de JP)

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de IR del 2026-11-16 (desk/inbox/20261116-122447-suggestion-deskops-sldb-enlaza-spec2viz-las-pruebas-mcp-de-ir-leen-el-store-real-de-spec2viz-de-forma-transitiva-g5.md). deskops/.sldb/store.yaml (links) y .sldb/core/store_index.yaml enlazan spec2viz -> ../spec2viz/.sldb; por eso una sesion sldb mcp que federa el store de deskops abre unos 1233 archivos del store real de spec2viz, y el Done When de la tarea de IR task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opcion-a no se cumple. Decision de JP (opcion b): deskops quita su enlace; G5 ya decidio archivar el store de spec2viz con su repo.

## Goal

_Describe the concrete result this task must produce._

El store de deskops ya no enlaza spec2viz: sin entrada spec2viz en links de .sldb/store.yaml ni en .sldb/core/store_index.yaml, quitada con el CLI de sldb (sldb stores remove spec2viz --store .sldb). sldb stores check, deskops doctor y deskops graph missing no empeoran (mismos hallazgos que antes, salvo los que desaparecen por el enlace), y ningun modelo ni documento de deskops depende del store de spec2viz. Los otros enlaces (sldb, pron, scion) no cambian.

## Scope

_State what is in scope and what is out of scope._

Entra: .sldb/store.yaml y .sldb/core/store_index.yaml (solo via sldb stores remove), y los tests de deskops que se rompan legitimamente porque esperaban ese enlace en el store real. No entra: tocar el repo spec2viz ni archivarlo, quitar menciones a spec2viz en atomos, drawer, tareas o el codigo de deskops/graph/desk_graph.py (la regla de specs tiene su propia tarea), ni los tests que crean un vecino spec2viz en un sandbox (tests/test_doctor_absolute_paths.py usa el nombre como ejemplo y no lee el store real). Si sldb stores remove rechaza porque un modelo de deskops hereda del store de spec2viz, se para y se informa el modelo, sin forzar.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Guardar antes la salida de sldb stores check --store .sldb, deskops doctor --root . y deskops graph missing --root . en el run dir. 2) Buscar con grep 'spec2viz' en .sldb/core/models y .sldb/store.yaml si algun modelo viene de ese store. 3) sldb stores remove spec2viz --store .sldb. 4) Repetir los tres comandos y comparar. 5) Comprobar que sldb stores list --store .sldb ya no muestra spec2viz. 6) Correr los tests de stores y la suite.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && sldb stores list --store .sldb (sin spec2viz)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && sldb stores check --store .sldb (sin hallazgos nuevos respecto de antes)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops doctor --root . y deskops graph missing --root . (sin hallazgos nuevos respecto de antes)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_migrate_desk_stores.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas, cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

sldb stores list no muestra spec2viz, check, doctor y graph missing no tienen hallazgos nuevos y la suite no tiene fallas nuevas.

FILE:desk/atoms/workflow-model/atom-code-changes-close-with-tests-and-commit.md
---
id: atom-code-changes-close-with-tests-and-commit
title: Code changes close with tests and commit
five_wh_one_plus: when
tags:
- system:deskops
- topic:testing
- topic:git
- topic:closeout
---

# Code changes close with tests and commit

## Answer

A task that modifies code is not closed until relevant tests pass and the completed change is recorded in a descriptive git commit.

FILE:.sldb/core/store_index.yaml
stores:
- name: sldb
  path: ../sldb/.sldb
- name: spec2viz
  path: ../spec2viz/.sldb
- name: pron
  path: ../pron/.sldb
- name: scion
  path: ../scion/.sldb
models:
- name: AtomDoc
  model_ref: deskops.models:AtomDoc
  path: deskops/models/atom.py
  models_index: .sldb/core/models/AtomDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics: []
- name: RepositoryDoc
  model_ref: deskops.models:RepositoryDoc
  path: deskops/models/repository.py
  models_index: .sldb/core/models/RepositoryDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics: []
- name: TaskDoc
  model_ref: deskops.models:TaskDoc
  path: deskops/models/task.py
  models_index: .sldb/core/models/TaskDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics: []
- name: RoleDoc
  model_ref: deskops.models:RoleDoc
  path: deskops/models/role.py
  models_index: .sldb/core/models/RoleDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics: []
- name: RuntimeProfileDoc
  model_ref: deskops.models:RuntimeProfileDoc
  path: deskops/models/runtime_profile.py
  models_index: .sldb/core/models/RuntimeProfileDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - type.workflow.runtime_profile
  - workspace.desk.runtimes
- name: RunDoc
  model_ref: deskops.models:RunDoc
  path: deskops/models/run.py
  models_index: .sldb/core/models/RunDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - type.workflow.run
  - workspace.desk.runs
- name: ProtoAtomDoc
  model_ref: deskops.models:ProtoAtomDoc
  path: deskops/models/protoatom.py
  models_index: .sldb/core/models/ProtoAtomDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - type.knowledge.protoatom
  - workspace.desk.atoms
- name: CrossroadDoc
  model_ref: deskops.models:CrossroadDoc
  path: deskops/models/crossroad.py
  models_index: .sldb/core/models/CrossroadDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - type.knowledge.crossroad
  - workspace.desk.atoms
- name: PillDoc
  model_ref: deskops.models:PillDoc
  path: deskops/models/pill.py
  models_index: .sldb/core/models/PillDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.workflow.pill
  - workspace.desk
- name: StepDoc
  model_ref: deskops.models:StepDoc
  path: deskops/models/step.py
  models_index: .sldb/core/models/StepDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.workflow.step
  - workspace.desk
- name: RitualDoc
  model_ref: deskops.models:RitualDoc
  path: deskops/models/ritual.py
  models_index: .sldb/core/models/RitualDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.workflow.ritual
  - workspace.desk
- name: InboxNoteDoc
  model_ref: deskops.models:InboxNoteDoc
  path: deskops/models/inbox.py
  models_index: .sldb/core/models/InboxNoteDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.desk.inbox-note
  - workspace.desk.inbox
- name: BoardDoc
  model_ref: deskops.models:BoardDoc
  path: deskops/models/board.py
  models_index: .sldb/core/models/BoardDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.workflow.board
  - workspace.desk
- name: MaterializationContractDoc
  model_ref: deskops.models:MaterializationContractDoc
  path: deskops/models/materialization.py
  models_index: .sldb/core/models/MaterializationContractDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.knowledge.materialization_contract
  - workspace.desk.materializations
- name: RelationTypeDoc
  model_ref: sldb.models.relation_type_doc:RelationTypeDoc
  path: /home/jp/proyectos/SLDB_1/sldb/src/sldb/models/relation_type_doc.py
  models_index: .sldb/core/models/RelationTypeDoc.yaml
  version: 1
  canonical: false
  family: relation
  semantics:
  - layer.topology
  - representation.markdown
  - source.document.markdown
  - type.relation.type
- name: RelationDoc
  model_ref: sldb.models.relation_doc:RelationDoc
  path: /home/jp/proyectos/SLDB_1/sldb/src/sldb/models/relation_doc.py
  models_index: .sldb/core/models/RelationDoc.yaml
  version: 1
  canonical: false
  family: relation
  semantics:
  - layer.topology
  - representation.markdown
  - source.document.markdown
  - type.relation.instance
- name: DeskFAQDoc
  model_ref: deskops.models:DeskFAQDoc
  path: deskops/models/faq.py
  models_index: .sldb/core/models/DeskFAQDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.documentation.faq
  - workspace.docs.faq
- name: TaskCodeDoc
  model_ref: deskops.models:TaskCodeDoc
  path: deskops/models/task_types.py
  models_index: .sldb/core/models/TaskCodeDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.workflow.task
  - workspace.desk
- name: TaskDocsDoc
  model_ref: deskops.models:TaskDocsDoc
  path: deskops/models/task_types.py
  models_index: .sldb/core/models/TaskDocsDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.workflow.task
  - workspace.desk
- name: TaskDebugDoc
  model_ref: deskops.models:TaskDebugDoc
  path: deskops/models/task_types.py
  models_index: .sldb/core/models/TaskDebugDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.workflow.task
  - workspace.desk
- name: TaskRefactorDoc
  model_ref: deskops.models:TaskRefactorDoc
  path: deskops/models/task_types.py
  models_index: .sldb/core/models/TaskRefactorDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.workflow.task
  - workspace.desk
- name: TaskDecisionDoc
  model_ref: deskops.models:TaskDecisionDoc
  path: deskops/models/task_types.py
  models_index: .sldb/core/models/TaskDecisionDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.workflow.task
  - workspace.desk
- name: TaskAggregateDoc
  model_ref: deskops.models:TaskAggregateDoc
  path: deskops/models/task_types.py
  models_index: .sldb/core/models/TaskAggregateDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.workflow.task
  - workspace.desk
- name: TaskExternalDoc
  model_ref: deskops.models:TaskExternalDoc
  path: deskops/models/task_types.py
  models_index: .sldb/core/models/TaskExternalDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.workflow.task
  - workspace.desk
- name: ReviewDoc
  model_ref: deskops.models:ReviewDoc
  path: deskops/models/review.py
  models_index: .sldb/core/models/ReviewDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - representation.markdown
  - source.document.markdown
  - type.workflow.review
  - workspace.desk.runs
- name: RuleDoc
  model_ref: sldb.models.rule_doc:RuleDoc
  path: /mnt/ssd/proyectos/SLDB_1/sldb-runtime/src/sldb/models/rule_doc.py
  models_index: .sldb/core/models/RuleDoc.yaml
  version: 1
  canonical: false
  family: rule
  semantics:
  - layer.governance
  - representation.markdown
  - source.document.markdown
  - type.rule
- name: ViewDoc
  model_ref: sldb.models.notation_models:ViewDoc
  path: /dev/shm/integ-deskops/venv/lib/python3.13/site-packages/sldb/models/notation/view_doc.py
  models_index: .sldb/core/models/ViewDoc.yaml
  version: 1
  canonical: false
  family: null
  semantics:
  - layer.presentation
  - representation.markdown
  - source.document.markdown
  - system.spec2viz
  - type.view
predicates:
- name: has_model
  axis: WHAT
  description: The store registers this model.
- name: has_document
  axis: WHAT
  description: The model has this document as an instance.
- name: has_section
  axis: WHERE
  description: The document contains this section.
- name: tagged_as
  axis: WHAT
  description: The model, document or section carries this semantic tag.
- name: semantic_parent
  axis: WHAT
  description: This tag is a child of that tag in the semantic DAG.
- name: semantic_equivalent
  axis: WHAT
  description: This local tag maps to that global tag across linked stores.
- name: has_field
  axis: WHAT
  description: The model declares this field; the field node carries its type and
    description.
- name: extends
  axis: WHAT
  description: The model inherits from that model (base_models); instances of the
    source are instances of the target.
- name: applies_to_source
  axis: WHAT
  description: 'Instances of this model may be the source of edges of this relation
    type: the verbs a class can be subject of.'
- name: applies_to_target
  axis: WHAT
  description: Instances of this model may be the target of edges of this relation
    type.
- name: names
  axis: WHAT
  description: The anchor (an alias word) names this model, field, relation type or
    document.
- name: references
  axis: WHAT
  description: A field the model declared in `__references__` holds this document's
    id; the edge carries the field name.
- name: contains
  axis: WHERE
  description: A field the model declared in `__containment__` holds this document
    as a child; the edge carries the field name and the models the declaration allows.
- name: composes
  axis: WHAT
  description: A composed field of the source (`__compositions__`) renders this document's
    payload into the source's text; the edge carries the composed field, the field
    holding the refs and the ref as authored.
store_hash: d18ba9094303b46f2ead3d1a88594f9267fb5038de161af798217e99ec5f8909

FILE:instruccion
Cold-bundle de la tarea task-deskops-quita-el-enlace-federado-al-store-de-spec2viz-de-su-sldb-g5-opcion-b-de-jp: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && sldb stores list --store .sldb (sin spec2viz)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && sldb stores check --store .sldb (sin hallazgos nuevos respecto de antes)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops doctor --root . y deskops graph missing --root . (sin hallazgos nuevos respecto de antes)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_migrate_desk_stores.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas, cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea

