## REFORMULACION

Propósito: cerrar el hueco que permitió a un ejecutor scion bloqueado (sin código) avanzar su tarea a `ritual-testing` sin vía de retorno. Resultado: (1) una transición sembrada `RitualDoc:ritual-testing → RitualDoc:ritual-execution`, `task_returns_to_execution`, sin condición, `attributes.sets.status: active`, `terminal: false`, `manual: true`, con su archivo de tipo, copiando `testing-task_hands_to_closeout.md` y `type-task_hands_to_closeout.md`, declarada en `desk_declaration.yaml`; el flag `advance task --back --reason "<texto>"` con sus códigos 2, su bloqueo sin transición manual, la entrada `history` con motivo y los post-hooks; y (2) la regla en `_render_agents_md` de `deskops/runtime/scion.py` para que el ejecutor bloqueado no avance y use `sciontool status blocked`; más documentación en el manual. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops` (paquete deskops, seeds, tests, docs). Límites: checkout principal, sin worktree ni rama, sin `git add`/`git commit`; aplicar la transición a desks reales queda fuera.

## AMBIGUEDADES

1. "la opcion en `deskops/cli/registry.py` y el comando que la recibe": no nombra módulo ni función del comando; obligaría a inventar dónde vive y cómo se registra.
2. "`--back` en un nodo sin transicion manual sale bloqueado con el mensaje `no hay transicion de vuelta desde <nodo>`": no fija código de salida ni si es un `TransitionResult` bloqueado; obligaría a inventar ambos.
3. "`--back` sin `--reason`, o con motivo vacio, sale con codigo 2": no aclara si un motivo de solo espacios cuenta como vacío; obligaría a inventar el criterio.
4. "agrega a `history` la cadena `task_returns_to_execution: <texto>`": ningún archivo de `deskops/models/` está en alcance y el validador `TaskDoc`/`lifecycle_table` podría rechazar esa forma; obligaría a inventar si se toca el modelo.
5. "si el ejecutor termina bloqueado o sin cambios": no define "sin cambios" (¿diff vacío, sin archivos, sin tests?); obligaría a inventar el criterio del agents.md.

## DRY-RUN

Lecturas: `lifecycle.py` (`Transition`, `advance`, `transitions_from`), `services/tasks.py` (`advance_task`), `cli/registry.py`, `runtime/scion.py` (`_render_agents_md`), `desk_declaration.yaml`, seeds `data/lifecycle/`, tests y manual. Cambios previstos: crear los dos seeds nuevos, añadirlos como `managed` y al `include` de `RelationDoc`, portar `manual` en `Transition` y su selección en `advance`, exponer `--back/--reason` y validaciones, escribir la regla del ejecutor, tests (a–e), goldens y doc. Dependencias: `sldb.api.edges_from/edges_holding/apply_effects`, `lifecycle_table`, seeding y `doctor`. Validaciones futuras: el `pytest` indicado, regeneración de goldens de ayuda y `deskops doctor --root .` sin deriva. Un ejecutor futuro lo haría, no esta revisión.

## FUTURO

Aplicar la transición a desks reales (`deskops desk update --apply`, fuera de alcance); decidir qué goldens conservar; relanzar ejecutor/coordinador; revisión y aceptación del encargo por otro nodo.
