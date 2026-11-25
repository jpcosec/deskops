## REFORMULACION
Propósito: automatizar la limpieza de trabajos `integrate` fallidos cuyos cambios ya llegaron a `origin`, evitando ordenarlos a mano. Resultado: al finalizar un `integrate` real exitoso, recorrer `runs/queue/failed`, mover a `done` los `integrate` cuyo commit de cierre sea ancestro de `origin/<branch>` y añadir una línea al log; los demás permanecen en `failed`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo `deskops/integrate.py` y `tests/test_integrate.py`; solo trabajos `kind == 'integrate'`; quedan fuera fases, encolado y otros tipos. Nodo ejecutable `task.code`, no agregado.

## AMBIGUEDADES
1. «deskops integrate recorre runs/queue/failed del desk» frente a «queue_dir(root)/'failed'»: no se define qué `root` o “desk” usar; obligaría a inventar la resolución del desk actual.
2. «tomar su task_id, buscar en la rama local el commit de cierre de esa tarea (… <integrate.branch>)»: no indica de dónde obtener `integrate.branch` ni qué hacer si falta; obligaría a inventar un fallback.
3. «mover el JSON a queue_dir(root)/'done'»: no define qué hacer si ya existe un archivo con ese nombre; obligaría a inventar sobrescritura o renombrado.
4. «después del fetch que integrate ya hace»: no aclara si ese fetch ocurre también cuando el éxito es «ya integrado»; obligaría a decidir si se hace un fetch adicional.

## DRY-RUN
Lecturas: TaskDoc, `deskops/integrate.py`, `tests/test_integrate.py`, helpers `queue_dir` y `_read_job`, fixtures de repo git temporal y origin bare. Cambios previstos: añadir barrido final tras integrate exitoso; leer JSON `failed`; filtrar `integrate`; buscar commit de cierre por `Task-Id`; comprobar ancestro con `merge-base --is-ancestor`; mover a `done` y anexar log, o conservar en `failed`. Dependencias: git, origin actualizado, helpers de cola y fixtures existentes. Validaciones futuras: `TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_integrate.py -k failed` y después el archivo completo.

## FUTURO
El ejecutor producirá el cambio y los tests; un humano resolverá las ambigüedades y aceptará el resultado. La activación real ocurrirá en un `integrate` posterior, fuera de este preflight.
