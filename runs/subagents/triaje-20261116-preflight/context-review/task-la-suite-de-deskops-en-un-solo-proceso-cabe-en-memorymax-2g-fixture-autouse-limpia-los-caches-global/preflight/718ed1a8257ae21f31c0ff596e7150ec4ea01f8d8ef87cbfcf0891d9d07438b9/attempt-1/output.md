## REFORMULACION
En el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, el ejecutor debe añadir en `tests/conftest.py` una fixture autouse que, después de cada test, limpie los caches globales: `invalidate_runtime_cache()`, `invalidate_index_cache()`, `built_cache.clear()` y `alert_sink.forget()` de sldb, más los caches propios de deskops en `deskops/doc_access.py`. El resultado esperado es que la suite completa en un solo proceso termine bajo `MemoryMax=2G` sin OOM. Límites: no modificar sldb, no cambiar la regla de ejecución con `-n 4`; validar con una corrida en un proceso bajo `systemd-run` y otra con `pytest -n 4`.

## AMBIGUEDADES
1. “vacia los caches propios de deskops en deskops/doc_access.py (alrededor de las lineas 150-154)”: no se nombran los caches ni la API exacta; obligaría a inventar qué estructuras limpiar o qué función pública crear.
2. “si alguna no existe con ese nombre en el sldb hermano, se llama a la equivalente y se anota”: no se indica dónde anotar; obligaría a inventar si va en comentario, commit o documentación.
3. “rc igual al de main con -n 4” y “las mismas fallas que main”: no se define qué `main` ni qué corrida baseline; obligaría a inventar la referencia de comparación.
4. “los 3 archivos mas pesados”: no se especifica métrica ni alcance; obligaría a inventar el criterio de perfilado.

## DRY-RUN
Lecturas previstas: `tests/conftest.py`, `deskops/doc_access.py` y los módulos citados de sldb. Cambios previstos: fixture autouse con `yield` y limpieza posterior; eventual función pública de limpieza en `doc_access.py`. Dependencias: nombres/API del sldb hermano, `systemd-run`, `/dev/shm` y pytest sin xdist. Validaciones futuras: ejecutar la suite en un proceso con `MemoryMax=2G` y ejecutar `pytest -n 4`; comparar rc y fallas contra el baseline de main.

## FUTURO
Un nodo ejecutor implementará y medirá; un humano o CI aportará el baseline de `main` y decidirá la aceptación; el cierre con tests y commit corresponde al flujo de la tarea.
