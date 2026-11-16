REFORMULACION
Propósito: reproducir y corregir que el closeout reconozca una `MaterializationContractDoc` declarada cuyo target es un golden bajo `tests/fixtures`, sin admitir fixtures no declarados. Resultado: recibo de reproducción, corrección en deskops o petición a sldb, y test de regresión —o `xfail` citando la nota a sldb—. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: tocar `deskops/graph/desk_graph.py` (EXCLUSIONS/MATERIALIZATION_TARGETS, ~83-93), `tests/test_desk_graph_runs_target.py` y el recibo; no modificar sldb directamente. Aplican los átomos de cierre con tests/commit y de mutación CLI con sandbox de desk roots.

AMBIGUEDADES
1. “Hay que confirmar donde corta antes de cambiar” y “Corregir en deskops o pedir a sldb”: no fija evidencia ni criterio para decidir el corte; obligaría a inventar el umbral de decisión.
2. “guardar la salida como recibo (`deskops review record <tarea> --kind reproduction --evidence <archivo> --reason ...`)”: no define nombre/ruta del archivo ni el `--reason`; obligaría a inventarlos.
3. “el test de regresion cubre el golden declarado y un archivo de fixtures no declarado sigue excluido (o queda xfail citando la nota a sldb)”: no indica cuándo el `xfail` es aceptable ni el formato/ID de la nota; obligaría a inventar ese criterio.
4. “sin fallas nuevas respecto de main”: no define cómo obtener/comparar la línea base; obligaría a inventar el método.

DRY-RUN
Lecturas: `desk_graph.py` alrededor de 83-93, test objetivo, tests de materialization/declared edges y el drawer citado. Cambios previstos: sandbox con átomo, materialization a `tests/fixtures/golden.txt` y cambio en ese archivo; capturar `deskops graph missing` y `deskops closeout verify`; registrar recibo; localizar el corte; corregir en deskops o enviar mensaje a sldb; añadir regresión. Dependencias: CLI deskops, sandbox de roots, `review record`, y eventual nota sldb. Validaciones futuras: los cuatro comandos pytest indicados, incluida la suite completa.

FUTURO
Un nodo/equipo sldb produce la corrección o el ID de nota si el corte está allí. Un humano decide si el `xfail` es aceptable y si la comparación con `main` satisface “sin fallas nuevas”.
