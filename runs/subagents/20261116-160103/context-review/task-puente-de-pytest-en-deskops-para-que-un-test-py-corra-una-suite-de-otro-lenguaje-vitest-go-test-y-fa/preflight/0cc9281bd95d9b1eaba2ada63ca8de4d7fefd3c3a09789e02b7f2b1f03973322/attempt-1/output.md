## REFORMULACION
Encargo: crear en el repo `deskops` un puente genérico para que pytest ejecute suites externas (vitest, `go test`) y falle si ellas fallan. Propósito: que el closeout siga exigiendo evidencia `.py` sin cambiar `reference_points_to_test` ni los gates. Resultado: `deskops/testing/foreign_suites.py` con `run_foreign_suite(command, *, cwd, timeout=None, env=None)`, que ejecuta sin shell, no hace nada si rc=0 y llama a `pytest.fail` ante rc≠0, ejecutable inexistente o timeout, nombrando comando, cwd, rc/causa y últimas 200 líneas de stdout/stderr; constantes `VITEST` y `GO_TEST`; `deskops/testing/__init__.py`; tests en `tests/test_foreign_suites.py`; documentación en `docs/workflow-policy-reference.md`. Límites: no tocar gates de closeout, no escribir las suites de sldb-ui/marcado-ui/scion, no evidencia de commits, no plugin `pytest11`, no comando CLI nuevo; `pyproject.toml` solo si hace falta declarar el paquete o pytest como extra.

## AMBIGUEDADES
1. “las ultimas 200 lineas de stdout y stderr” no aclara si son 200 por flujo o 200 combinadas; obligaría a inventar el criterio de truncado y el orden.
2. “el comando exacto para correrlo desde un repo sin entorno Python propio” no da el comando; obligaría a inventar la invocación con `uv`, la ruta al entorno de deskops y el tratamiento de dependencias.
3. “pyproject.toml solo si hace falta declarar el paquete deskops.testing o pytest como extra” deja condicional una decisión de empaquetado; obligaría a inventar cuándo “hace falta” y qué configuración exacta añadir.
4. “comprueba que closeout verify encuentra la evidencia de tests” no especifica el formato mínimo del desk sandbox ni la invocación exacta de verify; obligaría a inventar el montaje del fixture y el comando de verificación.

## DRY-RUN
Un ejecutor futuro leería `deskops/services/closeout_gates.py` (`reference_points_to_test`, `_test_path_candidates`), `pyproject.toml`, la sección de evidencia de tests en `docs/workflow-policy-reference.md`, tests existentes de closeout y la configuración de sldb-ui. Crearía los archivos nuevos y los tests indicados; ajustaría la doc; solo tocaría `pyproject.toml` si la lectura lo exige. Dependencias: `pytest`, `subprocess`, `npx vitest` disponible en sldb-ui. Validaría con los comandos pytest listados, el smoke contra `UIs/sldb-ui`, la suite completa con `-n 4` y comparación de fallas en worktree limpio de `origin/main`. No se ejecuta nada aquí.

## FUTURO
Quedan fuera: que los coordinadores escriban `tests/test_<suite>_suite.py` en cada repo; la evidencia de commit de otro repo; y la decisión humana sobre fallas preexistentes o sobre el resultado real del smoke si el entorno no tiene vitest.
