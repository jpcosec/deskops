# Resultado del ejecutor deskops-e-af97f091952a

Tarea: `task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb`

## Precondición sldb
- sldb importado por `../.venv`: `/mnt/ssd/herramientas/sldb/src/sldb` (repo `/mnt/ssd/herramientas/sldb`, HEAD 34b26a50).
- `git -C /mnt/ssd/herramientas/sldb merge-base --is-ancestor 477d1bc0 HEAD` → rc=0: incluye 477d1bc0.

## Línea base (antes del cambio)
`baseline-before.log`: 3 failed, 39 passed sobre los dos archivos; las 3 fallas son exactamente las del Rationale y todas por subject pinneado (`doc:TaskCodeDoc:task-x@sha256:…` vs `doc:TaskCodeDoc:task-x`). Ninguna otra causa.

## Archivos tocados (ambos dentro de `files`)
- `tests/test_review_record.py`
  - `test_subject_is_pinned_and_the_anchor_is_intact`: docstring corregido (sldb pinnea al crear —`create_document`, desde 477d1bc0— y al guardar); la aserción del recibo recién registrado pasa a `re.fullmatch(r"doc:TaskCodeDoc:task-x@sha256:[0-9a-f]{64}", subject)`, igual que la de la línea 266.
  - `test_a_short_selector_keys_and_anchors_receipts_on_the_full_task_id`: las dos aserciones (owner-1 y preflight-1) usan `re.fullmatch(rf"doc:TaskCodeDoc:{re.escape(full)}@sha256:[0-9a-f]{{64}}", …)`, con el id COMPLETO (`full`), no el selector corto.
- `tests/test_review_command.py`
  - `import re` (autorizado en bundle 1).
  - `test_preflight_writes_attempt_evidence_and_receipt`: aserción de subject → fullmatch pinneado.
- No se tocó código de deskops, otros tests ni aserciones que no sean sobre subject.

## Validation (`validation.log`)
- `pytest -q tests/test_review_record.py` → 21 passed, rc=0
- `pytest -q tests/test_review_command.py` → 21 passed, rc=0
- `git diff --stat` de los dos archivos: 2 files changed, 10 insertions(+), 7 deletions(-). El `git diff --stat` completo muestra además cambios previos de otras tareas (atoms citations, .sldb, desk/tasks/Board.md) que no son míos y no toqué.

## Suite completa
No corrida (orden del integrador wA:p1): para el integrador.

## Riesgos
- Ninguno conocido; si se reinstala un sldb anterior a 477d1bc0 estos tests volverían a fallar (esperado).
