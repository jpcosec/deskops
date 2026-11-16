# Result summary — deskops-e-4ba5a0d9443c (intento 1)

- run_id: run-deskops-e-4ba5a0d9443c
- task: task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-y-reconoce-los-specs-yaml-sincronizados
- session: scion://agent/deskops-e-4ba5a0d9443c (agente claude; la sesión la registra el lanzador)
- session_sha256: (no disponible desde dentro de la sesión)

## Cambios (todos dentro de `files` del TaskDoc)

- `deskops/graph/desk_graph.py`: la FileRule de kind `spec` pasa de `path_prefixes=("spec", "docs/architecture/spec2viz")` a `path_prefixes=("spec", "docs/architecture")`. Sufijos `_SPEC` (.md, .yaml, .yml) y orden de FILE_RULES sin cambios (precisión preflight 1: ensanchamiento intencional, Markdown incluido; precedencia FileRules/DocumentSurfaces sin tocar).
- `tests/test_graph_extract_sources.py`: test nuevo `test_extract_source_file_nodes_reads_spec_yaml_under_docs_architecture` sobre desk sandbox `tmp_path`: `docs/architecture/diagrams/desk-flow.yaml` se extrae como `spec:docs/architecture/diagrams/desk-flow.yaml` con kind `spec` y file_kind `spec`; `spec/artifacts/atom.yaml` sigue con file_kind `spec`. El test existente de `spec/artifacts/atom.yaml` sigue en verde sin modificarse.

No se movió ni renombró ningún archivo; no se tocó desk/ ni .sldb/ (los cambios de .sldb/ y runs/subagents/2026* en git status son previos, de otras sesiones/lanzador).

## Validación (ver validation.log)

| Comando | Resultado |
|---|---|
| pytest -q tests/test_graph_extract_sources.py | 17 passed, rc 0 |
| pytest -q tests/test_graph_snapshot.py | 10 passed, rc 0 |
| pytest -q tests/test_graph_missing_existing_files.py | 7 passed, rc 0 |
| grep -n spec2viz deskops/graph/desk_graph.py | sin coincidencias, rc 1 |

Suite completa y `stores build --check`: no corridos por orden del brief — para el integrador.

## Riesgos

- El ensanchamiento hace que cualquier .md/.yaml/.yml bajo `docs/architecture/` sea nodo `spec` vía FileRule; además los .md de docs siguen siendo DocumentSurface `doc` (precedencia sin cambios, por precisión del coordinador). deskops no tiene `docs/architecture` hoy, así que el grafo real no cambia.
