## REFORMULACION
CC33c es un nodo `delivery` de deskops, hijo del agregado CC33. Encargo: que `deskops graph build|neighbors|missing|reflect` y `drift` lean el grafo de proyecto de sldb (GD21) usando la configuración de grafo de deskops declarada como dato, y que desaparezcan la construcción propia (`graph/snapshot.py`), el rglob de `graph/checks.py` y los de `graph/self_reflection.py`. Resultado: paridad con el oráculo v1 en el desk real, oráculo borrado tras aceptar, grep de rglob vacío, goldens de ayuda/salida idénticos, `doctor` sin hallazgos nuevos en 6 desks, líneas antes/después y CHANGELOG. Repo dueño: deskops. Límites: no escribir en sldb, no suplir reglas con Python, no tocar P4, no cambiar formato del desk ni gramática del CLI; borrar el código viejo en el mismo paso; depende de CC38 y del gate G_GD21 (satisfecho).

## AMBIGUEDADES
1. «deskops graph build|neighbors|missing|reflect y drift leen sldb graph project» frente a la aceptación, que solo exige «graph neighbors y missing dan lo mismo que el oráculo v1»: `build`, `reflect` y `drift` no tienen aceptación; obliga a inventar cómo comprobarlos.
2. «con la configuración de grafo de deskops declarada como dato en project_graph» frente a DO8: «`sldb.api.project_graph(store)` no sirve porque deskops no declara `project_graph` en store.yaml» y usa `ProjectGraph(root, desk_graph_config())`; obliga a inventar dónde vive la declaración.
3. «El enlace atom/materialization que usa el closeout (CC33a) se lee de ese grafo cuando este nodo entra»: no hay arista CC33c→CC33a ni aceptación de ese enlace; obliga a inventar si CC33c toca closeout o espera a CC33a.
4. «requires: - G_GD21» frente a DO8: «Ambos esperan a sldb H1-H2 (drawer de sldb 61e9c7a9)»; falta gate/dependencia y obliga a inventar si puede promoverse ya.

## DRY-RUN
Un ejecutor futuro leería dag.yaml, brief, alcance, decisiones (DO8), el oráculo v1, el API GD21 de sldb y los goldens. Cambiaría la configuración de grafo en `desk_graph`, `cli/commands/graph.py` y `drift.py`; borraría `graph/snapshot.py`, `graph/checks.py` y los rglob de `graph/self_reflection.py`; adaptaría tests y CHANGELOG. Dependencias: CC38 integrado y G_GD21 pinneado; DO8 sugiere además H1-H2. Validaría: comparación `neighbors`/`missing` contra el oráculo sobre el desk real; grep de rglob vacío; goldens idénticos; `doctor` en 6 desks; líneas antes/después; tests tocados verdes. Sin ejecutar nada.

## FUTURO
CC33a/CC33b deciden la lectura del enlace atom/materialization en closeout; CC35c consume la configuración de grafo y `MentionPattern` que deja este nodo; el supervisor decide preflight/cold-bundle y promoción; el TaskDoc fijará nombres exactos de archivos y tests; sldb H1-H2 y DO8 los resuelve el coordinador o el dueño.
