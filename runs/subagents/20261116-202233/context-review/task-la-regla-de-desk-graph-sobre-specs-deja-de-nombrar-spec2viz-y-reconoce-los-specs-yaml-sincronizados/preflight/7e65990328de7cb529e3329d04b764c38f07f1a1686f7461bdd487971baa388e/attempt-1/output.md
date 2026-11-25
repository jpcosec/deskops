## REFORMULACION

**Propósito:** actualizar la FileRule de kind `spec` en `deskops/graph/desk_graph.py` para que deje de nombrar `spec2viz` y reconozca specs YAML bajo `docs/architecture`, conforme a la decisión de JP del 2026-11-15.

**Resultado:** `path_prefixes` pasa de `("spec", "docs/architecture/spec2viz")` a `("spec", "docs/architecture")`; los sufijos y el orden de `FILE_RULES` no cambian. Se añade cobertura en `tests/test_graph_extract_sources.py` usando un desk sandbox (`tmp_path`): un YAML bajo un subdirectorio de `docs/architecture` se extrae como nodo `file_kind spec`, y la aserción existente sobre `spec/artifacts/atom.yaml` sigue en verde.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`.

**Límites:** solo la FileRule y su test. Fuera: habilidades de agente y `render_diagram.py`, el `DocumentSurface` de kind spec y cualquier detección semántica de sincronización; el reconocimiento es por ruta.

## AMBIGUEDADES

1. «los sufijos (_SPEC: .md, .yaml, .yml) y el orden de las FILE_RULES no cambian» frente a «un YAML de spec en cualquier subdirectorio de docs/architecture es un nodo de file_kind spec». Al ampliar el prefijo, cualquier `.md` bajo `docs/architecture` pasaría a ser spec; obliga a inventar si se deben excluir Markdown o si el ensanchamiento es intencional.
2. «spec2viz se archiva cuando specir retirement check salga con 0». Obliga a inventar si esta tarea queda bloqueada por esa comprobación o si solo es contexto.
3. «la ruta docs/architecture/spec2viz se renombra o generaliza por pedido al desk de deskops». Obliga a inventar si el ejecutor debe mover/renombrar rutas o limitarse a cambiar la regla.
4. Goal dice «sldb notations sync» y Scope dice «sldb notations sync --spec». Obliga a inventar el comando exacto y si es dependencia ejecutable.

## DRY-RUN

**Lecturas:** `deskops/graph/desk_graph.py` (FILE_RULES y clasificación), `tests/test_graph_extract_sources.py`, y los otros dos tests de Validation para conocer fixtures.

**Cambios previstos:** sustituir el prefijo; añadir un test de extracción con YAML en subdirectorio de `docs/architecture` del sandbox; conservar aserciones existentes.

**Dependencias:** `../.venv/bin/python`, `pytest`, `tmp_path`, `grep`; `TMPDIR=/dev/shm`.

**Validaciones futuras:** los tres `pytest` indicados y `grep -n spec2viz deskops/graph/desk_graph.py` con rc 1.

## FUTURO

Otro nodo o un humano debe confirmar que `specir retirement check` da 0, decidir el renombrado/generalización de la ruta `docs/architecture/spec2viz` y archivar `spec2viz`. El commit queda sujeto al átomo de cierre con tests.
