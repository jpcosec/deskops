## REFORMULACION

Propósito: que BoardDoc declare las fases del DAG (qué tareas forman cada fase y la integración de la fase). Resultado: `PhaseIntegration(validation, closing_commit)`, `Phase(id, tasks, integration)`, campo `phases: list[Phase]` en `BoardDoc`, validador que rechaza tareas duplicadas, marcador de fases en `__template__` y `tests/test_board_phases.py` con casos (a)-(d). Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo `deskops/models/board.py`, su `__template__` y el test nuevo; fuera CLI, vista, integrate y skill. Es tarea ejecutable, no agregado.

## AMBIGUEDADES

1. «siguiendo como tests/test_board_portable_references.py construye un BoardDoc» y «Vocabulario: desk/rituals/phase.md y desk/contexts/pill-007-phase-gated-task-flow.md (solo leer)»: esos archivos no están en el input; obliga a inventar la construcción del BoardDoc de prueba y el vocabulario exacto.
2. «round-trip extract/render» (Scope) frente a «render -> extract» (Implementation Path): dirección contradictoria; obliga a elegir y puede dejar un sentido sin cubrir.
3. «hace round-trip render -> extract por sldb»: no se nombra la función/API de sldb; obliga a inventar la llamada de render/extracción.
4. «después de rituals: '# DAG phases: id, tasks, integration'»: no se fija línea exacta ni si el comentario es literal; obliga a decidir ubicación y formato.
5. «validation: list[str] = []» / «phases: list[Phase] = []»: no se indica versión de pydantic ni si usar `Field(default_factory=...)`; obliga a elegir forma de declaración.

## DRY-RUN

Lecturas: `deskops/models/board.py`, `__template__`, test de referencia, `phase.md`, `pill-007-phase-gated-task-flow.md`, API de sldb. Cambios previstos: clases `PhaseIntegration`/`Phase`, campo `phases` en `BoardDoc`, validador `ValueError` nombrando la tarea, marcador en el frontmatter del template y tests (a)-(d). Dependencias: pydantic y sldb ya presentes. Validaciones futuras: ejecutar `TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_board_phases.py tests/test_board_portable_references.py` y comprobar round-trip, rechazos y Board sin `phases`. Nada ejecutado.

## FUTURO

Otros nodos producirán el comando CLI (`task-deskops-declara-fases-del-board-por-cli`), la vista (`task-deskops-view-board-muestra-las-fases`), integrate y skill. Un humano aceptará el vocabulario y el Done When, y decidirá si el default vacío basta para los Board existentes.
