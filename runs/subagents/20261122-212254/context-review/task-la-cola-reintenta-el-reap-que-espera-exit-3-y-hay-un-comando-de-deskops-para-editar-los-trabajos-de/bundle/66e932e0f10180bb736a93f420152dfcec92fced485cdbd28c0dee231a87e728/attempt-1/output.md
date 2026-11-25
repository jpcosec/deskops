## REFORMULACION

**Propósito:** que el trabajo `dispatch-reap` reintente cuando sale 3 (EXIT_BUSY: agente vivo o worktree sucio) en vez de acabar en `runs/queue/failed` y trabar la tarea, y dotar al CLI de un modo de editar trabajos de cola sin tocar el JSON a mano.

**Resultado:** (1) `retry_exit_codes [3]` para `dispatch-reap` en el config por defecto de init y en `desk/config.json` de deskops, aplicado con el comando nuevo; (2) comando `deskops queue job set <trabajo> <campo> <valor> --root .` que valida y solo cambia ese trabajo.

**Repo/superficie:** deskops (`deskops/cli`, config por defecto de init, `desk/config.json`, tests, CHANGELOG).

**Límites:** fuera otros desks (sldb e IR), que aplica el coordinador; nada fuera de la cola y el config.

## AMBIGUEDADES

1. "deskops/data o donde se genere" — no fija la ruta del config por defecto; obligaría a inventar la ubicación.
2. "Un comando deskops queue job set <trabajo> <campo> <valor> --root . (o el nombre que encaje con el CLI existente)" — nombre y forma no cerrados; obligaría a inventar la jerarquía del CLI.
3. "antes de la regla de solo CLI" — la regla no está definida; obligaría a inventar su alcance.
4. "test de que el config por defecto de init trae..." sin archivo, mientras Validation solo corre `tests/test_queue_cli.py`; obligaría a inventar dónde vive ese test o si esa validación lo cubre.
5. "retry_exit_codes [3]" y "<valor>" — no define parseo de "3" a lista de enteros ni formato de entrada; obligaría a inventar la conversión.
6. "no toca nada más del archivo" — no fija preservación de orden/espaciado; obligaría a inventar la serialización.
7. p6 "git commit -- <rutas>" — rutas no listadas; obligaría a inventar el conjunto exacto.

## DRY-RUN

**Lecturas:** TaskDoc; `deskops/cli` (queue); generador de config de init; `desk/config.json`; `tests/test_queue_cli.py`; CHANGELOG; commits 1bb918d5 y ef84b70d.

**Cambios previstos:** tests p1 (set en desk temporal, JSON válido, solo ese trabajo) y p2 (default con `[3]`); implementación del comando con validación y escritura mínima; actualizar default; aplicar comando a `desk/config.json`; CHANGELOG.

**Dependencias:** worktree que provee dispatch; subcomando queue existente; regla solo CLI.

**Validaciones futuras:** `pytest tests/test_queue_cli.py`; inspección del JSON; suite `-n 4`; commit con trailer `Task-Id`.

## FUTURO

El coordinador aplica el comando en sldb e IR. Dispatch entrega el worktree. Un humano u otro nodo confirma nombre final del comando, ubicación del config por defecto y formato de valor.
