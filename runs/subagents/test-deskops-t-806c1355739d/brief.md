# Encargo del tester deskops-t-806c1355739d (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas código, tests ni desk/, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-deskops-review-puede-correr-con-un-runtimeprofiledoc-de-claude-cuando-pi-no-esta-disponible` (contrato: `deskops show task <id> --root .`; las "Precisiones del preflight 1" del scope son parte del contrato).
Entrega del ejecutor: cambios sin commitear en deskops/services/review.py y tests/test_review_command.py, más su evidencia en runs/subagents/exec-deskops-e-2ea9647a5250/ (result-summary.md, validation.log, manual-run/).

1. Lee el diff contra el goal, el scope, el implementation_path y el done_when: la rama claude (argv con -p, modelo del perfil, --system-prompt, flags de aislamiento, input por stdin y nunca como @ruta), la rama pi sin cambios, el default sigue siendo runtime-pi-deepseek-flash, y el manifest registra binario, modelo, entrega del input y aislamiento.
2. Aislamiento: comprueba tú, con `claude --help`, que cada flag de CLAUDE_ISOLATION existe en el claude instalado. Juzga si el aislamiento cumple lo que pide el contrato (que el revisor no vea el CLAUDE.md, la memoria ni los tools del usuario).
3. Juzga el rechazo de un perfil claude sin --model, y la recomendación del ejecutor de no editar runtime-claude del desk real y crear en su lugar un perfil aparte para el revisor.
4. Corre tú, sin lock y con PYTHONPATH al checkout: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py`, y lo mismo con tests/test_review_doc.py, tests/test_review_record.py y tests/test_command_registry.py. Confirma que los tests nuevos fallan con el código de HEAD (copia en /dev/shm).
5. Una corrida real corta en un desk sandbox en /dev/shm (git init + deskops init, perfil claude con --model haiku creado por CLI en el sandbox): `deskops review preflight <tarea del sandbox> --engine <perfil> --root .` con PYTHONPATH al checkout. Comprueba manifest y receipt. Una sola corrida, con haiku. No toques el desk real.
6. NO corras la suite completa ni stores build --check.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-806c1355739d/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-806c1355739d/)

`validation.log` y `verdict.md` (APROBADO o RECHAZADO con hallazgos archivo:línea y riesgos). Tu última línea: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
