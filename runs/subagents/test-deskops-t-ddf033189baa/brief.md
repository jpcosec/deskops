# Encargo del tester deskops-t-ddf033189baa (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas código ni tests, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-puente-de-pytest-en-deskops-para-que-un-test-py-corra-una-suite-de-otro-lenguaje-vitest-go-test-y-fa` (contrato: `deskops show task <id> --root .`). Las precisiones del coordinador forman parte del contrato: están en los motivos de los recibos preflight-1 y bundle-1 (desk/reviews/task-puente-de-pytest-en-deskops-para-que-un-test-py-corra-una-suite-de-otro-lenguaje-vitest-go-test-y-fa/) y al final de runs/subagents/exec-deskops-e-edb9213453ab/brief.md.
Entrega del ejecutor: cambios sin commitear en deskops/testing/__init__.py, deskops/testing/foreign_suites.py, tests/test_foreign_suites.py y docs/workflow-policy-reference.md, más su evidencia en runs/subagents/exec-deskops-e-edb9213453ab/ (result-summary.md, validation.log). No confíes en ese resumen: compruébalo.

1. Lee el diff y los archivos nuevos contra el goal, el scope, el implementation_path y el done_when. Revisa:
   - que `git diff` no toque deskops/services/closeout_gates.py ni ningún gate (decisión de JP);
   - el contrato de `run_foreign_suite(command, *, cwd, timeout=None, env=None)`: rc 0 no hace nada; rc != 0, ejecutable inexistente o timeout → pytest.fail con comando, cwd, rc y las últimas 200 líneas por flujo (stdout y luego stderr); un env dado reemplaza el entorno entero; sin shell;
   - las constantes VITEST y GO_TEST;
   - que importar deskops.testing no cargue pytest ni lo meta como dependencia de runtime, y que ningún módulo del CLI lo importe;
   - que la doc explique cómo declara un repo sus tests (tests/test_<suite>_suite.py) y el comando sin entorno Python propio, y que sea correcta;
   - que no haya cambios fuera de scope.
2. Corre tú, de a un archivo y sin lock (`cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`): test_foreign_suites.py, test_closeout_gates.py, test_closeout_test_paths.py.
3. Smoke real: en /dev/shm escribe un test .py que llame `run_foreign_suite(VITEST, cwd="/mnt/ssd/proyectos/SLDB_1/UIs/sldb-ui")` y córrelo con pytest (debe pasar). Haz también un control negativo en una COPIA de sldb-ui en /dev/shm (git archive HEAD + symlink a su node_modules) con un test vitest que falle: el test .py debe fallar y mostrar el resumen de vitest. No escribas en UIs/sldb-ui.
4. Prueba el comando documentado sin venv (uv run --no-project ... --with-editable) apuntando al checkout /mnt/ssd/proyectos/SLDB_1/deskops (el de /mnt/ssd/herramientas/deskops aún no tiene el cambio; eso se espera).
5. No corras la suite completa: la corre el integrador.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-ddf033189baa/ y /dev/shm, y limpia lo tuyo en /dev/shm.

## Evidencia (en runs/subagents/test-deskops-t-ddf033189baa/)

- `validation.log`: cada comando con su salida y rc.
- `verdict.md`: veredicto `APROBADO` o `RECHAZADO`, con hallazgos (archivo:línea) y riesgos.
- Tu última línea en la conversación: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
