# REFORMULACION

**Propósito:** que `closeout verify` no emita `generated_artifact_missing_declared_sources` para archivos bajo `tests/fixtures/`, donde un `.json`/`.md` con `.yaml`/`.yml`/`.mmd` hermano son goldens independientes y no proyecciones generadas.

**Resultado:** `_generated_artifact_source_finding` (o `_find_generated_artifact_source_sibling`) en `deskops/services/closure.py` (~línea 1583) excluye rutas bajo `tests/fixtures/`; fuera de ahí el chequeo no cambia. Dos tests nuevos en `tests/test_closeout_declared_evidence.py`.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops` (`deskops/services/closure.py`, `tests/test_closeout_declared_evidence.py`).

**Límites:** solo `tests/fixtures/`; fuera de alcance la regla para docs, diagramas y artefactos fuera de esa ruta.

# AMBIGUEDADES

1. "Bajo tests/fixtures/ el json y el yaml son dos goldens independientes" — el input no define criterio de detección (prefijo de ruta exacto, `Path.parts`, relativo a raíz de repo o de desk). Obliga a inventar el mecanismo de exclusión.
2. "Excluir las rutas bajo tests/fixtures/" — no aclara si aplica a rutas absolutas, a `files` relativas al repo, ni si cubre subdirectorios arbitrarios. Obliga a inventar normalización.
3. "los dos tests nuevos pasan" — no especifica nombres ni si sustituyen/conviven con los existentes de `test_closeout_declared_evidence.py`. Obliga a inventar nomenclatura y placement.

# DRY-RUN

**Lecturas:** `deskops/services/closure.py` (`_generated_artifact_source_finding`, su llamador y helper de hermanos); `tests/test_closeout_declared_evidence.py` (fixtures `repo`, `_write_declared_task`); `tests/test_closeout.py` (helpers `_git`, `_write`, `_write_board`).

**Cambios previstos:** guard temprano en la función de detección que retorne `None` si la ruta está bajo `tests/fixtures/`; dos tests con sandbox `tmp_path`: (a) par `tests/fixtures/golden/output/*.json` + `.yaml` en `files` no produce hallazgo; (b) `.md` con `.yaml` hermano fuera de `tests/fixtures/` sí lo produce.

**Dependencias:** fixtures de `lifecycle_desk`, `store_repo`, `track_task`; CLI `python -m deskops`; git local del sandbox.

**Validaciones futuras (no ejecutadas):** los dos comandos pytest de la sección Validation; commit descriptivo según `atom-code-changes-close-with-tests-and-commit`; escrituras solo en sandbox según `atom-cli-mutation-testing-uses-sandbox-desk-roots`.

# FUTURO

Decisión humana: criterio exacto de "bajo tests/fixtures/". Nodo posterior: ejecución de tests y commit de cierre; `closeout verify` real sobre la tarea de ack --reason (97649c61) para confirmar desbloqueo del gate `atom|materialization`.
