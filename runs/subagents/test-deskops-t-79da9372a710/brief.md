# Encargo del tester deskops-t-79da9372a710 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas código ni tests, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi` (contrato: `deskops show task <id> --root .`). Las precisiones del coordinador de los motivos de los recibos preflight-1 y bundle-1 (desk/reviews/task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi/) son parte del contrato.
Entrega del ejecutor: cambios sin commitear en deskops/services/closeout_gates.py, deskops/services/closure.py, docs/workflow-policy-reference.md, tests/test_closeout_gates.py y tests/test_closeout_resolved_by.py, más su evidencia en runs/subagents/exec-deskops-e-560a883f4c96/ (result-summary.md, validation.log). No confíes en ese resumen: compruébalo.

1. Lee el diff contra el goal, el scope, el implementation_path y el done_when. Revisa:
   - orden de resolución: registro del desk primero y, si no está, el registro del ecosistema (DESKOPS_ECOSYSTEM_REGISTRY o ~/setup/desk/registry); el local gana;
   - criterio de alcanzable reutilizado (reference_points_to_commit sobre la raíz del otro repo), no duplicado;
   - que una referencia que no resuelve (id desconocido, ambiguo, sha inexistente, root ausente) no cuente y no lance excepción;
   - resolved-by: solo --ref usa el ecosistema; --test queda igual;
   - DECISIÓN DE JP: el gate de tests NO cambia (qué evidencia de tests cuenta). Comprueba que el cambio a closeout_reference_evidence (parámetro points_to_commit opcional) no altera el resultado del gate de tests;
   - que los tests usen un registro sandbox y nunca escriban en ~/setup/desk/registry;
   - nada fuera de scope.
2. Juzga los riesgos que el ejecutor anota en result-summary.md: verify lee el registro real en solo lectura para prefijos desconocidos; un prefijo igual a project_identity ahora cuenta como commit local; un id repetido en el ecosistema invalida todo el ecosistema.
3. Corre tú, de a un archivo y sin lock (`cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`): test_closeout_gates.py, test_closeout_resolved_by.py, test_closeout_resolved_by_xrepo.py, test_closeout_test_paths.py, test_foreign_suites.py, test_message_ecosystem_registry.py.
4. Reproducción: confirma que los tests nuevos fallan con el código de HEAD, en una copia temporal en /dev/shm (git archive HEAD más los tests nuevos); no toques el checkout.
5. Caso real (solo lectura): en un desk sandbox en /dev/shm, una tarea con references a un sha real de otro repo del ecosistema que el sandbox no tenga en su desk/registry (por ejemplo sldb:<sha de su HEAD>, con el registro real del ecosistema): verify lo cuenta como commit.
6. NO corras la suite completa ni stores build --check (orden del integrador wA:p1).

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, escribir en ~/setup/desk/registry, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-79da9372a710/ y /dev/shm, y limpia lo tuyo en /dev/shm.

## Evidencia (en runs/subagents/test-deskops-t-79da9372a710/)

- `validation.log`: cada comando con su salida y rc.
- `verdict.md`: veredicto `APROBADO` o `RECHAZADO`, con hallazgos (archivo:línea) y riesgos.
- Tu última línea en la conversación: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
