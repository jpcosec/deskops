REFORMULACION
Propósito: que un nodo de un `dag.yaml` del drawer se promueva a `TaskDoc` con tipo, padre agregado y dependencias, y que el mapa nodo→tarea permita cruzar promoción y revisiones. Resultado: `deskops add task --from-drawer <plan>/dag.yaml --node <ID>` crea la tarea, escribe `promoted` en el dag, falla ante prerrequisito no promovido, gate `pending` o duplicado, y `review status <plan-dir>` muestra tarea y revisiones por nodo. Repo dueño: deskops. Límites: única escritura al drawer es `promoted`; no toca sldb; no transfiere revisiones de nodo a la tarea; no crea scripts para planes nuevos.

AMBIGUEDADES
1. “El mapa nodo → tarea se guarda en el dag.yaml bajo promoted: {ID: <task-id>} (única escritura al drawer; idempotente)” frente a “una segunda promoción del mismo nodo falla como duplicado”. El ejecutor debe inventar si reintentar es no-op idempotente o error de duplicado.
2. “review status <plan-dir> muestra por nodo la tarea promovida y el estado de sus revisiones”. No dice si “sus revisiones” son los `ReviewDoc` de nodo (`subject_ref`) o los `preflight`/`bundle` de la tarea, y el propio scope declara que no se transfieren.
3. “files (= output_scope partido por ',')”. El split literal produce entradas con anotación y directorios, p. ej. “deskops/services/review.py (status por plan)” y “tests/”; obliga a inventar si se limpian anotaciones, barras finales o se guardan crudas.

DRY-RUN
Lecturas: dag.yaml, GC03 (`review status`/`dispose`), GC09 (`add task --parent`, `task.aggregate`), modelos y bootstrap. Cambios previstos: `drawer.py`, `tasks.py`, `review.py` (status por plan), `registry.py`, tests, `docs/operator-manual.md`, `CHANGELOG.md`. Dependencias: GC03 y GC09 cerrados. Validaciones futuras: desk temporal; promover GC02; GC03 después con `depends_on`; GC03 antes falla nombrando GC02; GC04 falla nombrando `G_SLDB_EFFECTS`; duplicado falla; `promoted` escrito; `review status` cruza nodo/tarea; `pytest tests`; docs y CHANGELOG.

FUTURO
GC03 entrega el comando `review` y `status`; GC09 entrega `parent_id`, `children` y el agregado; sldb entrega los gates `G_SLDB_*`. El operador del desk dispone las revisiones y autoriza la promoción; nada de eso es ambigüedad de este nodo.
