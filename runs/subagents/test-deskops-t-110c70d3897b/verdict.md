# Veredicto del tester deskops-t-110c70d3897b

- task: task-deskops-declara-su-project-graph-con-closed-y-declared-file-targets-de-sldb-y-borra-los-desvios-h1-y
- role: tester (agente claude, sesión fresca); run_id: run-deskops-t-110c70d3897b; session: scion://agent/deskops-t-110c70d3897b; session_sha256: no disponible
- entrega revisada: diff sin commitear en deskops/graph/desk_graph.py, deskops/graph/checks.py, tests/test_graph_checks.py, tests/test_graph_declared_edges.py, tests/test_graph_cli.py (fuera de files) sobre HEAD fcb98cdb

## Contrato vs entrega

| done_when / goal | evidencia | estado |
|---|---|---|
| H2: closed: en vez de closed_document=_closed_issue | desk_graph.py:52-53 (CLOSED_ISSUE), :61 (closed= en la superficie issue); _closed_issue y closed_document= borrados; `grep -rn _closed_issue deskops` vacío | OK |
| declared_file_targets declarado | MATERIALIZATION_TARGETS (desk_graph.py:96, :196) ya existía; no hay otra carpeta con campo escalar declarable | OK |
| H1 desaparece o nota a sldb | declared_target_is_a_file sigue (checks.py:52, :63) con docstring de los 3 casos; nota ../sldb/desk/inbox/20261117-080724-suggestion-...md existe con rutas y referentes (lista references:, menciones de cuerpo, target_identity bajo tests/fixtures excluido) | OK por la rama "o hay nota a sldb" |
| graph missing igual | 149 líneas antes y después, diff por conjunto (sort) vacío, rc=1 en ambos | OK |
| tests pasan | test_graph_checks 5, test_graph_declared_edges 12, test_graph_cli 18, test_graph_missing_existing_files 7: todos passed, rc=0 | OK |

## Reproducción contra HEAD (copia en /dev/shm, ya borrada)

- test_graph_declared_edges.py: error de colección (no existe CLOSED_ISSUE); con stub, falla `test_the_desk_graph_config_is_data_with_no_closed_document_callable` (`<function _closed_issue> is None`). El test rojo de H2 es real.
- test_graph_checks.py (nuevo test H1) y el parametrizado de closed: pasan en HEAD: son guardas de no-regresión del comportamiento conservado, no tests rojos. Coherente con que H1 se conserva y H2 conserva semántica en frontmatter.

## Cambio en tests/test_graph_cli.py (fuera de files)

Sí es cambio de comportamiento: un issue con el estado solo en `## Status` o en una línea `Status:` del cuerpo deja de contar como historia (sus faltantes pasan de informativos a faltantes). Impacto real hoy nulo: no existe desk/drawer/issues en deskops (HEAD tampoco lo trackea) y en el ecosistema solo hay UIs/graph_ui/desk/drawer/issues, que no tiene ningún .md (solo assets/). La pérdida está declarada en result-summary y en la nota a sldb. Aceptable y reversible.

## Hallazgos (no bloqueantes)

1. desk_graph.py:52-53 — el predicado no es exactamente la condición de _closed_issue: `_frontmatter_status` (deskops/services/issues.py:136-141) acepta la clave status con cualquier capitalización (STATUS, sTaTuS); CLOSED_ISSUE solo `status`/`Status`. Además un valor con comillas internas y espacio (`"' closed'"`) cierra para issue_status y no para el predicado. Diferencial: 14/66 casos, todos raros; sin issues reales afectados. El comentario de desk_graph.py:47-51 dice "status (or Status)", así que no miente, pero "(case, quotes...)" sugiere paridad total. Seguimiento opcional: añadir `or STATUS ~ ...` o documentar la diferencia.
2. deskops/services/references.py:5 — docstring dice que la config "holds a callable (closed_document)"; ya es falso. Fuera de files; seguimiento.
3. El run dir del ejecutor no es runs/subagents/project-graph-<fecha>/ como dice el scope; lo justificó por orden del brief. Formal.
4. Suite completa no corrida (orden del brief); queda para el integrador.

VEREDICTO: APROBADO
