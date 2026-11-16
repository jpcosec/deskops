FILE:desk/tasks/task-deskops-declara-el-namespace-de-tags-host-para-marcar-en-que-maquina-corre-cada-tarea.md
---
sldb:
  by: agent
  at: '2026-11-16T04:03:28Z'
  authority: generated
  via: create_document
id: task-deskops-declara-el-namespace-de-tags-host-para-marcar-en-que-maquina-corre-cada-tarea
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-003533-suggestion-namespace-de-tags-host-para-marcar-en-qu-m-quina-corre-cada-tarea.md
- desk/inbox/20261116-003602-suggestion-namespace-de-tags-host-para-separar-tareas-de-ui-local-y-backend-robocop2.md
- desk/inbox/20261116-004745-suggestion-namespace-de-tags-host-para-rutear-tareas-por-m-quina-triaje-2026-11-16.md
- desk/inbox/20261116-004744-suggestion-triaje-2026-11-16-falta-un-namespace-de-tags-para-el-host-de-una-tarea-host-local-host-robocop2.md
- /mnt/ssd/proyectos/SLDB_1/triaje-drawers-inbox-brief.md
depends_on: []
pills: []
files:
- deskops/atom_tags.py
- docs/workflow-policy-reference.md
- .sldb/store.yaml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops declara el namespace de tags host para marcar en que maquina corre cada tarea

## Rationale

_Explain why this task exists or the business driver behind it._

Dos notas del 2026-11-16 (IR y deskops), del triaje de drawers e inbox: JP pide que cada TaskDoc diga en que maquina corre. Lo que tiene UI o verificacion en navegador va a la maquina local; suites, build --check, benchmarks, migraciones, scion y revisiones van a robocop2. La via es TaskDoc.tags, pero ningun store del ecosistema declara un namespace para la maquina (deskops no declara tag_namespaces en .sldb/store.yaml; sldb e IR solo tienen domain, layer, system y topic).

## Goal

_Describe the concrete result this task must produce._

La semilla de tag namespaces que deskops escribe en cada desk (deskops/atom_tags.py, DEFAULT_ATOM_TAG_NAMESPACES y la sincronizacion de tag_namespaces/tag_models alrededor de las lineas 159-204) incluye el namespace host, no jerarquico, aplicable a TaskDoc, con meaning 'maquina donde se ejecuta y valida la tarea', valores documentados host:local y host:robocop2, use_when y do_not_use_when (no se usa en atoms ni pills). Tras `deskops desk update --apply` en el desk de deskops, `deskops edit task <id> tags '["workspace:desk","artifact:task","host:robocop2"]'` no produce alertas de tag en `sldb stores check`.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/atom_tags.py, la semilla de desk que la usa, docs/workflow-policy-reference.md (una linea que explique el tag host) y un test nuevo o ampliado en tests/ (buscar el test actual de tag namespaces con `grep -rln tag_namespaces tests/`). No entra: taggear las tareas existentes (lo hace cada coordinador despues), restringir valores si sldb no soporta enumeraciones (se documentan).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer deskops/atom_tags.py completo y sldb docs/architecture/tags.md. 2) Agregar host a la semilla con tag_models que incluya TaskDoc. 3) Test: desk sandbox, desk update --apply, TaskDoc con host:robocop2, `sldb stores check` sin alerta de tag. 4) Aplicar en el desk de deskops y commitear .sldb/store.yaml.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_atom_tags.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_domain_tree.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops desk update --apply --root . && PYTHONPATH=../sldb/src:. ../.venv/bin/python -m sldb stores check --store .sldb (sin alertas de tag por host)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

El store de deskops declara host; una tarea con host:robocop2 no da alertas; el test pasa; la doc lo explica.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-declara-el-namespace-de-tags-host-para-marcar-en-que-maquina-corre-cada-tarea: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

