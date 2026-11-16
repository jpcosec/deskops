## REFORMULACION

Encargo: en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, redirigir las salidas derivadas de `deskops/graph/export.py` y `deskops/graph/self_reflection.py` desde `.sldb/runtime/` hacia `.sldb_cache/`, conservando la estructura de subcarpetas. Resultado esperado: ningún archivo Python de `deskops/` escribe en `.sldb/runtime/`; los tests indicados pasan; si hay consumidores externos que leen la ruta vieja, se les avisa por inbox. Límites: no migrar archivos ya escritos, no tocar `sldb`; el alcance incluye los dos módulos, sus tests y posiblemente `tests/test_gitignore_policy.py`.

## AMBIGUEDADES

1. “Cambiar las rutas a una constante comun que apunte a .sldb_cache”: no indica dónde definirla, su nombre ni si debe ser compartida entre módulos. Obligaría a inventar módulo, nombre y API.
2. “misma estructura de subcarpetas”: no enumera las subcarpetas actuales ni la raíz exacta. Obligaría a inferirlas leyendo el código.
3. “tests/test_gitignore_policy.py si hace falta”: no define el criterio de necesidad. Obligaría a inventar la condición.
4. “si hay, `deskops message send --to graph_ui`”: no especifica asunto, cuerpo ni si pueden existir otros destinatarios. Obligaría a inventar el mensaje.
5. “sin fallas nuevas respecto de main”: no define baseline ni procedimiento de comparación. Obligaría a inventar cómo medir “nuevas”.
6. “se borran a mano solo si no estan versionados”: no aclara quién decide ni cuándo. Obligaría a asignar responsabilidad.
7. El grep usa `sldb/runtime` y el texto `.sldb/runtime` de forma intercambiable; no queda claro si se busca con punto inicial.

## DRY-RUN

Lecturas previstas: los dos módulos, tests citados, pill de política, referencia de inbox. Cambios previstos: introducir constante hacia `.sldb_cache`, sustituir rutas, ajustar aserciones de tests. Dependencias: `.venv`, `pytest`, `TMPDIR=/dev/shm`, grep. Validaciones futuras: los cinco comandos pytest/grep listados y la suite completa. Sin ejecutar nada.

## FUTURO

Un ejecutor posterior aplicará los cambios y correrá las validaciones. Un humano decidirá si procede avisar a consumidores externos y aprobará el cierre. Otro nodo podría generar el mensaje de inbox y el commit.
