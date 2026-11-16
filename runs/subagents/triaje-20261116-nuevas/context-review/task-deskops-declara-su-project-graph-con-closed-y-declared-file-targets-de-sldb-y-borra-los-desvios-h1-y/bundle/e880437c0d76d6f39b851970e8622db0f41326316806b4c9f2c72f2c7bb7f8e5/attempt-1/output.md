REFORMULACION
Propósito: sustituir en deskops las desviaciones H1/H2 de CC33c por capacidades nativas de sldb (GD21). Resultado: `deskops/graph/desk_graph.py` arma su `ProjectGraphConfig` con `closed:` (predicado del lenguaje de reglas) en vez de `closed_document=_closed_issue`, y declara `declared_file_targets` para archivos existentes no-documento; `declared_target_is_a_file` y `_closed_issue` desaparecen. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo `deskops/graph/desk_graph.py`, `deskops/graph/checks.py` y dos tests; no se toca sldb ni `.sldb/store.yaml`; `graph missing --root .` debe dar la misma lista de faltantes; un destino no declarable se reporta por `deskops message send --to sldb` y conserva su tratamiento.

AMBIGUEDADES
1. "una condicion closed:" — no se da la sintaxis del lenguaje de reglas ni cómo se expresa la condición de `issue_status(text)=="closed"`; obligaría a inventar la forma del predicado `closed:`.
2. "declara declared_file_targets para los archivos existentes que no son documento" — `DeclaredFileTargets` exige `directory`+`field` de frontmatter; no se dice cómo cubrir destinos sueltos (`dag.yaml`, fixtures). Obligaría a inventar la config o el criterio de "no declarable".
3. "runs/subagents/<run>/graph-missing-antes.txt" — `<run>` no está definido; obligaría a inventar el directorio de la corrida.
4. "'...suite completa...). Sin fallas nuevas': 'cada test que falle...'" — clave truncada e imprecisa; obligaría a inventar el formato del informe y el umbral de "falla nueva".

DRY-RUN
Lecturas: `desk_graph.py:180-215`, `checks.py:55-90`, tests citados y las rutas de sldb (`document_surface.py:25`, `project_texts.py:41-48`, `project_graph_config_mapping.py:18,32-33`, `project_graph_config.py:38`, `declared_file_targets.py`, `declared_target_nodes.py`, `tests/api/test_project_graph.py:60`). Cambios previstos: capturar salida `graph missing` a `graph-missing-antes.txt`; reescribir `_closed_issue` como `closed:`; añadir `DeclaredFileTargets`; borrar `declared_target_is_a_file` y el filtro en `find_missing_graph_references`; ajustar tests. Dependencias: sldb GD21 con `closed:` y `declared_file_targets`. Validaciones futuras (sin ejecutar): pytest de los dos módulos, `graph missing` comparado, grep vacío, suite completa y, por cada falla, worktree limpio de `origin/main`.

FUTURO
Decide un humano si un destino no declarable amerita nota a sldb y su aceptación. Otro nodo ejecuta los cambios y corre las validaciones; el informe con fallas preexistentes lo consume el cierre.
