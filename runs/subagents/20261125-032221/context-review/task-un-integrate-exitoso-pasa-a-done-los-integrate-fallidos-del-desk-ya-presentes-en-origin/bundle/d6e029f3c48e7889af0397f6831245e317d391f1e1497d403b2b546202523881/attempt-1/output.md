## REFORMULACION

Encargo: que `deskops integrate`, tras un integrate real exitoso, barra `runs/queue/failed` del desk y promueva a `done` los trabajos de tipo `integrate` cuyo commit de cierre ya es ancestro de `origin/<rama>`, dejando constancia en su log. Resultado observable: esos fallidos pasan a `done` con una línea de log y los no integrados permanecen en `failed`; `tests/test_integrate.py` completo pasa. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`, tocando `deskops/integrate.py` y `tests/test_integrate.py`. Límites: fuera de alcance fases, encolado y otros tipos de trabajo. No es un nodo agregado ni paquete: es una tarea de código ejecutable.

## AMBIGUEDADES

1. "al final de un integrate real (no --dry-run) que termino bien" — no define cómo se detecta el éxito ni el punto exacto respecto a otros pasos finales; obligaría a inventar condición y orden.
2. "agregar al final del archivo de su campo log una linea" — no aclara si `log` es lista o cadena, ni separador/formato; obligaría a inventar representación.
3. "leer con queue._read_job" / "mover el JSON a done" — no dice qué hacer si el destino ya existe ni si el movimiento es atómico; obligaría a inventar política de colisión.
4. "buscar en la rama local el commit de cierre de esa tarea" — no cubre trabajos sin `task_id` ni múltiples coincidencias (`-1` implícito); obligaría a inventar fallback.
5. "despues del fetch que integrate ya hace" — asume un fetch en esa ruta; si no ocurre, el criterio de ancestro quedaría obsoleto.
6. "Tests nuevos ... con nombres que contengan 'failed'" — no fija cuántos ni qué casos límite; obligaría a inventar cobertura.

## DRY-RUN

Lecturas: `deskops/integrate.py`, `deskops/queue.py`, `tests/test_integrate.py`, fixtures de repo/origin bare. Cambios previstos: función de barrido de `queue_dir/'failed'`, filtro `kind=='integrate'`, resolución de sha por `git log -1 --grep`, comprobación `merge-base --is-ancestor`, escritura de log y movimiento a `done`; invocación al cierre exitoso; dos tests. Dependencias: git, helpers de cola, configuración de rama. Validaciones futuras: `TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_integrate.py -k failed`, luego el archivo entero. Sin ejecutar nada.

## FUTURO

Un ejecutor implementa y corre los tests; un humano valida el criterio de éxito y el formato de log antes del cierre.
