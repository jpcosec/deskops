## REFORMULACION

Encargo ejecutable (nodo `task.code`, no agregado): corregir en el repo deskops (`/mnt/ssd/proyectos/SLDB_1/deskops`) una regresión introducida por sldb 6f14a3b5. Al pasar un directorio target existente a ser `FileNode` con `file_kind: directory`, `_directory_materialization_targets` en `deskops/services/closure.py` deja de considerarlo (solo mira inválidas) y los archivos bajo él no reciben link, provocando `missing_changed_file_link`.

Resultado esperado: que una materialization cuyo `target_identity` es directorio cubra los archivos bajo él (`target_covers`) tanto si sldb lo reporta missing (viejo) como nodo del grafo (nuevo); un hermano con prefijo parecido (`pkg/subzero.py`) sigue sin cubrirse.

Límites: dentro, `closure.py` (`_changed_file_link_evidence`, `_directory_materialization_targets` o helper nuevo) y `tests/test_materialization_targets_outside_package.py` si hace falta; fuera, sldb.

## AMBIGUEDADES

1. «el sldb del venv (el de herramientas, que ya trae 6f14a3b5)» — no indica ruta ni activación del venv; obligaría a inventar el entorno.
2. «usar target_covers igual que con las inválidas» — no define firma ni si se reutiliza helper; obligaría a inventar la API.
3. «agregar un test que lo cubra con el nodo de directorio presente si el actual no lo distingue» — no fija criterio de distinción; obligaría a inventar el umbral.
4. «CHANGELOG, commit con rutas nombradas y Task-Id» — no especifica formato de entrada ni del Task-Id; obligaría a inventar convención.
5. «Un hermano con prefijo parecido (pkg/subzero.py) sigue sin cubrirse» — no aclara si debe añadirse aserción nueva o solo preservarse la existente.

## DRY-RUN

Lecturas: TaskDoc, `closure.py`, test citado, API de sldb para nodos de archivo. Cambios previstos: rama en `closure.py` que, para materializations válidas con arista a nodo `file_kind directory` (o target_identity directorio existente), aplique `target_covers` como en inválidas; posible test adicional. Dependencias: sldb 6f14a3b5 en el venv, pytest. Validación futura: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_materialization_targets_outside_package.py`. Sin ejecutar nada.

## FUTURO

Otro nodo ejecuta p1–p4, el commit y el CHANGELOG; un humano decide el formato del Task-Id/CHANGELOG y si ampliar el test.
