# Encargo del tester deskops-t-e83f943bfb0b (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-se-retiran-del-drawer-los-planes-workspace-documental-gates-por-tipo-deskops-ui-y-deskops-como-confi` (contrato: `deskops show task <id> --root .`; precisiones en los motivos de los recibos preflight-1 y bundle-1 de desk/reviews/task-se-retiran-del-drawer-los-planes-workspace-documental-gates-por-tipo-deskops-ui-y-deskops-como-confi/).
Entrega del ejecutor: cambios sin commitear (git rm en el índice de los 4 planes de desk/drawer/plans/ y de desk/drawer/tasks/workspace-documental/, el fixture nuevo tests/fixtures/plans/gates-por-tipo/, y cambios en tests/test_review_command.py, deskops/cli/registry.py, 3 goldens de ayuda de review, docs/operator-manual.md y docs/deskops-ui.md), más su evidencia en runs/subagents/exec-deskops-e-c5247d70fb6a/.

DECISIÓN DEL COORDINADOR sobre el bloqueo que informó el ejecutor: graph missing sube de 35 a 50 por 15 references/files de 8 TaskDocs que citan archivos de los planes borrados. Se acepta como esperado: son referencias de procedencia a archivos retirados que siguen en el historial de git (igual que from_drawer); editarlas dejaría stale recibos viejos y recibos de owner que solo dispone JP. Juzga el done_when con esa decisión: el criterio es que no aparezca ninguna entrada NUEVA que no sea una de esas 15 referencias a archivos de los 4 planes.

1. Lee el diff: el fixture es el mínimo con el que pasan los tests (incluye PC01 y brief.md); los ejemplos de ayuda usan desk/drawer/plans/mi-plan; las docs según las precisiones; los git rm son exactamente los 4 planes y la carpeta de fichas.
2. Corre tú, de a un archivo, sin lock y con PYTHONPATH al checkout: test_review_command.py, test_review_doc.py, test_cli_help_examples.py y, si la carga lo permite, test_output_goldens.py.
3. `deskops graph missing --root .`: compara con runs/subagents/exec-deskops-e-c5247d70fb6a/graph-before.txt; las entradas nuevas son solo las 15 descritas.
4. `grep -rn "drawer/plans/\(gates-por-tipo\|deskops-ui\|deskops-como-config\|workspace-documental\)" deskops tests docs README.md AGENTS.md .claude`: solo quedan literales de validación de test_review_doc.py y rutas dentro del sandbox de test_review_command.py.
5. NO corras la suite completa.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git rm`, `git commit`, `git push`, `git stash`, `git checkout`, `git restore`, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-e83f943bfb0b/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-e83f943bfb0b/)

`validation.log` y `verdict.md` (APROBADO o RECHAZADO con hallazgos). Tu última línea: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
