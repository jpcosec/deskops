REFORMULACION
Nodo ejecutable `task.code`, no agregado. Propósito: que pytest sea la evidencia del closeout aunque la suite real sea vitest o Go, sin cambiar el gate. Resultado: `deskops/testing/foreign_suites.py` con `run_foreign_suite(command, *, cwd, timeout=None, env=None)`, que ejecuta sin shell vía subprocess y llama a `pytest.fail` ante rc≠0, ejecutable ausente o timeout, incluyendo comando, cwd, rc/causa y últimas 200 líneas; ayudas `VITEST` y `GO_TEST`; tests; doc en `docs/workflow-policy-reference.md` con ejemplos y comando. Repo: `deskops`. Límites: no tocar `deskops/services/closeout_gates.py` ni gates, evidencia de commit, suites de otros repos, plugin pytest11 ni CLI; no escribir `tests/test_<suite>_suite.py` en sldb-ui, marcado-ui o scion.

AMBIGUEDADES
1. “las ultimas 200 lineas de stdout y stderr”: no aclara si son 200 por flujo, 200 combinadas o intercaladas. Inventar formato y selección.
2. “Smoke real ... corrido con pytest pasa”: presupone que la suite real de sldb-ui está verde. Si falla, el puente debe fallar; no dice si eso invalida la tarea, se registra rc/salida o se busca otra suite. Inventar el criterio.
3. “el comando exacto para correrlo desde un repo sin entorno Python propio”: solo ejemplifica “por ejemplo con uv y la instalacion de deskops de la maquina”. Inventar invocación, PATH y supuestos de entorno.
4. “pyproject.toml solo si hace falta declarar el paquete deskops.testing o pytest como extra”: no define “hace falta”. Inventar cuándo modificar el empaquetado.
5. “env None hereda el entorno”: no define si un `env` provisto reemplaza o superpone variables. Inventar la semántica.

DRY-RUN
Hipotéticamente: leer `closeout_gates.py` (`reference_points_to_test`, `_test_path_candidates`), `pyproject.toml`, tests existentes y la sección de evidencia de la doc. Crear `deskops/testing/__init__.py`, `foreign_suites.py` y `tests/test_foreign_suites.py` con casos rc0, rc≠0, ejecutable inexistente, timeout, cwd y sandbox desk con `tests/test_vitest_suite.py`; editar la doc; tocar `pyproject.toml` solo si el empaquetado lo exige. Dependencias: pytest/subprocess, `npx`/vitest y `go` para smoke, CLI deskops/sldb para el sandbox. Validaciones futuras: los cinco comandos del TaskDoc, smoke con salida/rc, suite completa y baseline en `git worktree`. Sin ejecutar nada.

FUTURO
El ejecutor implementa y corre validaciones; el Tester independiente valida; el coordinador decide aceptación, informe y evidencia; un humano confirma el smoke real y desvíos. El closeout emitirá recibos y commit.
