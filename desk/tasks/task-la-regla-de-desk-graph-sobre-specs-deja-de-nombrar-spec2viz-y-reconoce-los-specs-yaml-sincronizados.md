---
sldb:
  by: agent
  at: '2026-11-16T20:07:00Z'
  authority: generated
  via: save_document_payload
id: task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados
status: draft
summary: La FileRule de specs de desk_graph.py reconoce docs/architecture en vez de
  docs/architecture/spec2viz (pedido IR13, decision de JP G7).
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-224757-suggestion-ir13-pide-migrar-las-habilidades-y-el-script-de-deskops-de-spec2viz-a-specir.md
depends_on: []
pills: []
files:
- deskops/graph/desk_graph.py
- tests/test_graph_extract_sources.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# La regla de desk_graph sobre specs deja de nombrar spec2viz y reconoce los specs YAML sincronizados con sldb notations sync

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15 (G7 aceptada y recomendación del coordinador aceptada): el YAML del spec queda subordinado al grafo y spec2viz se archiva cuando specir retirement check salga con 0; deskops/graph/desk_graph.py:75 es la última regla de deskops que espera a G7.

## Goal

_Describe the concrete result this task must produce._

La regla de desk_graph.py reconoce los specs YAML como artefactos de autoría que se sincronizan al store con sldb notations sync, sin nombrar ni depender de spec2viz.

## Scope

_State what is in scope and what is out of scope._

Entra: la FileRule de kind spec en deskops/graph/desk_graph.py (hoy path_prefixes=("spec", "docs/architecture/spec2viz")) y su test en tests/test_graph_extract_sources.py. La regla pasa a path_prefixes=("spec", "docs/architecture"): un YAML de spec en cualquier subdirectorio de docs/architecture es un nodo de file_kind spec, sin nombrar ninguna herramienta; los sufijos (_SPEC: .md, .yaml, .yml) y el orden de las FILE_RULES no cambian. Decision de JP 2026-11-15 (repo IR, documento fuente-de-verdad-del-diagrama de su carpeta de decisiones, punto 4): los specs YAML se quedan como formato de autoria, se validan con sldb y se sincronizan con sldb notations sync --spec; la ruta docs/architecture/spec2viz se renombra o generaliza por pedido al desk de deskops. Sale: las habilidades de agente y el script render_diagram.py del drawer (tarea aparte de IR13), el DocumentSurface de kind spec (directory spec) y cualquier deteccion semantica de si un YAML esta sincronizado con sldb (el reconocimiento es por ruta).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer FILE_RULES y la clasificacion de archivos en deskops/graph/desk_graph.py. 2) Cambiar el path_prefix docs/architecture/spec2viz por docs/architecture. 3) En tests/test_graph_extract_sources.py, sobre un desk sandbox (tmp_path) como los tests existentes de ese archivo: un YAML creado en un subdirectorio de docs/architecture del sandbox se extrae como nodo de kind spec con file_kind spec, y la asercion existente sobre el atom.yaml de la carpeta spec/artifacts sigue en verde. 4) Correr los tests de la Validation.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_extract_sources.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_missing_existing_files.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -n spec2viz deskops/graph/desk_graph.py (sin coincidencias, rc 1)

## Done When

_Name the observable condition that makes the task complete._

grep de spec2viz en deskops/graph/desk_graph.py no da coincidencias, un YAML bajo docs/architecture/ de un desk sandbox se extrae como nodo de file_kind spec y los tres archivos de test de la Validation pasan.
