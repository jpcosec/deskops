# Resultado del ejecutor deskops-e-3cd90f55821f

- run_id: run-deskops-e-3cd90f55821f
- task: task-closeout-commit-no-amienda-un-commit-que-la-tarea-cita-como-evidencia-de-commit
- session: scion://agent/deskops-e-3cd90f55821f (sesión claude; sin archivo de transcript local)
- session_sha256: '' (no disponible desde dentro de la sesión)

## Cambios (todos dentro de `files`)

- `deskops/services/closure.py`
  - `_close`: antes de borrar la tarea lee sus citas de commit (`_cited_commit_evidence`). La rama de amend
    (`head_task_id == task_id and head_mode != "record"`) ahora además exige `not self._head_is_cited(...)`;
    si el HEAD está citado, el cierre es `git commit -m <mensaje>` (commit nuevo). Lo demás no cambia: el amend
    del índice de runs (index.jsonl) sobre el propio commit de cierre, los trailers y los otros modos.
  - `_cited_commit_evidence(task_id, task_path)`: items de `references` que son hex en minúsculas de 7+
    caracteres, y los `value` de los recibos `desk/reviews/<tarea>/evidence-commit-*.md` (ReviewDoc kind
    evidence, fact commit) con `verdict: accepted`. No mira history ni el cuerpo (precisión bundle 1, (5)).
  - `_head_is_cited`: `rev-parse HEAD` empieza con algún item de references, o es igual a un value de recibo.
- `tests/test_closeout.py`: dos tests nuevos (el primero parametrizado) más dos helpers:
  - `test_closeout_commit_does_not_amend_a_head_the_task_cites_as_commit_evidence[reference|receipt]`:
    commit de código con trailer `Task-Id: task-x`; citado por sha corto (8) en references o por recibo
    evidence-commit aceptado; `closeout verify` y luego `closeout commit --no-run`; el commit de código
    conserva su sha, es `HEAD^` y ancestro de HEAD, y el cierre es un commit aparte.
  - `test_closeout_commit_still_amends_an_uncited_head_with_the_task_id`: HEAD con el Task-Id sin cita
    (solo un recibo `rejected`) se sigue amendando: `HEAD^` es el commit previo y el sha de código ya no es ancestro.
  - Comprobado: con la condición nueva desactivada, los dos casos citados fallan y el no citado pasa.

## Validación (validation.log)

- `pytest -q tests/test_closeout.py`: 62 passed, rc=0
- `pytest -q tests/test_closeout_declared_evidence.py`: 23 passed, rc=0
- Suite completa: no corrida (orden del integrador wA:p1); para el integrador.
- No se tocó el CLI (sin comandos nuevos), así que test_command_registry.py no aplica.

## Decisiones y riesgos

- Valor del recibo: se compara entero por línea. `_evidence_facts` escribe `value` como los shas completos
  unidos por `\n`; con un solo commit esto es exactamente "value entero == sha del HEAD" (precisión preflight
  1, (2)); con varios commits cada línea se compara entera. Si el revisor quiere estrictamente el campo entero,
  basta quitar el `splitlines`.
- Referencias calificadas `<repo-id>:<sha>` no cuentan (no son hex puro), según la precisión (2).
- Si la tarea no existe en disco o no se puede leer, no hay citas y el comportamiento es el de antes.
