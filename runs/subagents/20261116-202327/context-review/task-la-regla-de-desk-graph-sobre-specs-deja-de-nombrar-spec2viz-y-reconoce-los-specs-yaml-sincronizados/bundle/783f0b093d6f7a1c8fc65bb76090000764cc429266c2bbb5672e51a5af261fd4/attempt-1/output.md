REFORMULACION
Propósito: que la FileRule de kind `spec` en `deskops/graph/desk_graph.py` deje de nombrar `docs/architecture/spec2viz` y reconozca los specs YAML sincronizados con `sldb notations sync`. Resultado: `path_prefixes=("spec", "docs/architecture")`, sin cambios en sufijos `_SPEC` ni en el orden de `FILE_RULES`, más un test en `tests/test_graph_extract_sources.py` sobre un desk sandbox (`tmp_path`) que extraiga un YAML bajo un subdirectorio de `docs/architecture` como nodo `spec` con `file_kind spec`, manteniendo verde la aserción existente sobre `spec/artifacts/atom.yaml`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: entran solo esa FileRule y su test; salen habilidades de agente, `render_diagram.py`, el `DocumentSurface` de kind spec, la detección semántica de sincronización y cualquier otro archivo.

AMBIGUEDADES
1. "su test en tests/test_graph_extract_sources.py": no se nombra la función de test; obligaría a inventar su nombre y ubicación exacta dentro del archivo.
2. "un YAML creado en un subdirectorio de docs/architecture del sandbox": no se fija qué subdirectorio ni nombre de archivo; obligaría a inventar la ruta concreta del fixture.
3. "los tres archivos de test de la Validation pasan": se citan `test_graph_snapshot.py` y `test_graph_missing_existing_files.py`, no listados en `files`; no aclara si basta ejecutarlos o si se espera tocarlos si fallan. Obligaría a decidir si modificarlos.

DRY-RUN
Lecturas: `deskops/graph/desk_graph.py` (FILE_RULES, `_SPEC`, extractores) y `tests/test_graph_extract_sources.py` (helper `write`, test de `spec/artifacts/atom.yaml`). Cambios previstos: sustituir `"docs/architecture/spec2viz"` por `"docs/architecture"` en la FileRule de spec; añadir una función de test en el archivo existente que escriba un YAML bajo `docs/architecture/<subdir>/` en `tmp_path` y afirme el nodo `spec:<ruta>` con `file_kind == "spec"`. Dependencias: `pytest`, `sldb.api.edges.project_graph`, entorno `../.venv`. Validaciones futuras (no ejecutadas): los tres `pytest -q` de la sección Validation y `grep -n spec2viz deskops/graph/desk_graph.py` con rc 1.

FUTURO
Un humano (JP) ya decidió la subordinación del YAML al grafo; otro nodo/IR13 ejecutará habilidades y `render_diagram.py`; el commit descriptivo lo exige el átomo `atom-code-changes-close-with-tests-and-commit`; el archivo de spec2viz depende de que specir retirement check salga 0; el renombrado de la ruta `docs/architecture/spec2viz` se pide al desk de deskops.
