## REFORMULACION

Encargo ejecutable de código en el repo `/mnt/ssd/proyectos/SLDB_1/deskops` (con lectura previa, no modificación, del repo hermano `/mnt/ssd/proyectos/SLDB_1/scion`). Propósito: que cada intento de despacho Scion tenga un RunDoc propio, con identidad por intento y con separación entre intención de dispatch y confirmación de dispatch, y que el cierre con `--run-dir` actualice el RunDoc correspondiente. Resultado: `deskops/runtime/scion.py` genera id `run-<agent_slug>` (intento 1) o `run-<agent_slug>-a2` (intento 2) tomando el intento de la etiqueta `deskops.attempt`; `deskops/models/run.py` añade `intent_at`, `dispatch_confirmed_at` y `external_ref: scion://agent/<slug>`, y documenta autoría y formato; `deskops/services/closure.py` actualiza por `run_dir` (outcome, commit, finished_at) y no toca RunDoc en `resolved-by`. Límites: sin importar conversaciones/mensajes, sin otro broker, replicación ni UI; sin contador nuevo de intentos ni intento 3; compatibilidad con RunDocs antiguos sin campos nuevos.

## AMBIGUEDADES

1. "si no esta expuesta, se usa solo la identidad interna": no define qué es la identidad interna ni de dónde se obtiene; obligaría a inventar su fuente y formato.
2. "outcome in_progress": no consta el vocabulario de outcomes; obligaría a inventar el literal exacto y su validación.
3. "el intento sale de la etiqueta deskops.attempt del despacho": no indica dónde se lee ni el formato del valor; obligaría a inventar el punto de lectura y el parseo.
4. "resolved-by no tiene run-dir y no toca RunDoc": no define la ruta resolved-by; obligaría a inventar cómo distinguirla del cierre con `--run-dir`.
5. "se actualizan con pytest --update-golden si el test lo admite, o editando el hash": no fija cuál aplicar; obligaría a inventar criterio de elección.

## DRY-RUN

Lecturas: `scion.py:800-860`, `models/run.py`, `close_from_run` en `closure.py`, tests citados y API de scion (`pkg/store/models.go`). Cambios previstos: id por intento; tres campos y docstring; actualización de cierre por `run_dir`; tests de dos intentos, cierre selectivo y compatibilidad; snapshot/golden. Dependencias: exposición de `RunID`/`PreviousRunIDs` en scion. Validaciones futuras: los cuatro comandos pytest indicados, incluida suite completa y baseline en worktree limpio de `origin/main`.

## FUTURO

Decide un humano/otro nodo: si la API de scion expone identidad de ejecución; si se acepta la lista de fallas preexistentes; la ejecución real, el commit y el registro del contrato en el snapshot.
