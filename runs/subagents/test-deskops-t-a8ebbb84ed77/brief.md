# Encargo del tester deskops-t-a8ebbb84ed77 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-repo-register-guarda-rutas-relativas-a-la-raiz-del-ecosistema-y-doctor-nombra-las-entradas-del-regis` (contrato: `deskops show task <id> --root .`; las "Precisiones del preflight 1" del scope son parte del contrato).
Entrega del ejecutor: cambios sin commitear en deskops/cli/commands/repo.py, deskops/doc_access.py, deskops/cli/commands/doctor.py y tests/test_registry_robustness.py, más su evidencia en runs/subagents/exec-deskops-e-ae9a07e468ed/.

1. Lee el diff contra el contrato: repo register guarda la ruta relativa a la raíz del repo que contiene el registro; las entradas viejas absolutas o con ~ siguen resolviendo; doctor da una alerta por cada entrada del registro del desk que no resuelve en esta máquina. Juzga el cambio de doc_access.repository_root (ahora expande ~ vía resolve_registered_root): ¿cambia algo para los lectores actuales del registro (message send --to, evidencia <repo-id>:<sha> de closeout_gates)?
2. Corre tú, de a un archivo, sin lock y con PYTHONPATH al checkout: test_registry_robustness.py, test_repo_identity.py, test_message_ecosystem_registry.py, test_doctor_alerts.py, test_closeout_gates.py, test_closeout_resolved_by.py, test_closeout_resolved_by_xrepo.py.
3. Solo lectura sobre el registro real: `deskops doctor --root .` con PYTHONPATH al checkout; anota qué entradas de desk/registry alerta y si es correcto (¿existen esas rutas?). NO escribas en desk/registry ni en ~/setup/desk/registry.
4. Reproducción: los tests nuevos fallan con el código de HEAD (copia en /dev/shm).
5. NO corras la suite completa.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-a8ebbb84ed77/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-a8ebbb84ed77/)

`validation.log` y `verdict.md` (APROBADO o RECHAZADO con hallazgos archivo:línea y riesgos). Tu última línea: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
