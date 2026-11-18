REFORMULACION
Nodo ejecutable `task.code`, no agregado. Propósito: evitar que un ejecutor bloqueado deje la tarea en `ritual-testing` y habilitar la vuelta manual `ritual-testing`→`ritual-execution`. Resultado: transición `task_returns_to_execution` (status `active`) usada solo con `advance task --back --reason <texto>`, guardando el motivo en `history`; plantilla `agents.md` del modo executor que prohíbe `advance task` si termina bloqueado o sin cambios, exige escribir `result-summary.md` y cerrar con `sciontool status blocked "<motivo>"`; tests y manual. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops` (implícito por cwd y rutas `deskops/...`). Límites: tocar siembra lifecycle, `advance_task` en `deskops/services/tasks.py`, `deskops/cli/registry.py`, `_render_agents_md` en `deskops/runtime/scion.py`, tests y manual; fuera aplicar a desks reales; checkout principal, sin worktree/rama ni git add/commit.

AMBIGUEDADES
1. «el modulo que escribe las RelationDoc de `desk/lifecycle`»: no da ruta ni nombre; obliga a inventar el archivo exacto.
2. «opcion nueva `--back` acompanada de `--reason <texto>`»: no define qué ocurre si falta, está vacío o `--back` va solo; obliga a inventar validación y código de salida.
3. «el motivo queda en history de la tarea»: no fija forma del registro; obliga a inventar campos.
4. «tests y manual»: no identifica archivo ni ubicación del manual; obliga a inventar destino.

DRY-RUN
Sin ejecutar: leer TaskDoc y átomos; localizar siembra lifecycle, `advance_task`, CLI y `_render_agents_md`; revisar tests existentes. Cambios previstos: añadir transición, opción/validación y registro en history; actualizar plantilla; añadir tests y manual. Dependencias: estructuras actuales de lifecycle, `advance_task`, CLI y plantilla; átomo de tests con sandbox de desks. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/test_lifecycle_graph.py tests/test_scion_runtime.py`; prueba manual en desk desechable: vuelta con `--back --reason`, avance normal sin `--back` sin cambio, y regla en `agents.md`.

FUTURO
El ejecutor futuro implementa y entrega; el revisor/aceptador valida. Un humano u otro nodo decide y ejecuta `deskops desk update --apply` en desks reales; también decide la aceptación del manual y el cierre.
