FALLA

# Tester: task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale

- Run: `exec-deskops-t-ff772f6d16de-testing`
- Executor commit: `8c58e3387b59f9f930240e6734245d2431d4eef3` (`runtime template: scion-env.yaml con --config y roles de hijos configurables`)
- Veredicto: **FALLA**. Los tests nuevos pasan, pero la implementacion no cumple el Goal completo ni las resoluciones del bundle aceptado (`desk/reviews/task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale/bundle-1.md`).

## Validaciones ejecutadas

El `../.venv/bin/python` del repo no puede correr pytest en este host (`No module named pytest`: el enlace apunta a Python 3.11 y sus site-packages son de 3.12). Use el Python 3.13 del venv de IR con el `PYTHONPATH` del workspace; no es una falla del cambio.

- `TMPDIR=/tmp .../IR/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py` -> **50 passed**
- `... tests/test_runtime_profiles.py` -> **12 passed**
- `... tests/test_output_goldens.py` -> **7 passed** (401 s)
- `... tests/test_command_registry.py` -> **3 passed**

No se corrio la suite completa, segun el encargo de tester.

## Lo que si cumple

- `scion-agent.yaml` ya no recibe `resources` ni `volumes`; ambos salen en `scion-env.yaml`, junto al template, y el archivo se reescribe o se elimina si queda vacio.
- `scion_start_argv` acepta `env_config` y agrega `--config`; el `agents.md` del coordinador incluye `--config "$RUN_DIR/scion-template/scion-env.yaml"` y `--config "$TEST_RUN/scion-template/scion-env.yaml"`.
- `--executor-role` / `--tester-role` existen, tienen los defaults `role-deskops-executor` / `role-deskops-tester`, y el `--type` del hijo sale sin el prefijo `role-` (`role-ir-executor` -> `ir-executor`).
- El golden `tests/fixtures/golden/help/deskops_runtime_template.txt` esta actualizado.

## Fallas encontradas

1. **No se pueden escribir `image`, `kubernetes` ni `telemetry` en `scion-env.yaml`.** El Goal pide esas cinco claves (las presentes) y la resolucion 4 del bundle aceptado pide agregarlas a `SCION_CONTEXT_OPTIONAL_KEYS` y pasarlas tal cual. `SCION_CONTEXT_OPTIONAL_KEYS` solo tiene `memory_limit`, `cpu_limit`, `shared_paths` y `env`; `ENV_CONFIG_KEYS` se declara pero no se usa.
   Reproduccion: un contexto valido con `image`, `kubernetes` y `telemetry` termina en
   `ValueError: Scion context has unknown key(s): image, kubernetes, telemetry`.
   Por lo tanto hoy solo se materializan `resources` y `volumes`. Los tests nuevos tampoco cubren esas tres claves.

2. **Orden de `--config` distinto al resolucion 2 del bundle aceptado.** Se pidio `--config`, RUTA justo despues de `--workspace`; el argv actual lo pone despues de `--harness-auth` y `--non-interactive`.
   Reproduccion: `--workspace` esta en el indice 8 y `--config` en el 13. El test nuevo solo verifica que `--config` exista, no su posicion. Ademas el parametro nuevo se llama `env_config`, mientras la resolucion pide `config`; el efecto funcional es el mismo, pero la firma no coincide con la resolucion.

3. **`dispatch start` no usa el `scion-env.yaml` materializado.** El bundle aceptado resolvio que `dispatch start` pase `target / 'scion-env.yaml'`. `deskops/dispatch.py` sigue sin cambios: llama `scion_start_argv(...)` sin `env_config` y luego agrega `role_cfg.env_config` (lineas 526-527). El ejecutor lo declaro fuera de alcance, pero la resolucion aceptada lo exige; si el coordinador lo considera fuera del contrato de esta tarea, debe resolverlo aparte antes de cerrar.

## Veredicto y siguiente paso

Los cuatro casos del paso 5 pasan, pero no prueban el contrato completo: falta el pass-through de `image`/`kubernetes`/`telemetry`, el orden de argv y el uso del env config generado por dispatch. Se requiere una correccion acotada del ejecutor y un tester fresco; no corresponde cerrar esta tarea.
