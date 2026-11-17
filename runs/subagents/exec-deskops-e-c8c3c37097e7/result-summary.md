# result-summary — run-deskops-e-c8c3c37097e7

- run_id: run-deskops-e-c8c3c37097e7
- task: task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y
- session: scion://agent/deskops-e-c8c3c37097e7 (agente claude; session_sha256: no disponible desde el contenedor)
- Sin commits. Evidencia en este directorio (no en `runs/subagents/project-graph-<fecha>/` del scope: el brief manda este run dir).

## Resultado

- **H2 migrado.** La superficie `issue` (`desk/drawer/issues`) declara `closed=CLOSED_ISSUE`, un predicado del lenguaje de reglas
  de sldb: `status ~ "(?i)^\s*["']*closed:*(\s|["']*\s*$)" or Status ~ …`, que reproduce la normalización de
  `deskops.services.issues._frontmatter_status` (mayúsculas, comillas, dos puntos finales, palabras detrás). `_closed_issue` y
  `closed_document=` desaparecen; la config ya vuelca como datos (`to_mapping()` no falla).
- **H1 no declarable → se conserva `declared_target_is_a_file`** (rama "o hay nota a sldb" del done_when). `MATERIALIZATION_TARGETS`
  (desk/materializations, `target_identity`) ya estaba declarado. Los destinos que hoy filtra la excepción en el desk real (medidos uno a uno)
  no salen de un campo escalar de frontmatter fuera de exclusiones:
  1. `references:` de desk/tasks (lista) → ~28 notas `desk/inbox/*.md`. `DeclaredFileTargets` solo lee un str.
  2. Menciones en el cuerpo (LineMentions): `tests/e2e_agent/scenarios/inbox-to-task.yaml`, `tests/fixtures/model_contract_hashes.json`, `dag.yaml` de los planes.
  3. `target_identity` de materializaciones bajo `tests/fixtures` (goldens de ayuda, `scaffold/update.json`, `model_contract_hashes.json`): `DeclaredTargetNodes` los descarta por `FileExclusions`.
  No hay otra carpeta del desk con un campo escalar que nombre archivos y sea campo de referencia del grafo (las de `provenance` no son ReferenceField).
  Nota enviada: `../sldb/desk/inbox/20261117-080724-suggestion-project-graph-de-deskops-destinos-de-h1-que-declaredfiletargets-no-puede-declarar-y-closed-sin-cuerpo-h2.md` (trackeada en el store de sldb; sin commitear allí).

## Archivos tocados

- `deskops/graph/desk_graph.py`: `CLOSED_ISSUE` + `closed=` en la superficie issue; borra `_closed_issue` y `closed_document=`.
- `deskops/graph/checks.py`: solo el docstring de `declared_target_is_a_file` (por qué se queda, con los tres casos).
- `tests/test_graph_declared_edges.py`: test parametrizado del `closed:` (closed / "Closed: fixed" / 'closed' / open / closed-ish) y test de que la config no tiene callable y vuelca como datos.
- `tests/test_graph_checks.py`: test que fija los tres casos H1 no declarables (lista, cuerpo, tests/fixtures) y que un archivo inexistente sí se reporta.
- **Fuera de `files`:** `tests/test_graph_cli.py` (`test_graph_missing_treats_a_closed_issue_as_a_record`): el issue de prueba tenía el estado en una sección `## Status` del cuerpo; `closed:` evalúa el payload (frontmatter), así que pasó a `status:` en frontmatter. Sin ese cambio el caso `closed` fallaba (1 != 0).

## Validación (ver validation.log)

| comando | resultado |
|---|---|
| pytest tests/test_graph_checks.py | 5 passed, rc=0 |
| pytest tests/test_graph_declared_edges.py | 12 passed, rc=0 |
| pytest tests/test_graph_cli.py (extra, por el cambio fuera de files) | 18 passed, rc=0 |
| pytest tests/test_graph_missing_existing_files.py, tests/test_graph_store_index_not_nodes.py (extra) | 7 + 3 passed |
| deskops graph missing --root . vs graph-missing-antes.txt | mismo conjunto de líneas (diff vacío), 49 entradas, rc=1 antes y después |
| ! grep declared_target_is_a_file\|_closed_issue deskops | `_closed_issue` vacío; `declared_target_is_a_file` queda (checks.py:52, :63) por H1 no declarable, cubierto por la nota a sldb |
| suite completa `pytest -n 4 -q tests` + comparación con origin/main | **para el integrador** (orden del brief: no se corre aquí) |

tests/test_command_registry.py no aplica: no cambió ningún comando del CLI.

## Riesgos

- **Pérdida de alcance de H2:** un issue cuyo estado vive solo en una sección `## Status` o en una línea `Status:` del cuerpo (formas que
  `deskops issue` acepta) deja de contar como historia en el grafo; ahora solo cuenta el `status:`/`Status:` del frontmatter. Hoy no hay
  ningún archivo en `desk/drawer/issues` en ninguno de los 6 desks del ecosistema, así que el efecto actual es nulo. Avisado a sldb en la misma nota. Reversible.
- `deskops/services/references.py` (fuera de scope) dice en su docstring que la config "holds a callable (closed_document)"; ya no es cierto
  (la config es datos). No se tocó; queda como seguimiento posible (declarar project_graph en store.yaml está fuera de scope de esta tarea).
- El venv resuelve sldb desde /mnt/ssd/herramientas/sldb (no el hermano ../sldb); el lenguaje `closed:` está en ambos.
