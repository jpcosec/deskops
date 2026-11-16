## REFORMULACION

Encargo ejecutable (no agregado): dotar a cada intento de Scion de un RunDoc propio que separe identidad del intento, identidad del agente y referencia `scion://agent/<slug>`, registre intención y confirmación de dispatch como hechos distintos, impida sobrescribir intentos previos y haga que el closeout actualice el RunDoc del intento cerrado. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`; verificación previa en el repo hermano `scion` (`pkg/store/models.go`). Resultado: cambios en `scion.py`, `models/run.py`, `closure.py`, tests y snapshot de contrato. Límites: sin importar conversaciones/mensajes, otro broker, replicación ni UI; `resolved-by` no toca RunDoc.

## AMBIGUEDADES

1. Formato del id: Goal dice `run-<agent_slug>-<n> (o equivalente estable)`; Scope dice `run-<agent_slug>-a2 en el 2`. Obliga a elegir entre plantilla numérica y sufijo alfabético.
2. Origen del intento: Implementation Path pide `Contador de intento por tarea+contrato`; Scope afirma `El intento sale de la etiqueta deskops.attempt del despacho, no de un contador nuevo`. Obliga a decidir si existe contador persistido.
3. `resolved-by`: Goal exige que `closeout commit y resolved-by actualizan exactamente el RunDoc`; Scope dice `resolved-by, que no tiene run-dir, no toca RunDoc`. Obliga a inventar cuál prevalece.
4. Identidad interna: `se usa solo la identidad interna` sin definir campos ni fuente. Obliga a inventar el esquema.
5. Intención/confirmación: `registra la intencion (outcome in_progress) y la confirmacion de dispatch como hechos distintos`, sin nombres de campos ni contrato. Obliga a inventar el modelo.
6. Contrato del supervisor: `igual que el nombre del hijo en el contrato de despacho del rol deskops-supervisor`, no citado. Obliga a inventar el mapeo.

## DRY-RUN

Lecturas: `scion.py:800-860`, `models/run.py`, `close_from_run`, ambos tests, snapshot/golden y API en `scion/pkg/store/models.go`. Cambios previstos: id por intento desde `deskops.attempt`; campos de intención/confirmación; localización por `run_dir` en closure; docstring; tests de dos intentos, cierre del segundo y lectura de RunDocs viejos. Dependencias: exposición de `Agent.RunID/PreviousRunIDs`, pytest y golden; sandbox de roots para mutaciones. Validaciones futuras: los cuatro comandos y suite completa con comparación en worktree limpio.

## FUTURO

Deciden otro nodo o humano: si la API de `scion` expone el run id, el esquema final de campos, la prevalencia de `resolved-by`, y la aceptación de fallas preexistentes detectadas en el worktree limpio.
