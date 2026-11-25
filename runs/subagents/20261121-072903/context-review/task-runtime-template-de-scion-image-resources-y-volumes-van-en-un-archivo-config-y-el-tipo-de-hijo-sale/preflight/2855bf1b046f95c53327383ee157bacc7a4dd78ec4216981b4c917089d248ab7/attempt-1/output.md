REFORMULACION
Propósito: corregir `deskops runtime template` para que image, resources, volumes, kubernetes y telemetry se escriban en `scion-env.yaml`, no en `scion-agent.yaml`; que `scion_start_argv` pase `--config <ruta>`; y que los roles del coordinador sean configurables. Resultado: template separado, argv con `--config`, `agents.md` con roles/`--type` derivados, flags `--executor-role`/`--tester-role` y tests/goldens actualizados. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`; superficie: `deskops/runtime/scion.py` (líneas citadas), `deskops/cli/commands/runtime.py`, `tests/test_scion_runtime.py` y goldens de ayuda. Límites: no tocar repo scion, no lanzar scion real, no cambiar imagen ni engine de review.

AMBIGUEDADES
1. Contradicción del prefijo de rol: “reciben un id de RoleDoc completo (con prefijo role-)” frente a “con --executor-role ir-executor el agents.md generado nombra ir-executor”. Obliga a inventar si el flag acepta/normaliza ids sin `role-`, si debe rechazarlos, o si el test es errata.
2. “sus goldens de ayuda” y “tests/fixtures/golden (ayuda de runtime template)” no nombran archivos exactos. Obliga a elegir qué fixtures actualizar si la búsqueda no es inequívoca.
3. “scion_start_argv recibe la ruta y agrega --config” no fija posición/orden en argv. Si un test compara argv exacto, obliga a inventar el orden.

DRY-RUN
Un ejecutor futuro leería el TaskDoc, `scion.py`, `runtime.py`, tests y fixtures; separaría claves de entorno; escribiría `scion-env.yaml` junto a `scion-agent.yaml`, sobrescribiéndolo; añadiría `--config` al argv; parametrizaría roles en la plantilla; añadiría flags y tests; actualizaría goldens. Dependencias: helpers YAML y APIs existentes; sin red ni scion real. Validaría con los pytest listados y compararía fallas en worktree limpio de `origin/main`.

FUTURO
Otro nodo ejecuta implementación y tests; un humano decide cómo resolver la contradicción de prefijos y acepta fallas basales; el cierre incluye commit según átomo.
