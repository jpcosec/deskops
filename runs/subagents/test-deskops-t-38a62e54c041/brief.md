# Encargo del tester deskops-t-38a62e54c041 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas código ni tests, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-deskops-atoms-citations-escanea-las-citas-codigo-atomo-reporta-citas-rotas-y-atomos-sin-cita-y-las-l` (contrato: `deskops show task <id> --root .`; las "Precisiones del preflight 1" del scope son parte del contrato).
Entrega del ejecutor: cambios sin commitear en deskops/services/atoms.py, deskops/cli/registry.py, deskops/cli/commands/atoms.py, deskops/cli/commands/operations.py, tests/test_atom_citations.py, tests/fixtures/golden/help/deskops_atoms.txt y tests/fixtures/golden/help/deskops_atoms_citations.txt, más su evidencia en runs/subagents/exec-deskops-e-d62639bcf100/ (result-summary.md, validation.log). No confíes en ese resumen: compruébalo. Ojo: en el checkout hay otros cambios sin commitear (.sldb, desk/tasks/Board.md y una tarea nueva de review); no son de esta entrega.

1. Lee el diff contra el goal, el scope, el implementation_path y el done_when. Revisa la gramática de citas (bloque Atoms: del docstring y comentario # Atom:), el reporte de citas rotas y átomos sin cita, el código de salida de --check, --write idempotente (crea y borra RelationDoc cited_by) y la sección "Cited by:" de show atom. Juzga los 3 archivos tocados fuera de files (registry y goldens de ayuda; commands/atoms.py y commands/operations.py): ¿son necesarios para el contrato?
2. PUNTO CLAVE: el ejecutor informa que sldb no acepta una ruta de archivo como extremo de una RelationDoc: las citas quedan como documentos pero no como aristas del grafo (check_edges da un error por cita tras --write) y show atom las lee de los documentos. Compara eso con el contrato literal (goal, scope y done_when): ¿cumple lo que la tarea pide o deja el store con errores que el contrato no admite? Corre --write en un desk sandbox y mira qué dicen sldb stores check y deskops doctor sobre ese sandbox. Si el contrato pide aristas recorribles o un store sin errores y esto no lo da, es RECHAZADO con ese motivo; si el contrato se cumple y es una limitación de sldb a rutear, APROBADO con el riesgo anotado.
3. Corre tú, de a un archivo y sin lock (`cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`): test_atom_citations.py, test_output_goldens.py, test_cli_help_examples.py, test_graph_checks.py, test_cli.py.
4. Reproducción: confirma que test_atom_citations.py falla con el código de HEAD, en una copia temporal en /dev/shm; no toques el checkout. Comprueba que en el checkout no quedó ningún golden reescrito de más (el ejecutor corrió --update-golden y revirtió 4).
5. Solo lectura en el repo real: `deskops atoms citations --check --root .` (NO --write en el repo real).
6. NO corras la suite completa ni stores build --check (orden del integrador wA:p1).

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, `--update-golden`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-38a62e54c041/ y /dev/shm, y limpia lo tuyo en /dev/shm.

## Evidencia (en runs/subagents/test-deskops-t-38a62e54c041/)

- `validation.log`: cada comando con su salida y rc.
- `verdict.md`: veredicto `APROBADO` o `RECHAZADO`, con hallazgos (archivo:línea) y riesgos.
- Tu última línea en la conversación: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
