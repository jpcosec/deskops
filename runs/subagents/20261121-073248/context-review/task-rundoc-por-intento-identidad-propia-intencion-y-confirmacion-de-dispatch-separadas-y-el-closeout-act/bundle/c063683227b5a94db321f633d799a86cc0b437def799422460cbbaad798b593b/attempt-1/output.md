REFORMULACION

El nodo debe implementar en `/mnt/ssd/proyectos/SLDB_1/deskops` un RunDoc por intento Scion: id `run-<agent_slug>` en el intento 1 y `run-<agent_slug>-a2` en el 2; campos `intent_at`, `dispatch_confirmed_at` y `external_ref`; `closeout commit --run-dir` actualiza solo el RunDoc cuyo `run_dir` coincide; docstring y tests. Límites: no importar conversaciones/mensajes, otro broker, replicación ni UI; sin intento 3; si la API de scion no expone run id, solo identidad interna. El repo scion hermano se consulta, no se modifica.

AMBIGUEDADES

1. «intent_at (cuando runtime template registra la intencion…)» y «(outcome, commit, finished_at)» frente a campos actuales `started_at`, `ended_at` y `commit_sha`: obliga a inventar si se renombran, se añaden o se mantienen ambos.
2. «mas external_ref scion://agent/<slug>» frente a `session_path` ya usado por `record_scion_run`: obliga a decidir si es campo nuevo, reemplazo o alias.
3. «dispatch_confirmed_at (cuando se observa el agente en scion)»: no nombra componente ni función que observe y escriba; obliga a inventar el mecanismo.
4. «el intento sale de la etiqueta deskops.attempt del despacho»: `record_scion_run` recibe `agent_slug`, no etiquetas; obliga a inventar cómo llega el intento.
5. «se usa solo la identidad interna»: no define qué identidad; obliga a inventar si es el slug, el `run_dir` o `session_path`.
6. «Entra: … tests/test_scion_runtime.py y tests/test_closeout.py» contradice que luego se actualicen «tests/test_model_contract_snapshot.py y tests/fixtures/model_contract_hashes.json»; obliga a decidir si esos archivos están dentro del alcance.

DRY-RUN

Lecturas: `scion.py:800-860`, `models/run.py`, `close_from_run` en `closure.py`, tests citados, contrato de despacho del rol y `pkg/store/models.go` del repo scion. Cambios previstos: campos opcionales en RunDoc, id derivado del intento, registro de intención y confirmación, `closeout commit` localizando `run.md` por `run_dir`, docstring y tests de dos intentos, cierre selectivo y RunDocs antiguos. Dependencias: API de scion y actualización del snapshot de modelos. Validaciones futuras: los cuatro comandos del TaskDoc y comparación de fallas en worktree limpio. Sin ejecutar nada.

FUTURO

Otro nodo confirma qué identidad expone scion y ejecuta las validaciones; el coordinador despacha y corre `closeout commit --run-dir`; un tester independiente valida; el humano adjudica fallas y aprueba el commit final.
