# Encargo del tester deskops-t-110c70d3897b (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y` (contrato: `deskops show task <id> --root .`; las "Precisiones del preflight 1" del scope son parte del contrato, incluida la rama "o hay nota a sldb" del done_when).
Entrega del ejecutor: cambios sin commitear en deskops/graph/desk_graph.py, deskops/graph/checks.py, tests/test_graph_checks.py, tests/test_graph_declared_edges.py y tests/test_graph_cli.py (fuera de files), más su evidencia en runs/subagents/exec-deskops-e-c8c3c37097e7/.

1. Lee el diff: H2 usa closed: (predicado de reglas de sldb) con la misma normalización que _frontmatter_status y _closed_issue desaparece; H1 se conserva con su justificación y la nota a sldb existe (/mnt/ssd/proyectos/SLDB_1/sldb/desk/inbox/20261117-080724-*.md, solo lectura). Juzga el cambio en tests/test_graph_cli.py (estado del issue del cuerpo al frontmatter): ¿es un cambio de comportamiento que podría afectar issues reales del drawer que tengan el estado solo en el cuerpo? Mira si hay issues así en desk/drawer/issues.
2. Corre tú, de a un archivo, sin lock y con PYTHONPATH al checkout: test_graph_checks.py, test_graph_declared_edges.py, test_graph_cli.py, test_graph_missing_existing_files.py.
3. `deskops graph missing --root .` con PYTHONPATH al checkout: el mismo conjunto de líneas que runs/subagents/exec-deskops-e-c8c3c37097e7/graph-missing-antes.txt.
4. Reproducción: los tests nuevos fallan con el código de HEAD (copia en /dev/shm).
5. NO corras la suite completa.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-110c70d3897b/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-110c70d3897b/)

`validation.log` y `verdict.md` (APROBADO o RECHAZADO con hallazgos archivo:línea y riesgos). Tu última línea: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
