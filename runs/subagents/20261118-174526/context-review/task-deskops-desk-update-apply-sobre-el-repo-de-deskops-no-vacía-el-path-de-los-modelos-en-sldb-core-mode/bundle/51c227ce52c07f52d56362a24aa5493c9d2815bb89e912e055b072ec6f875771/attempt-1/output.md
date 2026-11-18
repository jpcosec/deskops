## REFORMULACION

**Propósito:** en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, corregir `deskops desk update --apply` para que no vacíe `path` en `.sldb/core/models/*.yaml` y no escriba relation types no declarados por el paquete deskops.

**Resultado:** reproducción documentada en el run dir; test en `tests/test_desk_sync.py` que falle antes y pase después; arreglo localizado con archivo y línea; CHANGELOG; `result-summary.md`.

**Límites:** no cambiar el layout de `.sldb`; el ejecutor corre solo `tests/test_desk_sync.py` y tests de archivos tocados; la suite completa la corre integrate. El informe debe incluir `git diff --stat` y `git diff -- .sldb/core/models sldb/relation_types` de la copia limpia.

## AMBIGUEDADES

1. “con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra”: el input no incluye rituales, pills, átomos ni archivos resueltos. Obligaría a inventar qué elementos aplicar y en qué orden.
2. “git -C /tmp/repro checkout --detach <HEAD>”: no se fija el hash concreto. Obligaría a inventar o sustituir `<HEAD>` por el HEAD disponible, que podría no coincidir con “el momento del despacho”.
3. “los tests de los archivos que toque”: no se enumeran esos archivos ni su selección. Obligaría a inventar el perímetro exacto de pruebas.
4. “si reltype-links_to y el cambio de has_model.md están declarados”: no se aporta la ruta ni el contenido de la declaración. Obligaría a inventar la fuente de verdad si no se inspecciona el repo.

## DRY-RUN

Sin ejecutar: leer TaskDoc, `.sldb/store.yaml`, código de `desk update`, `tests/test_desk_sync.py`, declaraciones de relation types y CHANGELOG. Crear copia limpia en `/tmp/repro`, ejecutar `deskops desk update --apply --root /tmp/repro` y capturar diffs. Añadir test con `tmp_path` y helper existente: store con modelo de `path` local; tras `--apply`, el path debe permanecer. Localizar y corregir la escritura que vacía `path`; condicionar la escritura de relation types a lo declarado. Actualizar CHANGELOG y `result-summary.md`. Dependencias: git, pytest, TMPDIR, repo accesible. Validaciones futuras: test nuevo falla antes y pasa después; diff reproducible sin cambios en modelos; `TMPDIR=/tmp python -m pytest -q tests/test_desk_sync.py`; tests de archivos tocados.

## FUTURO

Integrate ejecuta la suite completa y valida el conjunto. Un humano decide commit/merge, acepta el tratamiento de relation types y confirma que la evidencia de reproducción satisface el encargo.
