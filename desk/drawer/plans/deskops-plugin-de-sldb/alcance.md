# Alcance: qué se mueve y adónde

## Desacuerdos entre ritos y código (F3)

| Id | Desacuerdo | Dónde |
|---|---|---|
| W1 | Nombres de nodos y estados no calzan con los ritos (`task_activates` deja la implementación en `ritual-testing`; `task_hands_to_closeout` escribe `ready_for_testing`). | `desk/lifecycle/*`, `deskops/data/lifecycle/` |
| W2 | `next_actions` de `deskops/spec/workflows/task_lifecycle.yaml` contradice `desk/rituals/closeout.md` y `execution.md`. | YAML del paquete |
| W3 | `closeout commit` fuerza `current_node = ritual-closeout` y no toma la arista `task_completes`: una tarea en ejecución con recibos podría cerrarse. | `services/closure.py` `closeout_rule_findings` |
| W4 | Las compuertas de cierre solo corren si la tarea está en el Board; ninguna regla lo dice. | `services/closure.py` `_close` |
| W5 | supersede, resolved-by y retire escriben `status` e `history` directo, sin aristas. | `services/closure.py` `_record_closing_status`, `models/task_lifecycle.py` |
| W6 | El validador de coherencia lee el grafo del paquete, no el del desk. | `models/task_lifecycle.py` |
| W7 | Compuertas que existen solo en Python: `_closeout_link_gate`, `_changed_file_link_evidence`, `_skill_guard_test_evidence`, `_generated_artifact_source_finding`. | `services/closure.py` |

## Módulos (F2 mala adaptación, F3 dato, F4 a sldb)

| Módulo | Destino |
|---|---|
| `services/references.py` | APIs públicas de sldb (`rewrite_references` con grafo y `excluded_sources`) |
| `doc_access.py` | guarda lossy, `select_documents` y template anchors de sldb |
| `services/atoms.py` | `rewrite_references` + `transaction` de sldb; las citas a archivos esperan el pedido ya abierto en sldb |
| `cli/commands/message.py` | `create_document`, `sldb inbox`, `fields update`; wake queda propio |
| `bootstrap.py`, `workspace.py`, `cli/commands/desk.py` | `stores init/add/build`, `models add`, scaffold de sldb |
| `atom_tags.py`, `domain_tree.py`, `tag_migration.py`, `tag_vocabulary.py` | namespaces de tags de sldb (`tags.md`) |
| `identity.py` | catálogo de stores por nombre (pedido C7) |
| `doctor_findings.py` | `sldb stores check` + reglas |
| `cli/registry.py` (CRUD) | `sldb docs create/list/show`, `fields update`; queda un CLI delgado |
| `services/closure.py` (snapshot/restore) | `transaction` de sldb; la parte git queda propia |
| `graph/self_reflection.py` | RuleDoc `on_check` |
| `graph/desk_graph.py` `EXCLUSIONS` | `project_graph` en `store.yaml` |
| `services/drawer.py`, `services/issues.py` | modelos trackeados (TaskDoc `deferred`, IssueDoc) |
| `cli/commands/view.py` H4–H8 | ViewDocs sobre inbox, drawer y recibos trackeados |
| `data/rules/closeout-evidence.yaml` | se borra: el piso sale de las RuleDoc |
| `lifecycle.py` (advance, siembra) | primitiva "tomar transición" (C2) y reglas enlazadas (C1) |
| `absolute_paths.py`, `cli/model_introspection.py` | sldb (C6, C9) |

## Queda propio

`dispatch.py`, `runtime/scion.py` (salvo la prosa de `_render_*_agents_md`, que pasa a dato), `integrate.py`, `queue.py`,
`runtime/herdr.py`, la parte git de `services/closure.py`, el lanzador de `services/review.py`, `wake.py`,
`lifecycle_hooks.py` (ejecutor), `materializers/*` y un CLI delgado.

## Pedidos nuevos a sldb (F4)

C1 reglas y aristas de un store enlazado; C2 primitiva "tomar transición"; C3 reglas sobre el último elemento de una lista;
C4 momento `on_delete`; C5 extensión del CLI de sldb; C6 rutas absolutas en campos de referencia; C7 catálogo de stores por
nombre; C8 chequeo store-árbol para pre-commit/CI; C9 creación de documentos desde el esquema del modelo.
Ya pedidos en sldb (no se repiten): vistas H1–H8 y herencia H6, "sldb escucha" (eventos), hook Write/Edit, rule-graph en frío,
`models validate` de deskops, `declaredfiletargets`, `stores check` por modelo, rutas de archivo como extremo de RelationDoc,
versionar sldb.
