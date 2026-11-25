REFORMULACION
PC03 es un agregado no ejecutable del plan gates-por-tipo, repo deskops: agrupa composición y grafo para que un plan se promueva nodo a nodo y el DAG quede en el store. Resultado conjunto: `parent_id`/`children` y tipo `task.aggregate` (GC09); `add task --from-drawer … --node` (GC10); `deskops graph` sobre aristas de sldb (GC11). Límites: no escribe en sldb salvo `message send`; no reimplementa el evaluador; ningún gate se salta.

AMBIGUEDADES
1. "la tarea resultante tiene tipo, parent_id y depends_on como aristas del store". Obliga a decidir si `task_type` debe materializarse como arista nueva o basta que el documento se guarde bajo el modelo del tipo, como fija GC10; ningún hijo define esa arista.

DRY-RUN
No hay ejecución de PC03: termina cuando cierran sus hijos. Orden por aristas: GC09 (depende de GC01 y GC05) produce los campos de referencia, la regla de activación del agregado, doctor y show/next; entrega esos contratos a GC10 y GC11. GC10 (depende de GC03 y GC09) promueve nodos de `dag.yaml` a TaskDoc con tipo, padre y dependencias, y deja el mapa `promoted`; no entrega nada a GC11, hermano sin arista. GC11 (depende de GC09) cambia el snapshot de `graph` para tomar aristas del índice de sldb y reportar `missing`. Validación conjunta al cerrar: en un desk temporal, promover un nodo produce tipo, `parent_id` y `depends_on` como aristas; un agregado no activa hasta cerrar sus hijos; `graph neighbors` lista esos campos desde sldb; además `pytest tests` verde (regla 3). Lecturas previstas: dag.yaml, brief/alcance/decisiones y código citado; dependencias externas: GC01, GC03, GC05 y `G_SLDB_LANG` en GC09.

FUTURO
GC01 fija tipos y `__closeout_evidence__`; GC03 entrega `deskops review`; GC05 las reglas y `edges_blocked`. sldb debe cerrar los gates `G_SLDB_*` y deskops pinnear versión. El dueño confirma DC7, `--evidence`, `task.external` y Scion; quien opera el desk ejecuta la validación y dispone las revisiones.
