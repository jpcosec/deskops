REFORMULACION
Propósito: corregir la cola para que `dispatch-reap` reintente cuando termina en exit 3 (`EXIT_BUSY`) y añadir un comando de deskops que edite trabajos de la cola sin tocar el resto de `desk/config.json`. Resultado: `dispatch-reap` con `retry_exit_codes [3]` en el config por defecto de `deskops init` y en el `desk/config.json` de deskops, aplicado mediante el comando nuevo; el comando `deskops queue job set <trabajo> <campo> <valor> --root .` —o el nombre que encaje con el CLI— valida el JSON y modifica solo ese trabajo. Repo: deskops (CLI `deskops/cli`, config por defecto de init, tests, CHANGELOG y `desk/config.json`). Límites: fuera otros desks (sldb e IR los aplica el coordinador); no editar a mano; commit desde el worktree con trailer `Task-Id`. Este nodo es un TaskDoc de implementación, no un agregado ni paquete; no tiene hijos ni atoms.

AMBIGUEDADES
1. “o el nombre que encaje con el CLI existente”: no fija el nombre ni la jerarquía exacta del comando; obligaría a inventar sintaxis, flags y parseo de valores.
2. “deskops/data o donde se genere”: no identifica la ruta real del config por defecto; obligaría a inventar dónde buscarlo o generarlo.
3. “no toca nada más del archivo”: no define formato, orden de claves ni serialización; obligaría a decidir cómo preservar el resto del JSON.
4. “commit desde el worktree que dispatch te da”: no da ruta ni mecanismo para obtenerlo; obligaría a inventar el flujo de worktree.

DRY-RUN
Lecturas: TaskDoc, código de `deskops/cli` para queue, plantilla/config de init, `desk/config.json`, `tests/test_queue_cli.py`, CHANGELOG. Cambios previstos: tests p1/p2, implementación del comando, actualización del config por defecto, aplicación del comando a `desk/config.json`, CHANGELOG y commit. Dependencias: convenciones del CLI, esquema de config, worktree provisto por dispatch. Validaciones futuras: ejecutar el pytest indicado, comprobar JSON válido y cambio limitado, probar el config de init, suite con `-n 4` y revisar diff/commit. Sin ejecutar nada.

FUTURO
Otro nodo o humano debe proveer el worktree, confirmar el nombre definitivo del comando si no se deduce, aplicar el comando en sldb e IR desde el coordinador y revisar el commit/CHANGELOG.
