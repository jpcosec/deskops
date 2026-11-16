---
sldb:
  by: agent
  at: '2026-11-16T21:32:42Z'
  authority: generated
  via: create_document
id: task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- tests/test_review_record.py
- tests/test_review_command.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# los tests de review esperan el subject pinneado que ahora escribe create_document de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

sldb 477d1bc0 (closeout aacb03cc, task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload) hizo que create_document pinnee las anclas a documentos (doc:<Modelo>:<id>@sha256:<hash>) igual que save_document_payload. Desde entonces la suite de deskops sobre origin/main da 3 fallas (integrador wA:p1, 2026-11-16): tests/test_review_record.py::test_subject_is_pinned_and_the_anchor_is_intact, tests/test_review_record.py::test_a_short_selector_keys_and_anchors_receipts_on_the_full_task_id y tests/test_review_command.py::test_preflight_writes_attempt_evidence_and_receipt esperan el subject sin pin ('doc:TaskCodeDoc:task-x'). sldb ajusto sus propias expectativas igual (tests/api/test_doc_anchors.py de sldb).

## Goal

_Describe the concrete result this task must produce._

Los tres tests esperan el subject pinneado que escribe hoy create_document al registrar un recibo, y pasan contra el sldb de origin/main; el codigo de deskops no cambia.

## Scope

_State what is in scope and what is out of scope._

Entra: solo las aserciones sobre el campo subject de los recibos (y el docstring que dice que create_document no pinnea) en tests/test_review_record.py y tests/test_review_command.py. Cada aserccion de igualdad exacta con 'doc:TaskCodeDoc:<id>' sobre un recibo recien creado pasa a exigir el valor pinneado con la misma forma que ya usa la aserccion de la linea 266 de tests/test_review_record.py: re.fullmatch(r'doc:TaskCodeDoc:<id>@sha256:[0-9a-f]{64}', subject). El docstring de test_subject_is_pinned_and_the_anchor_is_intact se corrige: sldb pinnea al crear y al guardar. Sale: el codigo de deskops (deskops/), sldb, otros tests y cualquier aserccion que no sea sobre subject. Si un test falla por otra causa, el ejecutor para y lo informa.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr los dos archivos de test y confirmar que fallan solo por el subject sin pin (guardar la salida). 2) Cambiar cada aserccion de subject sin pin por el fullmatch con @sha256:[0-9a-f]{64}; donde el test ya compara con el id completo de la tarea, usar re.escape del valor esperado. 3) Corregir el docstring. 4) Correr la Validation.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_record.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && git diff --stat (solo los dos archivos de test)

## Done When

_Name the observable condition that makes the task complete._

Los dos archivos de test pasan contra el sldb instalado (origin/main con 477d1bc0) y git diff solo toca tests/test_review_record.py y tests/test_review_command.py.
