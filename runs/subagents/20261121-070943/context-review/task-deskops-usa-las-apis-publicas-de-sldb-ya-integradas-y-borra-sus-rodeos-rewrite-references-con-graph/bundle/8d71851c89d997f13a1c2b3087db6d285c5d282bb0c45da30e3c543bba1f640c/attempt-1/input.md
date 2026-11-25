FILE:desk/tasks/task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph.md
---
sldb:
  by: agent
  at: '2026-11-21T06:39:17Z'
  authority: generated
  via: save_document_payload
id: task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-083618-suggestion-referrers-y-rewrite-references-aceptan-graph-excluded-sources-y-no-duplican-menciones-del-frontmatter-h-a-h-c-de-cc35c.md
- desk/inbox/20261116-082230-suggestion-sldb-api-template-anchors-los-p-rrafos-ancla-literales-de-la-plantilla-de-un-modelo-h1-de-placeholder.md
- desk/inbox/20261116-081341-suggestion-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops usa las APIs publicas de sldb ya integradas y borra sus rodeos: rewrite_references con graph y excluded_sources, template_anchors y create_document que pinnea anclas

## Rationale

_Explain why this task exists or the business driver behind it._

Tres notas de sldb (20261116-083618, 20261116-082230, 20261116-081341) avisan APIs nuevas que reemplazan codigo propio de deskops. Verificado hoy en el sldb instalado (/mnt/ssd/herramientas/sldb): sldb.api.rewrite_references acepta graph= y excluded_sources=, sldb.api.referrers acepta graph=, existe sldb.api.template_anchors(model_type), y segun la nota create_document y Transaction.create pinnean con @sha256 los doc: de __doc_anchors__ (tests de sldb tests/api/test_doc_anchors.py::test_create_document_pins_the_anchor_without_a_later_save).

## Goal

_Describe the concrete result this task must produce._

(a) deskops/services/references.py deja de tener _rewrite_mentions y _in_frontmatter (lineas ~143-230) y usa sldb.api.rewrite_references(..., graph=g, excluded_sources=[...]) y referrers(..., graph=g). (b) deskops/doc_access.py template_placeholders (~linea 546) usa sldb.api.template_anchors en vez de AST_Handler().split_nodes + TemplateExtractor().extract_nodes, y el import de TemplateExtractor desaparece si no queda otro uso. (c) deskops/services/closure.py, en los recibos de evidencia (~lineas 1102-1171), deja el rodeo de create + update sin cambios en la misma transaccion y crea el recibo con un solo create, que ya queda pinneado. El comportamiento observable no cambia: los tests existentes pasan sin tocar sus aserciones.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/references.py, deskops/doc_access.py, deskops/services/closure.py y los tests que cubren esos caminos (tests/test_edit_template_placeholder.py, tests/test_closeout_evidence_receipts.py, tests de references/retire). No entra: cambiar sldb; si alguna API no se comporta como dice la nota, se para esa parte y se deja nota a sldb por inbox, las otras partes siguen.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer las firmas con python -c "import inspect, sldb.api as a; print(inspect.signature(a.rewrite_references))" y equivalentes. 2) Reemplazar cada rodeo por la API, de a uno, corriendo los tests del archivo tocado despues de cada uno. 3) Verificar que un recibo de evidencia recien creado tiene subject con @sha256 y anchor_state intact.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_edit_template_placeholder.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_evidence_receipts.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -n -E "_rewrite_mentions|_in_frontmatter|TemplateExtractor" deskops/services/references.py deskops/doc_access.py (sin resultados)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; cada falla se corre igual en un worktree limpio de origin/main y solo se acepta si falla igual ahi, listada en la entrega)

## Done When

_Name the observable condition that makes the task complete._

Los tres rodeos no estan en el codigo (el grep de validation no da nada), los recibos de evidencia se crean con un solo create y quedan pinneados, y la suite completa pasa sin cambiar aserciones existentes.

FILE:instruccion
Cold-bundle de la tarea task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_edit_template_placeholder.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_evidence_receipts.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -n -E "_rewrite_mentions|_in_frontmatter|TemplateExtractor" deskops/services/references.py deskops/doc_access.py (sin resultados)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; cada falla se corre igual en un worktree limpio de origin/main y solo se acepta si falla igual ahi, listada en la entrega)

