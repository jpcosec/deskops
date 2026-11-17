# Encargo del tester deskops-t-bfb4a8401ae2 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-deskops-message-ack-acepta-reason-y-la-nota-guarda-el-porque-en-un-campo-ack-reason` (contrato: `deskops show task <id> --root .`; precisiones del coordinador en los motivos de los recibos preflight-1 y bundle-1 de desk/reviews/task-deskops-message-ack-acepta-reason-y-la-nota-guarda-el-porque-en-un-campo-ack-reason/).
Entrega del ejecutor: cambios sin commitear en deskops/models/inbox.py, deskops/cli/registry.py, deskops/cli/commands/message.py, tests/test_message_cli.py, tests/fixtures/model_contract_hashes.json y 10 goldens (help y output), más su evidencia en runs/subagents/exec-deskops-e-e6f5a3ab8886/.

1. Lee el diff contra el contrato: ack --reason guarda ack_reason; sin --reason queda ''; una nota vieja sin el campo se lee como ''; message read lo muestra. Revisa que los goldens tocados sean solo los que cambian por el campo nuevo y que no quedó ningún golden ajeno reescrito o borrado (`git status tests/fixtures`).
2. RIESGO A JUZGAR: el modelo de nota del inbox lo comparten todos los desks (la instalación de deskops es única). Cuando esto llegue a herramientas/deskops, ¿un desk cuyo .sldb tiene el modelo InboxNoteDoc viejo puede recibir, leer y ackear notas nuevas (con ack_reason) y viejas? ¿Qué dice su doctor o stores check? Pruébalo en un sandbox: un desk inicializado con el código de HEAD (modelo viejo) y luego operado con el código del checkout (PYTHONPATH). Di qué tendría que hacer cada desk (por ejemplo sldb stores update) y si es bloqueante.
3. Corre tú, de a un archivo, sin lock y con PYTHONPATH al checkout: test_message_cli.py, test_command_registry.py, test_model_contract_snapshot.py, test_message_delivery.py, test_message_ecosystem_registry.py y, si la carga lo permite, test_output_goldens.py.
4. Reproducción: los tests nuevos fallan con el código de HEAD.
5. NO corras la suite completa.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout` en el checkout, `--autostash`, `--update-golden`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-bfb4a8401ae2/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-bfb4a8401ae2/)

`validation.log` y `verdict.md` con una línea `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>` y hallazgos. Tu última línea en la conversación es esa misma.
