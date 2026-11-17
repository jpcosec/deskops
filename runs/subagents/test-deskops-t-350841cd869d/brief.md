# Encargo del tester deskops-t-350841cd869d (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-retirar-el-alias-deskops-inbox-docs-y-skills-pasan-a-deskops-message-y-se-borra-el-alias` (contrato: `deskops show task <id> --root .`; las "Precisiones del preflight 1" del scope son parte del contrato).
Entrega del ejecutor: los cambios sin commitear de `git status` en deskops/, docs/, README.md, .claude/skills/deskops-workflow/ y tests/ (incluye goldens borrados y regenerados), más su evidencia en runs/subagents/exec-deskops-e-d5d217748798/ (result-summary.md, validation.log). El coordinador autorizó tocar los tests y goldens que rompía la eliminación del comando.

1. Lee todo el diff contra el goal, el scope y el done_when. Revisa:
   - que `deskops inbox` desaparece del CLI (invalid choice, rc 2) y que cada uso documentado pasa a `deskops message send|list|read|ack` con flags equivalentes y reales (compáralos con `deskops message <sub> --help`);
   - que los tests migrados conservan sus aserciones (mismo contrato con message) y que no se borró cobertura sin equivalente (el ejecutor dice que el caso de message send --to ya existía: compruébalo);
   - que no quedó ningún golden reescrito de más (corrió --update-golden y restauró varios): `git status tests/fixtures` solo debe mostrar los inbox borrados y help/deskops.txt.
2. Corre tú, de a un archivo, sin lock y con PYTHONPATH al checkout (`cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`): test_message_cli.py, test_message_delivery.py, test_output_goldens.py, test_skill_cli_drift.py, test_cli_grammar.py, test_command_registry.py, test_inbox_promote_cli_gaps.py, test_cli.py, test_cli_help_examples.py.
3. `grep -rnw 'deskops inbox' docs .claude .opencode deskops README.md AGENTS.md tests`: cada coincidencia que quede es histórica o está en la lista de pendientes del ejecutor. Juzga si el escenario e2e tests/e2e_agent/scenarios/inbox-to-task.yaml queda roto o solo cae a su rama || (no lo corras si lanza un agente).
4. NO corras la suite completa ni stores build --check.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, `--update-golden`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-350841cd869d/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-350841cd869d/)

`validation.log` y `verdict.md` (APROBADO o RECHAZADO con hallazgos archivo:línea y riesgos). Tu última línea: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
