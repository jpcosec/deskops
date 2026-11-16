# Encargo del tester deskops-t-9da54e09a30a (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas código ni tests, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados` (contrato: `deskops show task <id> --root .`). Las precisiones del coordinador de los motivos de los recibos preflight-1 y bundle-1 (desk/reviews/task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados/) son parte del contrato.
Entrega del ejecutor: cambios sin commitear en deskops/graph/desk_graph.py y tests/test_graph_extract_sources.py, más su evidencia en runs/subagents/exec-deskops-e-4ba5a0d9443c/ (result-summary.md, validation.log). No confíes en ese resumen: compruébalo.

1. Lee `git diff -- deskops/graph/desk_graph.py tests/test_graph_extract_sources.py` contra el goal, el scope, el implementation_path y el done_when: la FileRule de spec pasa a path_prefixes ("spec", "docs/architecture"), sin otros cambios en sufijos ni orden; el test nuevo usa un desk sandbox y comprueba file_kind spec para un YAML bajo docs/architecture; nada fuera de scope.
2. Corre tú, de a un archivo y sin lock (`cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`): test_graph_extract_sources.py, test_graph_snapshot.py, test_graph_missing_existing_files.py, test_graph_extract_docs.py, test_graph_checks.py. Y `grep -n spec2viz deskops/graph/desk_graph.py` (debe dar vacío).
3. Reproducción: confirma que el test nuevo falla con el código de HEAD, en una copia temporal en /dev/shm (git archive HEAD más el test nuevo); no toques el checkout.
4. Comprueba que el grafo real de deskops no cambia: `deskops graph missing --root .` sigue en 36 entradas.
5. NO corras la suite completa ni stores build --check (orden del integrador wA:p1).

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-9da54e09a30a/ y /dev/shm, y limpia lo tuyo en /dev/shm.

## Evidencia (en runs/subagents/test-deskops-t-9da54e09a30a/)

- `validation.log`: cada comando con su salida y rc.
- `verdict.md`: veredicto `APROBADO` o `RECHAZADO`, con hallazgos (archivo:línea) y riesgos.
- Tu última línea en la conversación: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
