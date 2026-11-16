# Encargo del tester deskops-t-adb2be97a1a5 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas código ni tests, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-los-selectores-de-deskops-aceptan-una-ruta-desk-y-el-error-explica-que-formas-acepta` (contrato: `deskops show task <id> --root .`; las "Precisiones del preflight 1" son parte del contrato).
Entrega del ejecutor: cambios sin commitear en deskops/desk_paths.py, deskops/doc_access.py, deskops/cli/registry.py, tests/fixtures/golden/help/deskops_edit_task.txt, tests/test_desk_paths.py y tests/test_tracked_selector_resolution.py, más su evidencia en runs/subagents/exec-deskops-e-ac841a0ca757/ (result-summary.md, validation.log). No confíes en ese resumen: compruébalo.

1. Lee `git diff -- <esos 6 archivos>` contra el goal, el scope, el implementation_path y el done_when. Revisa:
   - la normalización de la precisión: '/' → resolve contra la raíz, stem dentro de desk/, error 'el selector apunta fuera de desk/' fuera de desk/;
   - que el error de no encontrado liste las formas aceptadas;
   - que el ejemplo de ayuda use la ruta literal desk/drawer/tasks/<item>.md;
   - que la resolución por fragmento único no haya cambiado;
   - que no haya cambios fuera de scope;
   - si el test existente que se actualizó (igualdad del mensaje) se ajustó legítimamente.
2. Corre tú, de a un archivo y sin lock (`cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`): test_desk_paths.py, test_tracked_selector_resolution.py, test_output_goldens.py, test_cli_help_examples.py, test_cli.py.
3. Reproducción: confirma que los tests nuevos fallan con el código de HEAD. Hazlo en una copia temporal en /dev/shm (p. ej. git archive HEAD más los tests nuevos); no toques el checkout.
4. Comprueba que en el checkout no quedó ningún golden borrado ni reescrito de más: el ejecutor corrió --update-golden y dice que restauró lo que sobraba.
5. No corras la suite completa: la corre el integrador.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, `--update-golden`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-adb2be97a1a5/ y /dev/shm, y limpia lo tuyo en /dev/shm.

## Evidencia (en runs/subagents/test-deskops-t-adb2be97a1a5/)

- `validation.log`: cada comando con su salida y rc.
- `verdict.md`: veredicto `APROBADO` o `RECHAZADO`, con hallazgos (archivo:línea) y riesgos.
- Tu última línea en la conversación: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
