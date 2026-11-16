# Encargo del tester deskops-t-64f1e63a41b3 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-deskops-atoms-citations-queda-declarado-como-comando-que-modifica-en-el-test-del-registro-de-comando` (contrato: `deskops show task <id> --root .`; precisiones en el motivo del recibo bundle-1 en desk/reviews/task-deskops-atoms-citations-queda-declarado-como-comando-que-modifica-en-el-test-del-registro-de-comando/).
Entrega del ejecutor: un cambio sin commitear en tests/test_command_registry.py, más su evidencia en runs/subagents/exec-deskops-e-8341bcf0ae0b/. Hay otros cambios sin commitear en el checkout (otra tarea: closeout verify --run-dir) que no son de esta entrega.

1. `git diff -- tests/test_command_registry.py`: solo agrega ('atoms', 'citations') a MUTATING_COMMANDS. Confirma en deskops/cli/registry.py que esa entrada declara mutates=True y que el comando de verdad escribe en el desk con --write (lee deskops/services/atoms.py).
2. Corre, sin lock y con PYTHONPATH al checkout: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_command_registry.py` y lo mismo con tests/test_atom_citations.py. Confirma que test_command_registry.py falla con el test de HEAD (copia en /dev/shm).
3. NO corras la suite completa.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-64f1e63a41b3/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-64f1e63a41b3/)

`validation.log` y `verdict.md` (APROBADO o RECHAZADO con hallazgos). Tu última línea: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
