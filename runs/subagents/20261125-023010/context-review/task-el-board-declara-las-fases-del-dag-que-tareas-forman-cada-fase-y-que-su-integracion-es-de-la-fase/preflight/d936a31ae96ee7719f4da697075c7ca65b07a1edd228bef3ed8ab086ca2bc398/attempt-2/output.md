**REFORMULACION**
Propósito: que el Board declare explícitamente las fases del DAG, qué tareas componen cada fase y que la integración (validación combinada y commit de cierre) pertenece a la fase. Resultado: en `/mnt/ssd/proyectos/SLDB_1/deskops`, añadir al modelo `BoardDoc` (`deskops/models/board.py`) `PhaseIntegration(validation: list[str] = [], closing_commit: str | None = None)`, `Phase(id, tasks, integration)` y `phases: list[Phase] = []`; un validador que rechace tareas duplicadas entre fases o dentro de una fase (`ValueError` nombrando la tarea); el marcador en el `__template__` tras `rituals:` (`# DAG phases: id, tasks, integration` / `phases: ⸢rev•phases⸥`); y `tests/test_board_phases.py` con casos (a) round-trip de dos fases, (b) tarea en dos fases, (c) repetida en la misma fase, (d) Board sin `phases` válido. Límites: no CLI, vista, `integrate` ni skill; solo modelo, template y su test; ejecutar solo ese test y `test_board_portable_references.py`.

**AMBIGUEDADES**
1. “round-trip render -> extract por sldb con los mismos valores”: no fija ids de fase, tareas ni integración del fixture; obligaría a inventar los datos concretos de las dos fases.
2. “ValueError que nombra la tarea”: no fija formato ni texto del mensaje; obligaría a inventar la redacción exacta (y qué asertar).
3. “‘# DAG phases: id, tasks, integration’ y ‘phases: ⸢rev•phases⸥’”: no aclara si esa línea es comentario YAML literal ni si debe preservarse exactamente; obligaría a decidir el formato del marcador.
4. “sigue como tests/test_board_portable_references.py construye un BoardDoc”: no transcribe el patrón; obligaría a asumir la API de construcción (kwargs, `from_dict`, etc.) sin ver el archivo.

**DRY-RUN**
Lecturas: `deskops/models/board.py`, `desk/rituals/phase.md`, `desk/contexts/pill-007-phase-gated-task-flow.md`, `tests/test_board_portable_references.py`. Cambios previstos: clases y campo pydantic, validador, marcador en `__template__`, nuevo test. Dependencias: pydantic, render/extract de sldb. Validación futura: `TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_board_phases.py tests/test_board_portable_references.py`. Sin ejecutar nada.

**FUTURO**
Otros nodos producirán el comando CLI y la vista; un humano decidirá el cierre y el formato aceptado de integración; no es ambigüedad de este nodo.
