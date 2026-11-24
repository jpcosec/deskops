---
sldb:
  by: agent
  at: '2026-11-24T18:27:55Z'
  authority: generated
  via: save_document_payload
id: task-el-runner-de-revisiones-lanza-al-revisor-con-stdin-devnull-cuando-la-entrada-va-por-archivo
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-224522-suggestion-review-preflight-bundle-se-cuelga-con-el-stdin-abierto-pi-print-espera-reportado-por-mepu.md
depends_on: []
pills: []
files:
- deskops/services/review.py
- tests/test_review_command.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El runner de revisiones lanza al revisor con stdin DEVNULL cuando la entrada va por archivo

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261122-224522 (reenviada desde mepu, nota 20261114-091248): el 14-11 varias revisiones de mepu (Q15b1, Q15c, Q16) terminaron en technical_failure por "timeout after 900s/1800s" con salida vacía; el mismo argv a mano responde en 14 s y deskops review bundle con </dev/null terminó en 28 s. Sigue igual en origin/main a7694665: deskops/services/review.py línea 592 llama subprocess.run(argv, input=command["stdin"], ...) y, cuando la entrega es por archivo, command["stdin"] es None (línea 272), así que el revisor hereda el stdin y pi --print queda esperándolo en segundo plano.

## Goal

_Describe the concrete result this task must produce._

Cuando command["stdin"] es None, subprocess.run recibe stdin=subprocess.DEVNULL (y no input); cuando hay entrada por stdin, se sigue pasando por input como hoy.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/review.py (alrededor de la línea 592) y tests/test_review_command.py. No entra: los timeouts, el engine de review, el manifest.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test en tests/test_review_command.py: test_file_delivery_runs_reviewer_with_stdin_devnull, con un revisor falso que lee su stdin (cat) y un stdin del proceso de test que no se cierra (por ejemplo un pipe abierto puesto en sys.stdin/fd 0 con monkeypatch): sin el arreglo se cuelga hasta un timeout corto de 5 s; con el arreglo termina enseguida y con salida. p2: implementar. p3: suite con -n 4. p4: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

El test nuevo pasa (falla con timeout sin el arreglo) y los tests existentes de tests/test_review_command.py siguen verdes.
