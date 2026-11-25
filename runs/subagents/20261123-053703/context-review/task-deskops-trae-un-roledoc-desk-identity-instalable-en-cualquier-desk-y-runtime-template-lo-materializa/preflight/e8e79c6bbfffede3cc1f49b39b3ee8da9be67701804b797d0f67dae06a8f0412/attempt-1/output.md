## REFORMULACION

Encargo ejecutable (task.code): añadir a deskops un RoleDoc `desk-identity` empaquetado como YAML en una carpeta `roles` hermana de `data/templates` (fuera de esta para que `seed_desk` no lo trate como semilla), instalable por `desk update` e `init` sin pisar roles existentes, y un `--mode identity` en `runtime template` que genere un `agents.md` persistente con raíz del desk y proyecto scion, sin worktree ni instrucciones de ejecutor/tester/coordinador. Resultado: dos tests nuevos verdes, goldens de ayuda y scaffold actualizados solo con la opción y el rol, suite completa verde y commit con trailer `Task-Id`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no crear el agente en scion, no hook, no tocar repo scion, no mapa de propiedad, no traducción de tools (es dependencia).

## AMBIGUEDADES

1. «nombra la raiz del desk y el proyecto scion» — no se define de dónde sale el nombre del proyecto scion (`_example_roots` se cita solo para la raíz); obligaría a inventar la fuente del dato.
2. «deskops runtime template desk-identity --mode identity» — no se especifica qué es el posicional `desk-identity` ni si el modo identity lo consume; obligaría a inventar el contrato del argumento.
3. «workspace relativo ... el unico modo que admite reincarnate» — afirmación sobre scion no verificable con el input; obligaría a inventar/verificar ese comportamiento.

## DRY-RUN

Lecturas: `pyproject.toml`, `deskops/cli/commands/desk.py`, `core.py`, `runtime/scion.py` (selección líneas 495-504, `_example_roots` 508, ValueError 384), `cli/registry.py`, `cli/commands/runtime.py`, tests `test_desk_sync.py`, `test_scion_runtime.py` y goldens citados. Cambios previstos: YAML del rol + `package-data`; función compartida de instalación idempotente; rama identity con `_render_identity_agents_md`; choices de `--mode`; tests; regeneración de goldens vía pytest con `--update-golden`; commit selectivo. Dependencias: `task-el-runtime-profile-traduce-los-tools...`. Validaciones futuras: los cuatro comandos pytest de la sección Validation, revisión del diff de goldens y comprobación de `deskops init` → «Desk is up to date».

## FUTURO

Otro nodo completa la traducción de tools a claude (dependencia) y el hook que despierta al agente; creación del agente en scion queda fuera. Un humano revisa el diff de goldens y mergea el commit; el push está prohibido al ejecutor.
