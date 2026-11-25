## REFORMULACION
Encargo ejecutable (`task.code`, no agregado): en el repo `deskops`, modificar `deskops/graph/checks.py`, `deskops/cli/commands/graph.py` y `tests/test_graph_checks.py` para que `graph missing` clasifique como `informational` con código `planned_target` los `missing_declared_target` cuyo origen sea un TaskDoc abierto (`status` distinto de `closed`, `superseded`, `cancelled` o `retired`; ausente/desconocido cuenta como abierto) y cuyo destino sea `source_file`, `test_file` o `doc` inexistente. Los mismos destinos desde documentos no abiertos siguen como `missing`. La salida debe indicar cuántos hay de cada tipo, con línea de resumen `N missing, M informational (P planned_target)`. Límites: no cambiar `SOURCE_PATH` ni el extractor; no ocultar los `planned_target`. Resultado esperado: comportamiento CLI y tests ajustados; validación en repo `deskops`.

## AMBIGUEDADES
1. «lo reporta como informational con el codigo planned_target» frente a «planned_target va en el campo kind del hallazgo»: no queda fijado si `planned_target` es un `kind`, un `code` o ambos; obligaría a inventar el esquema exacto del hallazgo.
2. «graph missing da rc 0 igual»: no se especifica si los `planned_target` conservan rc 0; obligaría a decidir semántica de exit code no declarada.
3. «un atomo del sandbox que cita ese mismo archivo da missing»: no se define cómo construir ese átomo ni si el sandbox ya dispone de uno; obligaría a inventar el fixture.

## DRY-RUN
Lecturas previstas: TaskDoc, `checks.py`, `graph.py`, `tests/test_graph_checks.py` y, solo para entender dependencias, extractor/parseo de `status`. Cambios previstos: separar listas `missing`/`informational` en `checks.py`; ajustar resumen y presentación en `graph.py`; añadir tests de tarea abierta con destino planificado y de átomo con destino faltante. Dependencias: `kind` asignado por el extractor, lectura del `status` del frontmatter y formato actual de la CLI. Validaciones futuras, sin ejecutar: `pytest -q tests/test_graph_checks.py`, `pytest -q tests/test_graph_cli.py`, `deskops graph missing --root .` y suite completa con comparación de fallas en worktree limpio de `origin/main`.

## FUTURO
El ejecutor futuro producirá el parche, tests y el informe con fallas de baseline. Un humano o nodo revisor decidirá las ambigüedades anteriores, aceptará el tratamiento de rutas mal escritas en tareas abiertas como `planned_target` y aprobará el cierre/merge. No hay nodos hijos que recorrer.
