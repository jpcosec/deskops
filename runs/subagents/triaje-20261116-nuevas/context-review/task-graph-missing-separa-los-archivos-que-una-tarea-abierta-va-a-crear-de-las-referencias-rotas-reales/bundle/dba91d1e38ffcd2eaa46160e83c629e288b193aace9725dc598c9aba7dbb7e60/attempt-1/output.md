## REFORMULACION
Nodo ejecutable `task.code` (no agregado) en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Propósito: que `graph missing` distinga destinos inexistentes citados por tareas abiertas, que probablemente se crearán, de referencias rotas reales. Resultado: los primeros se reportan como informational con código `planned_target`, separados de los `missing`; los mismos destinos desde documentos no abiertos siguen como missing; la salida informa cuántos hay de cada tipo. Límites: no cambiar `SOURCE_PATH` ni el extractor; no ocultar los `planned_target`, que siguen listándose. Superficie: `deskops/graph/checks.py`, `deskops/cli/commands/graph.py`, `tests/test_graph_checks.py`.

## AMBIGUEDADES
1. «status distinto de closed, superseded, cancelled o retired»: no dice dónde se lee el estado del TaskDoc ni qué hacer con estado ausente o desconocido; obligaría a inventar la fuente y el valor por defecto.
2. «el destino es un source_file, test_file o doc inexistente»: no define cómo clasificar el destino; obligaría a inventar reglas por extensión, prefijo o ubicación.
3. «lo reporta como informational con el codigo planned_target»: no aclara si `planned_target` va en `kind`, `reason`, un campo nuevo o solo en la salida; obligaría a inventar el esquema.
4. «La salida dice cuantos son de cada tipo»: el CLI actual cuenta missing/informational, no tipos; obligaría a inventar si “tipo” es `kind`, categoría planned/missing o ambos.

## DRY-RUN
Lecturas futuras: `checks.py`, `graph.py`, `tests/test_graph_checks.py`, `desk_graph.py` y el modelo de estados de TaskDoc. Cambios previstos: clasificar `missing_declared_target` según estado del TaskDoc de origen y clase del destino; añadir `planned_target` como informational; ajustar el listado y conteos del CLI; agregar tests para tarea abierta, átomo y tarea cerrada/archivada. Dependencias: estado disponible en frontmatter o histórico, mapeo `source_id`→TaskDoc y clasificación estable de destinos. Validaciones futuras, sin ejecutar: pytest de `test_graph_checks.py` y `test_graph_cli.py`, `deskops graph missing --root .`, y suite completa; las fallas se compararían contra un worktree limpio de `origin/main`.

## FUTURO
Un ejecutor/humano correrá las validaciones, decidirá si las fallas son preexistentes, registrará el informe, hará el commit descriptivo y cerrará la tarea. Otro nodo podrá revisar el diff o ejecutar la suite completa; aquí no se ejecuta ni se decide nada de eso.
