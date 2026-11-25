## REFORMULACION
Propósito: corregir una regresión en `deskops` introducida por sldb 6f14a3b5: un directorio target declarado como materialization pasó a ser `FileNode` con `file_kind: directory`, dejó de ser materialization inválida y `closure.py` ya no aplica `target_covers`, por lo que `verify` reporta `missing_changed_file_link`. Resultado: los archivos bajo un directorio target quedan cubiertos con sldb viejo y nuevo, sin cubrir prefijos hermanos como `pkg/subzero.py`. Repo: `deskops`; superficie: `deskops/services/closure.py` (`_changed_file_link_evidence`, `_directory_materialization_targets` o helper nuevo) y `tests/test_materialization_targets_outside_package.py`. Límites: fuera `sldb`; incluye CHANGELOG, commit con rutas nombradas y `Task-Id`.

## AMBIGUEDADES
1. “su test … si hace falta ampliarlo” y “agregar un test … si el actual no lo distingue”: no define cuándo es obligatorio añadir cobertura; obligaría a inventar el criterio de suficiencia.
2. “para cada materialization válida cuyo arista apunta a un nodo de archivo con file_kind directory (o cuyo target_identity declarado es un directorio existente)”: no fija la fuente de verdad ni el tratamiento de symlinks/rutas relativas; obligaría a inventar semántica de detección.
3. “los dos casos” de `test_closeout_verify_covers_files_under_a_directory_target`: no los enumera; obligaría a inferir qué parametrizaciones cuentan.
4. “commit con rutas nombradas y Task-Id”: no especifica formato del mensaje ni si el commit lo hace este nodo; obligaría a inventar convención.

## DRY-RUN
Lecturas: TaskDoc, `closure.py`, test citado, modelos/evidencia de materialization y CHANGELOG. Cambios previstos: extender la condición que aplica `target_covers` a materializations válidas con target directorio; ajustar/añadir test para cubrir el nodo directorio y preservar el caso `pkg/subzero.py`; actualizar CHANGELOG. Dependencias: venv de herramientas con sldb 6f14a3b5 y deskops 7e8492ea. Validación futura: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_materialization_targets_outside_package.py`. Nada ejecutado.

## FUTURO
El ejecutor producirá el diff y el commit; el validador ejecutará pytest; un humano decidirá si la cobertura añadida y el mensaje de commit cumplen la convención. No es un nodo agregado.
