PASA

# Veredicto: PASA

Commit del ejecutor: `5f8e878f129103e3bdbd8f4591431867ec7478b4`
("doctor: detect gitignore variants of old .sldb layout; init checks only existing store")
Trailer presente: `Task-Id: task-doctor-reporta-el-layout-viejo-de-sldb-y-nombra-sldb-stores-migrate-layout-como-remedio`.

## Archivos del commit

- `deskops/sldb_layout.py`
- `deskops/bootstrap.py`
- `deskops/cli/commands/core.py`
- `tests/test_doctor_sldb_layout.py`

Los cambios de README y `.claude/skills/deskops-workflow/SKILL.md` vienen del commit previo
`2373f55d` y siguen presentes en HEAD.

## Comprobaciones de la resolución pedida

1. `.gitignore`: se aceptan las 16 variantes de prefijo (`""`, `/`), nombre (`core`, `runtime`)
   y sufijo (`""`, `/`, `/**`, `/*`). Verificado a nivel de `old_layout_signals` para las 16, y
   la suite parametrizada las prueba end-to-end con `doctor`.
2. `init` en un repo SIN store que solo tiene una línea vieja en `.gitignore`: sale 0 e inicializa
   `.sldb/`. El chequeo está en `SLDBBootstrap.init_local_store` y solo corre si `.sldb` ya existe.
3. Mensaje exacto:
   `old .sldb layout (SEÑALES): run sldb stores migrate-layout --store RUTA`
   con `RUTA` absoluta (`root` se resuelve en `DoctorCLI.run` y `target_path` en `InitCLI`).

## Tests ejecutados

Entorno: el `../.venv` del workspace está roto en este contenedor (apunta a Python 3.12
inexistente). Se creó `/tmp/ws-venv312` con Python 3.12.16 (uv), instalando `sldb` y `deskops`
editables + `pytest` + `pytest-xdist`. Comandos con `TMPDIR=/tmp`.

| Archivo | Resultado |
|---|---|
| `tests/test_doctor_sldb_layout.py` | 24 passed (333 s) |
| `tests/test_doctor_alerts.py` | 5 passed (55 s) |
| `tests/test_gitignore_policy.py` | 2 passed (0.6 s) |
| `tests/test_doctor_model_registration.py` + `tests/test_federated_models.py` (init/bootstrap) | 11 passed (134 s) |
| `tests/test_cli.py` (init/CLI, `-n 4`) | 103 passed (396 s) |

No existen `tests/test_bootstrap.py`, `tests/test_core.py` ni `tests/test_sldb_layout.py`.
No se corrió la suite completa, según la instrucción del tester.

## `deskops doctor --root .`

`deskops doctor --root .` no reporta ningún issue de layout (`grep -i 'migrate-layout|old .sldb layout'`
sin coincidencias). El comando sale 1 por hallazgos preexistentes ajenos a esta tarea (alertas de
review receipts perdidos y rutas de registro inexistentes), no por el layout.

## Conclusión

Las tres correcciones del intento 2 y los criterios de aceptación se cumplen; los tests pasan.
