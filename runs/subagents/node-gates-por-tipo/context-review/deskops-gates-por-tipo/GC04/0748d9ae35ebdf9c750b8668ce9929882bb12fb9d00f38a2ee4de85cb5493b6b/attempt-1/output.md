## REFORMULACION
Propósito: que el ciclo de vida de deskops declare los efectos en las aristas y que `advance` los aplique vía sldb. Resultado: `ensure_lifecycle_graph` escribe cada `RelationDoc` con `attributes.sets`/`terminal`; `desk update --apply` reescribe los divergentes; el YAML conserva `transitions` como plantilla sin `sets_status`/`terminal` de nivel superior; `advance` usa `edges_holding`/`apply_effects` y sigue escribiendo `history`; el cierre sigue en `closeout commit`. Repo dueño: deskops. Límites: solo `output_scope`; no toca sldb ni reimplementa el evaluador; requiere `G_SLDB_EFFECTS` (pending).

## AMBIGUEDADES
1. "si terminal, current_node = complete" frente a "La transición terminal sigue sin persistirse desde advance". Obliga a inventar si `advance` debe escribir `current_node=complete` o no, y qué excluye exactamente "persistir" la transición terminal.
2. "se aplica apply_effects(payload, effects, modelo del tipo de la tarea)" con "depends_on: []". No se declara de dónde sale ese modelo ni si GC04 puede ejecutarse antes de GC01; obliga a inventar la resolución del tipo o a añadir una dependencia no escrita.
3. "se toma la primera en el orden del spec". No define si el orden es el de `transitions` del YAML, el de `edges_holding` o el de los `RelationDoc`; obliga a inventar el desempate cuando varias aristas se cumplen.
4. Aceptación: "los tres RelationDoc tienen attributes.sets.status (active, ready_for_testing, closed)" y "advance ... deja status active ... (test que cambia el sets del RelationDoc a otro valor)". No identifica los tres documentos ni fija si el status esperado es `active` o el valor cambiado; obliga a inventar el mapa y el resultado esperado.

## DRY-RUN
Lecturas: `deskops/lifecycle.py`, `spec/workflows/task_lifecycle.yaml`, `services/tasks.py`, `workflow/next_actions.py`, tests de lifecycle, docs y CHANGELOG. Cambios previstos: `attributes` en los `RelationDoc`, limpieza de `sets_status`/`terminal` del YAML y de `Transition/LifecycleSpec.effect`, migración idempotente en `desk update --apply`, `advance` por `edges_holding`/`apply_effects`, tests adaptados. Dependencia: `G_SLDB_EFFECTS`. Validaciones futuras: desk temporal, tres aristas, terminal, grep, idempotencia, tests y CHANGELOG. Sin ejecutar.

## FUTURO
sldb cierra GO09 y deskops pinnea la versión para `G_SLDB_EFFECTS`. GC05 asume `findings`/`edges_blocked` y `closeout_evidence_verified`. GC01, si corresponde, entrega los modelos de tipo usados por `apply_effects`. La promoción del TaskDoc y la aceptación final son del humano que opera el desk.
