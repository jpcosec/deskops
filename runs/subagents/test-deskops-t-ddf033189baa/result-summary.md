# Veredicto del tester deskops-t-ddf033189baa

- task: task-puente-de-pytest-en-deskops-para-que-un-test-py-corra-una-suite-de-otro-lenguaje-vitest-go-test-y-fa
- role: tester (role-deskops-tester), run run-deskops-t-ddf033189baa, agente claude, sesión fresca
- session: scion://agent/deskops-t-ddf033189baa; session_sha256: '' (sin acceso al archivo de sesión)
- Entrega revisada: cambios sin commitear del ejecutor exec-deskops-e-edb9213453ab
- Evidencia: validation.log (este directorio)

## VEREDICTO: APROBADO

## Comprobaciones

| Punto del encargo | Resultado |
|---|---|
| `git diff` no toca `deskops/services/closeout_gates.py` ni ningún gate | OK: diff de `deskops/services` y `pyproject.toml` vacío. Cambios del ejecutor: `deskops/testing/` (nuevo), `tests/test_foreign_suites.py` (nuevo), `docs/workflow-policy-reference.md`. Todos en `files`. Lo de `.sldb/` y `desk/inbox/` es de otras sesiones (nota entrante y el RunDoc de este tester). |
| Contrato de `run_foreign_suite` | OK. `deskops/testing/foreign_suites.py:44-85`: lista de argumentos sin shell (`subprocess.run(argv, ...)`, sin `shell=True`); rc 0 → `None`; rc≠0 (`:83`), `FileNotFoundError` (`:73`, cubre ejecutable y cwd inexistentes), otro `OSError` (`:77`) y `TimeoutExpired` (`:80`) → `pytest.fail(..., pytrace=False)` con texto plano: causa, `command:`, `cwd:`, `--- stdout (last 200 lines) ---` y luego `--- stderr ...` (`:34-41`). `env` reemplaza el entorno entero (`:71`), `None` hereda; `timeout=None` sin límite; `cwd` keyword obligatorio, str o Path (`:62`). |
| Constantes | OK: `VITEST = ["npx","vitest","run"]`, `GO_TEST = ["go","test","./..."]` (`:20-21`). |
| pytest no es dependencia de runtime ni lo carga el import | OK: `import pytest` perezoso (`:59`); `import deskops.testing.foreign_suites` deja `'pytest' in sys.modules == False`; pytest sigue solo en el extra `dev` de pyproject.toml (sin cambios). `grep` de `deskops.testing`/`foreign_suites` en `deskops/` fuera de `deskops/testing/` → vacío: ningún módulo del CLI lo importa. |
| Doc | OK: `docs/workflow-policy-reference.md:113-150`, subsección "Tests evidence from a suite in another language" junto a la evidencia de closeout: regla del gate (fiel a `reference_points_to_test`, `closeout_gates.py:157-190`), contrato, ejemplos `tests/test_vitest_suite.py` y `tests/test_go_suite.py`, comando `uv run --no-project --with pytest --with-editable /mnt/ssd/herramientas/deskops python -m pytest -q tests/test_vitest_suite.py` y aviso de que ese checkout debe incluir `deskops/testing/`. |
| Fuera de scope | Ninguno: sin plugin pytest11, sin comando CLI, sin tests de sldb-ui/marcado-ui/scion, sin tocar pyproject. |

## Validaciones corridas (rc en validation.log)

1. `pytest -q tests/test_foreign_suites.py` → 10 passed, rc 0 (incluye closeout verify sobre bare_desk y store_desk con `tests/test_vitest_suite.py` como evidencia).
2. `pytest -q tests/test_closeout_gates.py` → 5 passed, rc 0.
3. `pytest -q tests/test_closeout_test_paths.py` → 31 passed, rc 0.
4. Smoke real: `/dev/shm/tester-ddf03/smoke/test_vitest_smoke.py` con `run_foreign_suite(VITEST, cwd="/mnt/ssd/proyectos/SLDB_1/UIs/sldb-ui")` → 1 passed, rc 0 (con `PYTHONPATH` al checkout; sin él, el `.venv` compartido resuelve `deskops` editable a `/mnt/ssd/herramientas/deskops`, que todavía no tiene el cambio → ModuleNotFoundError de colección, esperado). `git status` de sldb-ui sin cambios míos.
5. Comando documentado sin venv, en una copia de sldb-ui (git archive HEAD + symlink a node_modules, sin pyproject/venv) con `--with-editable /mnt/ssd/proyectos/SLDB_1/deskops` → 1 passed, rc 0.
6. Control negativo en la copia (`src/zz/fail.test.ts` con `expect(1).toBe(2)`) → rc 1; mensaje: `foreign suite failed: exit code 1`, `command: npx vitest run`, `cwd: /dev/shm/tester-ddf03/copy`, bloques stdout/stderr rotulados, `Test Files 1 failed | 34 passed (35)`, `Tests 1 failed | 219 passed (220)` y el detalle `FAIL src/zz/fail.test.ts > tester negative control`.
7. Sonda extra: timeout=1 sobre un comando que deja un nieto (`sleep 15`) con los pipes heredados → falla a los 1.0 s con `timed out after 1 seconds`; no se cuelga.

No corrí la suite completa (la corre el integrador, según el encargo).

## Riesgos (no bloquean)

- El comando documentado apunta a `/mnt/ssd/herramientas/deskops`; hasta que ese checkout reciba este commit falla con `ModuleNotFoundError: deskops.testing`. Lo mismo el `.venv` compartido de SLDB_1, editable a ese checkout. Los coordinadores de sldb-ui, marcado-ui y scion necesitan ese pull.
- En timeout solo se mata el proceso directo: los nietos (workers de vitest/go) quedan huérfanos hasta terminar solos. Aceptable para el contrato; mejora posible: `start_new_session=True` + `os.killpg`.
- La regla nueva de la doc no tiene átomo propio en `desk/atoms/` (AGENTS.md: átomo antes que doc sustantiva); desk/ quedaba fuera del scope de la tarea. Candidato a tarea de seguimiento.
- Tests faltantes o viejos: ninguno relevante; el caso "cwd inexistente" no tiene test propio pero lo cubre la misma rama `FileNotFoundError`.
