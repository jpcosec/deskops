## REFORMULACION

El encargo es una tarea de código ejecutable —no un agregado ni un paquete— en el repo `SLDB_1/deskops`. Propósito: evitar que `closeout verify` emita `generated_artifact_missing_declared_sources` para goldens/fixtures bajo `tests/fixtures/`, donde un `.json` y un `.yaml` hermanos son dos goldens independientes y no una proyección renderizada. Resultado esperado: ajustar `_generated_artifact_source_finding` —o `_find_generated_artifact_source_sibling`— en `deskops/services/closure.py` y añadir cobertura en `tests/test_closeout_declared_evidence.py`, de modo que el gate `atom|materialization` deje de bloquearse. Límites: solo esa regla y esos tests; fuera de `tests/fixtures/` el chequeo permanece igual; no se abordan docs, diagramas ni artefactos externos.

## AMBIGUEDADES

1. «para archivos bajo `tests/fixtures/` (goldens y fixtures de test)» frente a «un par json/yaml bajo `tests/fixtures/golden/output/`». ¿La exclusión cubre todo `tests/fixtures/` o solo `golden/output/`? Obliga a inventar el alcance exacto del guard.
2. «Los dos tests nuevos pasan» frente a la Validation, que lista dos archivos de test, no dos casos nuevos. Obliga a inventar si son dos casos dentro de un archivo, uno por archivo o más.
3. «Excluir las rutas bajo `tests/fixtures/`» no precisa si se compara ruta relativa al repo, absoluta o por componente. Obliga a inventar la normalización.

## DRY-RUN

Lecturas previstas: `deskops/services/closure.py` alrededor de la línea 1583, definición y llamadas de `_generated_artifact_source_finding`/`_find_generated_artifact_source_sibling`; `tests/test_closeout_declared_evidence.py`; referencias a sandbox `tmp_path`. Cambios previstos: añadir un guard temprano que omita el hallazgo cuando la ruta normalizada esté bajo `tests/fixtures/`; añadir dos casos pytest en sandbox: par `.json`/`.yaml` bajo `tests/fixtures/golden/output/` sin hallazgo y `.md` con `.yaml` hermano fuera de `tests/fixtures/` con hallazgo. Dependencias: pytest, entorno `PYTHONPATH` y `TMPDIR`, utilidades de sandbox existentes. Validaciones futuras, sin ejecutar: los dos comandos pytest de la sección Validation.

## FUTURO

El ejecutor producirá el parche y los tests; otro nodo ejecutará las validaciones y el cierre. Un humano decidirá cualquier precisión de alcance si persiste la ambigüedad.
