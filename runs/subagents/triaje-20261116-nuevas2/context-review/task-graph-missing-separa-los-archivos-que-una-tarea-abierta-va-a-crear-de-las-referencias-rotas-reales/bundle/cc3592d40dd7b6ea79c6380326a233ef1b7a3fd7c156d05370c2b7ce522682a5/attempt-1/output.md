## REFORMULACION

**Propósito:** que `graph missing` deje de mezclar en una sola lista los destinos inexistentes que una tarea abierta aún va a crear con las referencias realmente rotas.

**Resultado:** los `missing_declared_target` cuyo origen es un TaskDoc con status abierto y cuyo destino es `source_file`/`test_file`/`doc` inexistente pasan a informarse como `planned_target` en la sección informacional, con contadores separados; el resto sigue como missing.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops` (`task_type: task.code`, nodo ejecutable, no agregado).

**Límites:** no tocar `SOURCE_PATH` ni el extractor, no ocultar los `planned_target`, no reescribir rutas del desk para esquivar el detector; fuera de alcance `deskops/graph/desk_graph.py`.

## AMBIGUEDADES

1. «El tipo de destino lo da el kind del nodo que ya asigna el extractor (source_file, test_file, doc)» — un target inexistente no tiene nodo ni kind; obligaría a inventar el mapeo ruta→kind o a asumir que todo planned es `doc`.
2. «buscar MISSING_TARGET_KINDS y 'informational'» — esa constante no aparece en `checks.py`; obligaría a inventar dónde vive o crearla.
3. «planned_target va en el campo kind del hallazgo, con el mismo reason» — no dice si lleva `record=True` (única palanca actual de la lista informacional) ni a qué `reason` se refiere.
4. «La linea de resumen pasa a 'N missing, M informational (P planned_target)'» — no dice si cambia la cabecera «Informational (archived records)» ni el código de salida (hoy `1 if failing else 0`).
5. «una tarea cerrada (en history) no aplica porque ya no esta en desk/tasks» — deja sin fixture el caso «documentos que no son tareas abiertas», que el Goal exige; obligaría a inventar dónde vive ese documento.

## DRY-RUN

**Lecturas:** `deskops/graph/checks.py`, `deskops/cli/commands/graph.py`, `tests/test_graph_checks.py`, `tests/test_graph_cli.py` y, solo como referencia, `deskops/graph/desk_graph.py` (`SOURCE_PATH`, kinds).

**Cambios previstos:** en `checks.py`, clasificar cada missing por status del TaskDoc de origen (leyendo frontmatter; ausente/desconocido = abierto) y reetiquetar `kind`/`record`; en `graph.py`, separar bloques, contar `planned_target` y ajustar la línea de resumen; en tests, tres casos (tarea draft → planned; átomo → missing; no-tarea → missing).

**Dependencias:** `MissingProjectTarget` de sldb (sin `kind` de destino), lectura de frontmatter, `record` como criterio informacional.

**Validaciones futuras:** las cuatro órdenes de la sección Validation, incluida la suite completa y la comparación en worktree limpio de `origin/main`.

## FUTURO

- Decisión humana: aceptar que una ruta mal escrita en tarea abierta salga como `planned_target`.
- Otro nodo ejecuta los tests, el commit descriptivo (átomo de cierre) y redacta el informe con fallas preexistentes.
