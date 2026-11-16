## REFORMULACION

Encargo ejecutable de código en `deskops` (no es agregado): hacer que cada intento de Scion tenga un RunDoc propio e inmutable, separando identidad del intento (`run-<agent_slug>-<n>` o equivalente estable), identidad del agente y referencia `scion://agent/<slug>`; registrar intención (`outcome: in_progress`) y confirmación de dispatch como hechos distintos; impedir que un reintento sobrescriba al anterior; y hacer que el closeout (commit y resolved-by) actualice exactamente el RunDoc del intento cerrado. Debe actualizar la docstring de `models/run.py`. Resultado: tests indicados en verde y contrato reflejado en el snapshot de modelos. Límites: solo `scion.py`, `models/run.py`, `closure.py` y los tests citados; no importar conversaciones/mensajes, otro broker, replicación ni UI.

## AMBIGUEDADES

1. «run-<agent_slug>-<n> (o equivalente estable)»: no fija esquema ni criterio de estabilidad; obliga a inventar el identificador definitivo.
2. «Contador de intento por tarea+contrato»: no dice dónde persiste ni cómo se comporta con concurrencia; obliga a inventar almacenamiento y atomicidad.
3. «si no esta expuesta, se usa solo la identidad interna»: no define quién decide ni cómo se documenta la rama elegida; obliga a inventar el criterio de fallback.
4. «closeout commit y resolved-by actualizan exactamente el RunDoc del intento cerrado»: no indica de dónde salen commit/resolved-by ni cómo se localiza el run_dir; obliga a inventar la resolución.
5. «El cambio de contrato de RunDoc queda registrado en el snapshot de modelos»: el test `tests/test_model_contract_snapshot.py` no figura en `files`; obliga a inventar si se regenera o se edita.
6. «sin fallas nuevas respecto de main»: no fija baseline ni tolerancia a flakes; obliga a inventar el criterio de comparación.
7. «La docstring de run.py queda al dia»: no especifica contenido; obliga a inventar el texto contractual.

## DRY-RUN

Lecturas: `scion.py:800-860`, `models/run.py`, `close_from_run` en `closure.py`, tests citados y, si hay acceso, `pkg/store/models.go` del repo scion. Cambios previstos: generación de ID por intento, campos intención/confirmación, actualización selectiva en closure, docstring y snapshot. Dependencias: acceso al repo scion hermano, convención de snapshot, baseline de `main`. Validaciones futuras: los cuatro comandos pytest del bloque Validation; ninguno se ejecuta aquí.

## FUTURO

Un humano o nodo posterior debe decidir el esquema estable de ID, la fuente de commit/resolved-by y la política de snapshot; otro nodo debe proveer el baseline de `main` y, si aplica, confirmar la API de Scion.
