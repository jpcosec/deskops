PASA

# Veredicto del tester

El commit del ejecutor cumple el Goal, la Validation y el Done When de la tarea.

## Commit evaluado

- Commit: `b3b40a14d8376b2add3df1dac9001c1f5fc4d66c`
- Mensaje: `graph export y self_reflection escriben en .sldb_cache (DERIVED_ROOT)`
- Trailer: `Task-Id: task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime`
- Archivos:
  - `deskops/graph/paths.py` (nuevo, `DERIVED_ROOT = Path(".sldb_cache")`)
  - `deskops/graph/export.py`
  - `deskops/graph/self_reflection.py`
  - `tests/test_graph_snapshot.py`
  - `tests/test_graph_self_reflection.py`
  - `tests/test_output_goldens.py`
  - `tests/fixtures/golden/graph_snapshot.kg.json`
  - `tests/fixtures/golden/self_reflection_findings.json`

El código del working tree coincide con el commit (`git diff b3b40a14 -- deskops tests` vacío). Existe un commit equivalente en el worktree del ejecutor (`78867dfe`) con el mismo cambio.

## Pruebas ejecutadas

El `.venv` de `/mnt/ssd/proyectos/SLDB_1` está roto en este contenedor: sus binarios apuntan a un Python 3.12 ausente y `python` resuelve a 3.11 sin pytest. Para no modificar el repo, corrí los tests con el Python 3.12.16 instalado por `uv`, usando el `site-packages` del `.venv` del proyecto y el `sldb` sibling en `PYTHONPATH`:

```bash
PY=/home/scion/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12
SP=/mnt/ssd/proyectos/SLDB_1/.venv/lib/python3.12/site-packages
export PYTHONPATH="$SP:/mnt/ssd/proyectos/SLDB_1/sldb/src"

TMPDIR=/tmp $PY -m pytest -q tests/test_graph_snapshot.py        # 10 passed
TMPDIR=/tmp $PY -m pytest -q tests/test_graph_self_reflection.py #  2 passed
TMPDIR=/tmp $PY -m pytest -q tests/test_output_goldens.py        #  7 passed (377 s)
TMPDIR=/tmp $PY -m pytest -q tests/test_gitignore_policy.py      #  2 passed
TMPDIR=/tmp $PY -m pytest -q tests/test_graph_cli.py             # 18 passed
```

No hay `tests/test_<modulo>.py` para `paths.py` ni `export.py`; `test_graph_snapshot.py`, `test_graph_self_reflection.py` y `test_graph_cli.py` cubren los módulos tocados. No corrí la suite completa, según la instrucción del tester.

## Validation

```text
$ grep -rnF '.sldb/runtime' deskops/ --include=*.py
deskops/graph/self_reflection.py:40:    ".sldb/runtime/",
deskops/graph/desk_graph.py:91:    path_prefixes=(".sldb/runtime", ".sldb/core/documents", ".sldb_cache", "tests/fixtures"),
```

Las dos únicas menciones son de exclusión (filtros de fuentes), no de escritura. Las salidas ahora son:

- `.sldb/runtime/graphs/deskops.kg.json` -> `.sldb_cache/graphs/deskops.kg.json`
- `.sldb/runtime/self_reflection_findings.json` -> `.sldb_cache/self_reflection_findings.json`
- `.sldb/runtime/self_reflection_decisions.json` -> `.sldb_cache/self_reflection_decisions.json`

`self_reflection.py` además suma `.sldb_cache/` a `EXCLUDED_SOURCE_PREFIXES`, como pedía el bundle-2. `.gitignore` ya ignora `.sldb_cache/`.

## Pill

`desk/contexts/pill-010-graph-runtime-output-policy.md:42` ahora dice que las salidas derivadas van a `.sldb_cache/` y que se toma de `deskops.graph.paths.DERIVED_ROOT`; el `.sldb/core/documents/PillDoc/...yaml` correspondiente está actualizado con el nuevo hash. El cambio de pill está en el working tree sin commitear (cambio de desk para el closeout), y el código de la tarea sí está commiteado.

## Consumidores

Busqué el literal `.sldb/runtime` en todo `/mnt/ssd/proyectos/SLDB_1` excluyendo `runs/`, `.git` y `node_modules`, y busqué por nombre los derivados (`deskops.kg.json`, `self_reflection_findings.json`, `self_reflection_decisions.json`) en código fuera de `deskops/`.

No hay consumidor real: los hits externos son docstrings sobre stores ajenos (`UIs/graph_ui/tests/test_sldb_end_to_end.py`), fixtures de tests que crean su propio `knowledge_graph.kg.json` legado (`spec2viz/tests/test_deskops.py`, `IR/tests/visual/test_catalog.py`) y metadata/docs. Ningún código fuera de deskops abre los derivados de graph export/self_reflection bajo la ruta vieja, así que no correspondía enviar `deskops message send`, consistente con la resolución del preflight-3.

## Observaciones no bloqueantes

- `docs/operator-manual.md:1258` y `.opencode/skills/use-kgdb/SKILL.md` (sección "Output policy") todavía mencionan `.sldb/runtime/` como destino de escritura. No son código ni consumidores y quedan fuera del Scope/Done When de esta tarea; conviene actualizarlos en una tarea documental aparte.
- El nombre del test `test_write_graph_snapshot_uses_ignored_runtime_path` conserva la palabra "runtime" pero ya verifica `.sldb_cache/`; no afecta el comportamiento.
