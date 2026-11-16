# Encargo del tester deskops-t-b9835a9a1e2c (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb` (contrato: `deskops show task <id> --root .`). Las precisiones del coordinador de los motivos de los recibos preflight-1 y bundle-1 (desk/reviews/task-los-tests-de-review-esperan-el-subject-pinneado-que-ahora-escribe-create-document-de-sldb/) son parte del contrato.
Entrega del ejecutor: cambios sin commitear SOLO en tests/test_review_record.py y tests/test_review_command.py, más su evidencia en runs/subagents/exec-deskops-e-af97f091952a/. Hay otros cambios sin commitear en el checkout (otra tarea: atoms citations, .sldb, Board.md): no son de esta entrega.

1. `git diff -- tests/test_review_record.py tests/test_review_command.py`: solo cambian las aserciones de subject que fallaban (líneas 261, 363, 371 de test_review_record.py y 165 de test_review_command.py en HEAD), el docstring de test_subject_is_pinned_and_the_anchor_is_intact y el import re. Los subjects pasan a re.fullmatch con @sha256:[0-9a-f]{64}; en el test del selector corto el id es el completo (re.escape(full)), no el selector. Nada se debilita más allá de eso (por ejemplo, no se borra una aserción).
2. Confirma que el sldb importado por ../.venv incluye 477d1bc0 (git -C /mnt/ssd/herramientas/sldb merge-base --is-ancestor 477d1bc0 HEAD).
3. Corre tú, de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_record.py` y lo mismo con tests/test_review_command.py: pasan. Confirma con git archive HEAD en una copia de /dev/shm que con los tests de HEAD fallan exactamente esos 3.
4. NO corras la suite completa ni stores build --check.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-b9835a9a1e2c/ y /dev/shm, y limpia lo tuyo en /dev/shm.

## Evidencia (en runs/subagents/test-deskops-t-b9835a9a1e2c/)

- `validation.log`, `verdict.md` (APROBADO o RECHAZADO con hallazgos). Tu última línea: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
