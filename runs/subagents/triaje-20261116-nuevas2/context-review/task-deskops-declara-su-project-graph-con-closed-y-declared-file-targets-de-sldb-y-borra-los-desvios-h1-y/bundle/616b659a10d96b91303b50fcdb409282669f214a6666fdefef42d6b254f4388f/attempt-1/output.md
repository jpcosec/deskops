## REFORMULACION

Encargo ejecutable (task.code) en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`: migrar la configuración de `project_graph` de deskops a dos capacidades de sldb (GD21) que hoy emula con código propio —H2 `closed:` como predicado del lenguaje de reglas en lugar de `closed_document=_closed_issue`, y H1 `declared_file_targets` en lugar de `declared_target_is_a_file`— y borrar ambos desvíos de CC33c. Resultado observable: `deskops graph missing --root .` devuelve el mismo conjunto de líneas que antes (guardado en `runs/subagents/project-graph-<AAAAMMDD>/graph-missing-antes.txt`), el grep de `declared_target_is_a_file|_closed_issue` en `deskops` queda vacío, y pasan los tests indicados más la suite completa sin fallas nuevas. Límites: no se toca sldb ni `.sldb/store.yaml` a mano; alcance en `desk_graph.py`, `checks.py` y sus dos tests; destinos no declarables conservan su tratamiento y se avisan a sldb.

## AMBIGUEDADES

1. «declara declared_file_targets para los archivos existentes que no son documento» frente a «se declara uno por cada carpeta del desk cuyos documentos nombran archivos en un campo de frontmatter (al menos desk/materializations con field target_identity)»: no se enumeran las carpetas/campos; obligaría a inventar la lista de `DeclaredFileTargets`.
2. «la misma condicion que hoy evalua _closed_issue»: `_closed_issue` delega en `issue_status(text)`, pero no se da la expresión `closed:` concreta; obligaría a inventar la sintaxis del predicado.
3. «guardar la salida ... en runs/subagents/<run>/graph-missing-antes.txt» y «La corrida se llama runs/subagents/project-graph-<AAAAMMDD>/»: no aclara si `<run>` es ese directorio; obligaría a decidir la ruta.
4. «diff vacio» frente a «por conjunto de lineas (orden indistinto)»: criterios incompatibles; obligaría a elegir comparación.
5. «se manda deskops message send --to sldb con el caso»: no define formato ni umbral de "no declarable"; obligaría a inventar el contenido.

## DRY-RUN

Lecturas: `deskops/graph/desk_graph.py:180-215`, `deskops/graph/checks.py:55-90`, docs y `tests/api/test_project_graph.py` de sldb, estado del repo y de la versión instalada. Cambios: crear el directorio de corrida y guardar la salida previa de `graph missing`; en `desk_graph.py` sustituir `closed_document=_closed_issue` por `closed` con la condición traducida y completar `declared_file_targets`; borrar `_closed_issue`; en `checks.py` borrar `declared_target_is_a_file` y su filtro; ajustar/añadir tests. Dependencias: sldb con `closed:` y `DeclaredFileTargets`, CLI `deskops`, `../.venv`. Validaciones futuras: los cinco comandos del TaskDoc y, si falla la suite, worktree limpio de `origin/main` para comparar. Nada se ejecuta aquí.

## FUTURO

Otro nodo recibe la nota a sldb si algún destino no es declarable; un humano decide aceptar fallas preexistentes y aprueba el informe; el cierre exige el commit descriptivo del átomo de cambios de código.
