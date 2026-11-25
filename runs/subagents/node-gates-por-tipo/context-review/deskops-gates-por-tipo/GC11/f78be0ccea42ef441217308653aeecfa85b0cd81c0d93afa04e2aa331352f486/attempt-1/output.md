REFORMULACION
Propósito: que `deskops graph` construya el snapshot desde el índice de aristas de sldb y deje de inferir aristas por regex en prosa. Resultado: aristas de referencia de `TaskDoc` (`depends_on`, `inherits_from`, `parent_id`, `children`, `pills`, `atoms`, `current_node`) y de `ReviewDoc` (`subject`) con su campo como role; `graph missing` reporta `unresolved_references`; esquema del snapshot versionado; `neighbors` y `reflect` leen el nuevo; goldens regenerados; tests y CHANGELOG. Repo dueño: deskops. Límites: solo `output_scope` (graph/*, CLI graph, tests/fixtures, docs/knowledge-graph, CHANGELOG); no escribir en sldb; no suplir con Python reglas de sldb; depende de GC09.

AMBIGUEDADES
1. «Los nodos de archivos fuente (extract_sources.py) y las materializaciones se conservan si el índice de sldb no los cubre; el TaskDoc fija la lista tras el grep.» No define cómo se comprueba la cobertura ni qué lista exacta sobrevive; obliga a inventar el criterio y la lista antes de que el TaskDoc la fije.
2. «produce aristas con role depends_on, parent_id, children y subject», sobre «una tarea task.code con depends_on, parent_id y un ReviewDoc». No hay agregado ni hijos en el montaje; el origen de `children` queda indefinido y obliga a inventar el fixture o a emitir una arista vacía.
3. «El esquema del snapshot sube de versión; graph neighbors y reflect leen el nuevo.» No hay aceptación ni salida esperada para `neighbors`/`reflect`; obliga a inventar qué significa «leer el nuevo» y cómo comprobarlo.
4. «los goldens de graph (tests/fixtures) regenerados y el diff revisado en el TaskDoc» no dice quién revisa ni qué convierte el diff en revisado; obliga a inventar el criterio de aceptación.

DRY-RUN
Lecturas: `dag.yaml` GC11 y GC09, `extract_edges.py`, `snapshot.py`, `checks.py`, `self_reflection.py`, comando graph, índice de aristas de sldb, fixtures y CHANGELOG. Cambios previstos: retirar el extractor regex de prosa, leer nodos/aristas del índice, mapear roles por campo, exponer `unresolved_references`, versionar el snapshot y regenerar goldens. Dependencias: GC09 (`parent_id`/`children`) y el contrato del índice de sldb. Validaciones futuras: `pytest tests/test_graph_*.py`, `graph build` en desk temporal, `graph missing`, grep de `TASK_OR_ISSUE_RE`, diff de goldens y CHANGELOG.

FUTURO
El TaskDoc fijará la lista de nodos fuente/materializaciones y los nombres exactos; un humano dispondrá la revisión del diff de goldens; GC09 entrega `parent_id`/`children`; sldb entrega el índice de aristas.
