PASA

# Resultado del tester

Tarea: task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale
Run: run-deskops-t-ff772f6d16de-a2

## Commits evaluados

Ambos commits llevan el trailer `Task-Id` correcto y son ancestros del HEAD actual:

- `8c58e3387b59f9f930240e6734245d2431d4eef3` — "runtime template: scion-env.yaml con --config y roles de hijos configurables"
  - `deskops/runtime/scion.py`, `deskops/cli/commands/runtime.py`, `deskops/cli/registry.py`,
    `tests/fixtures/golden/help/deskops_runtime_template.txt`, `tests/test_scion_runtime.py`
- `1858aca9036f7fab82df93d841850db70aa9ac06` — "runtime template: image/kubernetes/telemetry a scion-env.yaml, --config tras --workspace, dispatch usa scion-env.yaml"
  - `deskops/runtime/scion.py`, `deskops/dispatch.py`, `tests/test_scion_runtime.py`, `tests/test_dispatch.py`

## Pruebas ejecutadas (de a uno, con `TMPDIR=/tmp`)

Nota de entorno: el `../.venv` del proyecto apunta a un intérprete Python 3.12 ausente en este host
(`python3` local es 3.11 y ese venv es 3.12), por lo que no puede importar pytest. Se usó el venv de
pruebas disponible `/dev/shm/deskops-test-venv/bin/python` (Python 3.12.16, pytest 9.2.0, `deskops`
y `structuredlanguagedb` en modo editable). No se modificó ningún archivo del repositorio.

- `tests/test_scion_runtime.py` -> **51 passed** (incluye los tests nuevos de scion-env, `--config` y roles).
- `tests/test_dispatch.py` -> **49 passed** (incluye `scion-env.yaml` materializado y `--config` en el argv).
- `tests/test_output_goldens.py` -> **7 passed** (incluye `help/deskops_runtime_template.txt` con los flags nuevos).
- `tests/test_runtime_profiles.py` -> **12 passed**.
- `tests/test_command_registry.py tests/test_cli_help_examples.py` -> **16 passed**.
- `tests/test_role_runtime_artifacts.py` -> **3 passed**.
- `tests/test_registry_robustness.py` -> **8 passed**.

No se ejecutó la suite completa (la integra el host).

## Comprobaciones contra el Goal

1. Se generó un template real por CLI con contexto que trae `image`, `resources`, `volumes`,
   `kubernetes` y `telemetry`:
   - `scion-env.yaml` queda en el mismo directorio que `scion-agent.yaml` y contiene exactamente
     esas claves de primer nivel (`image`, `volumes`, `resources`, `kubernetes`, `telemetry`).
   - `scion-agent.yaml` ya no contiene ninguna de esas cinco claves (conserva `env`, que es otra cosa).
2. Una segunda corrida con otros límites (`4Gi`/`1` CPU) y sin imagen/kubernetes/telemetry
   sobrescribe `scion-env.yaml`: los límites cambian y las claves ausentes desaparecen.
3. `scion_start_argv` coloca `--config <ruta>` inmediatamente después de `--workspace <ruta>` y solo
   cuando se le pasa la ruta; `dispatch start` usa el `scion-env.yaml` materializado.
4. El `agents.md` del coordinador, generado con `--executor-role role-ir-executor
   --tester-role role-ir-tester`, usa los ids completos en los comandos `runtime template`, deriva
   `--type ir-executor` / `--type ir-tester`, y agrega
   `--config "$RUN_DIR/scion-template/scion-env.yaml"` y
   `--config "$TEST_RUN/scion-template/scion-env.yaml"` al lanzar cada hijo.
   Con los defaults sigue produciendo `--type deskops-executor` y `--type deskops-tester`.
5. La ayuda de `deskops runtime template` incluye `--executor-role` y `--tester-role` con los
   defaults `role-deskops-executor` / `role-deskops-tester`, y el golden coincide.

Veredicto: **PASA**.
