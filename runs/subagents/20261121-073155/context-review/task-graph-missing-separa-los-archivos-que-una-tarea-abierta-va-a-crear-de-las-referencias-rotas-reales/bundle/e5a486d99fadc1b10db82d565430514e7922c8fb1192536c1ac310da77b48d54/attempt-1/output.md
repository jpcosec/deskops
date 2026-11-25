## REFORMULACION

**Propósito:** evitar que `deskops graph missing` trate como referencias rotas los archivos que una tarea abierta aún va a crear, sin ocultarlos ni reescribir rutas. **Resultado:** los `missing_declared_target` cuyo origen es un TaskDoc abierto y cuyo destino es un `source_file`, `test_file` o `doc` inexistente pasan a informativos con código `planned_target`; el resto sigue como missing y la salida informa cuántos hay de cada tipo. **Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`. **Límites:** solo `deskops/graph/checks.py`, la salida de `deskops graph missing` en `deskops/cli/commands/graph.py` y `tests/test_graph_checks.py`; no se toca `SOURCE_PATH`, el extractor, ni se ocultan los `planned_target`.

## AMBIGUEDADES

1. «el tipo de destino lo da el kind del nodo que ya asigna el extractor (source_file, test_file, doc)»: un destino inexistente no tiene nodo, y `MissingGraphTarget` en el input solo expone `source_id`, `target_id`, `provenance_path`, `provenance_locator`, `extractor`, `reason` y `record`. Obligaría a inventar cómo derivar el `kind` del destino.
2. «planned_target va en el campo kind del hallazgo, con el mismo reason»: no hay referente para «el mismo reason» ni se indica qué valor toma `record` para que el hallazgo sea informativo. Obligaría a inventar el texto de `reason` y el criterio de clasificación informativa.
3. «La linea de resumen pasa a 'N missing, M informational (P planned_target)'»: no aclara si `P` es subconjunto de `M` o un contador adicional. Obligaría a inventar la semántica del resumen.

## DRY-RUN

**Lecturas:** `checks.py` (búsqueda de `MISSING_TARGET_KINDS` y `informational`), `graph.py` (`_missing`), `test_graph_checks.py`, el extractor en `deskops/graph/desk_graph.py` y los frontmatter de los TaskDoc de origen. **Cambios previstos:** clasificar hallazgos por `status` del TaskDoc origen (ausente/desconocido = abierto), marcar `kind=planned_target` y `record=True`, ajustar resumen en `graph.py` y añadir tests de tarea draft vs átomo vs inexistente. **Dependencias:** `extract_declared_edges(...).missing_targets`, disponibilidad del `kind` de destino y lectura de `status`. **Validaciones futuras:** `pytest -q tests/test_graph_checks.py`, `pytest -q tests/test_graph_cli.py`, `deskops graph missing --root .`, suite completa con `-n 4` y comparación en worktree limpio de `origin/main`.

## FUTURO

Decisión humana: aceptar que una ruta mal escrita en tarea abierta también salga como `planned_target`. Otro nodo/extractor podría exponer el `kind` del destino. Cierre: tests verdes y commit descriptivo.
