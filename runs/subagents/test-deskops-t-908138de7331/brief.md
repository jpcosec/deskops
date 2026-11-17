# Encargo del tester deskops-t-908138de7331 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-review-status-compara-el-contrato-del-taskdoc-y-no-su-texto-entero-igual-que-el-anchor-state-de-la-r` (contrato: `deskops show task <id> --root .`; precisiones del coordinador en los motivos de los recibos preflight-3 y bundle-3 de desk/reviews/task-review-status-compara-el-contrato-del-taskdoc-y-no-su-texto-entero-igual-que-el-anchor-state-de-la-r/).
Entrega del ejecutor: cambios sin commitear en deskops/services/review.py, deskops/models/review.py, tests/test_review_command.py y tests/fixtures/model_contract_hashes.json, más su evidencia en runs/subagents/exec-deskops-e-289fe7bfa1df/.

1. Lee el diff contra el contrato y las precisiones: reutiliza task_contract_sha256; el ReviewDoc nuevo guarda contract_sha256; el estado de un recibo con ese campo depende del contrato (y en bundle de las demás fuentes), no de tags/status/history ni de la cabecera sldb; los recibos viejos sin el campo siguen como hoy; input.md e input_sha256 no cambian; la agregación no cambia.
2. Juzga si actualizar tests/fixtures/model_contract_hashes.json (fuera de files) era necesario y si el valor nuevo es el correcto.
3. Corre tú, de a un archivo, sin lock y con PYTHONPATH al checkout (`cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`): test_review_command.py, test_review_doc.py, test_review_record.py, test_model_contract_snapshot.py, test_activation_rules.py, test_closeout_evidence_receipts.py.
4. Reproducción: el test de tags y status falla con el código de HEAD (copia en /dev/shm).
5. Caso real en sandbox (/dev/shm, git init + deskops init con PYTHONPATH al checkout y el pi falso o un recibo de prueba): una tarea con preflight aceptado escrito por el código nuevo; deskops edit task <t> tags '[...]'; deskops review status sigue accepted; editar goal lo deja stale.
6. NO corras la suite completa ni stores build --check.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout` en el checkout, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-908138de7331/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-908138de7331/)

`validation.log` y `verdict.md` (APROBADO o RECHAZADO con hallazgos archivo:línea y riesgos). Tu última línea: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
