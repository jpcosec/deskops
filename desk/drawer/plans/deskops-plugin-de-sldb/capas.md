# Mapa de capas: cada módulo de deskops/ y su paquete

Fecha: 2026-11-25. Base: `diagnostico.md` (tres capas: núcleo, operación y mantenimiento, uso). Es la especificación
del paso 1 de la tarea de capas (E1). Las líneas son de `main` en `bf4dd510`.

## Los cinco paquetes

Las tres capas del diagnóstico quedan en cinco paquetes. El uso se parte en tres: lo que toca el mundo (`runtime`),
la lista única de operaciones (`operations`) y las superficies que la exponen (`surfaces`).

| Paquete | Capa | Qué contiene | Puede importar |
|---|---|---|---|
| `deskops/core` | Núcleo | Modelos (TaskDoc y demás), ciclo de vida, compuertas, vistas del núcleo (el prompt de una tarea, el Board, `next`), resolución de documentos del desk. Sin git, sin subprocesos, sin scion, sin texto de ayuda. | `sldb`, `pydantic`, stdlib |
| `deskops/ops` | Operación y mantenimiento | Que el desk esté sano: doctor, bootstrap e init, migraciones, registro de repos, tags, grafo y chequeos. | `core`, `runtime` (adaptadores como git), `sldb` |
| `deskops/runtime` | Uso (efectos) | Lo que toca el mundo: git (commit del cierre, integrate), scion, herdr, claude y pi, cola, wake. Adaptadores sin decisiones del workflow. | `core`, `sldb`, git y subprocesos |
| `deskops/operations` | Uso (contrato) | Una función por operación, la que publica MCP. Compone `core`, `ops` y `runtime`. | `core`, `ops`, `runtime` |
| `deskops/surfaces` | Uso (superficies) | `cli` (lo que quede escrito a mano: bootstrap e init), `mcp` (`register`), `view` (lo que lee la UI), render de salida. | solo `operations` (y `core` para tipos) |

Contratos de import-linter (los que valida la tarea de capas y después las guardas de E4):

1. `core` no importa `ops`, `runtime`, `operations` ni `surfaces`, ni `subprocess`.
2. `runtime` no importa `ops`, `operations` ni `surfaces`; `ops` no importa `operations` ni `surfaces` (sí puede usar los
   adaptadores de `runtime`, por ejemplo git para doctor).
3. `surfaces` importa solo `operations` (y modelos de `core`).

## Asignación por módulo

Columna **después**: lo que pasa con el módulo en una etapa posterior. "sldb" quiere decir que se reemplaza por una
API de sldb (E3) y el módulo se borra o adelgaza. La tarea de capas solo mueve; no reescribe.

### Núcleo (`core`)

| Módulo hoy | Líneas | Destino | Después |
|---|---|---|---|
| `models/*` (salvo `task_lifecycle.py`) | ~1 500 | `core/models/` | |
| `models/task_lifecycle.py` | 226 | `core/models/` | Validador a regla `on_write` (E3) |
| `lifecycle.py` | 576 | `core/lifecycle.py` | Tomar transición de sldb (pedido C2, E3) |
| `lifecycle_hooks.py` | 88 | `core/lifecycle_hooks.py` | |
| `services/tasks.py` | 368 | `core/tasks.py` | |
| `services/closeout_gates.py` | 456 | `core/gates.py` | Cláusulas de RuleDoc (E3) |
| `services/closure.py`, parte de compuertas y decisión | ~900 de 1 989 | `core/closure.py` | Cierre por arista (E3) |
| `models/task_types.py`, `task_policy.py` | 297 | `core/` | |
| `workflow/next_actions.py` | 47 | `core/` | Sale del RitualDoc (E3) |
| `doc_access.py` | 1 066 | `core/doc_access.py` | APIs públicas de sldb (E3) |
| `desk_paths.py`, `paths.py`, `slugs.py`, `errors.py`, `config.py`, `constants.py`, `doc_readability.py` | ~420 | `core/` | |
| `atom_references.py` | 88 | `core/atoms/` | |
| `services/atoms.py` (salvo split) | ~900 | `core/atoms/` | `move_document` de sldb (E3); split se borra (E1) |
| `domain_tree.py` | 311 | `core/atoms/` | |
| `services/drawer.py`, `services/issues.py`, `services/retire.py`, `services/replace.py` | 1 097 | `core/` | Inbox y drawer como modelos (E3) |
| `services/references.py` | 225 | `core/references.py` | |
| `services/review.py`, parte de recibos | ~400 de 1 104 | `core/review.py` | |
| `dispatch.py`, parte del texto del prompt | ~250 de 741 | `core/prompt.py` | Prompt como vista (E2) |
| `specs/compiler.py` | 161 | `core/specs/` | |
| `materializers/atoms.py`, `materializers/roles.py`, `materializers/runtime_profiles.py` | 300 | `core/materializers/` | |
| `foreign_files.py` | 128 | `core/` | |

### Operación y mantenimiento (`ops`)

| Módulo hoy | Líneas | Destino | Después |
|---|---|---|---|
| `doctor_findings.py`, `cli/commands/doctor.py` (lógica) | ~500 | `ops/doctor.py` | Mutación separada de error (drawer) |
| `bootstrap.py` | 472 | `ops/bootstrap.py` | `apply_declaration` de sldb (E3) |
| `workspace.py` | 1 107 | `ops/workspace.py` (scaffold) y `ops/migrations/` (las cuatro migraciones) | Migración de task_type se borra (E1) |
| `sldb_layout.py` | 50 | `ops/migrations/` | |
| `identity.py` | 338 | `ops/identity.py` | `catalog_store` de sldb (E3) |
| `cli/commands/repo.py` (lógica) | ~250 | `ops/repos.py` | |
| `atom_tags.py`, `tag_vocabulary.py`, `tag_migration.py`, `cli/commands/tags.py` | 579 | `ops/tags/` | `tag_namespaces` de sldb (E3) |
| `graph/*` (salvo `atom_trace.py`) | 1 188 | `ops/graph/` | `sldb graph project` (E3); `self_reflection.py` a `on_check` |
| `absolute_paths.py` | 326 | `ops/` | Rutas absolutas en sldb (C6) |
| `cli/commands/drift.py`, `cli/commands/materialize.py` (lógica) | 49 | `ops/` | |

### Efectos (`runtime`)

| Módulo hoy | Líneas | Destino | Después |
|---|---|---|---|
| `runtime/*` (scion, herdr, supervise, grouping, initializer, task, desk_agents) | ~1 850 | `runtime/` | `desk_agents.py` a `surfaces/view` |
| `testing/foreign_suites.py` | 84 | `deskops/testing/` (se queda: lo importan 5 tests de scion) | |
| `dispatch.py`, lanzamiento y reap | ~490 de 741 | `runtime/dispatch.py` | Despacho claude, pi y scion (drawer) |
| `services/closure.py`, git, staging y rollback | ~1 090 de 1 989 | `runtime/git_closeout.py` | |
| `services/review.py`, lanzador del revisor | ~700 de 1 104 | `runtime/review_launcher.py` | |
| `integrate.py` | 486 | `runtime/integrate.py` | |
| `queue.py` | 365 | `runtime/queue.py` | |
| `wake.py` | 43 | `runtime/wake.py` | |

### Operaciones (`operations`)

| Módulo hoy | Líneas | Destino | Después |
|---|---|---|---|
| `operations.py` | 307 | `operations/` | Herramientas MCP (E2) |
| `cli/commands/operations.py` | 378 | `operations/` (se funde con la anterior) | |

### Superficies (`surfaces`)

| Módulo hoy | Líneas | Destino | Después |
|---|---|---|---|
| `cli/main.py`, `cli/parser.py`, `cli/parse_input.py`, `cli/render.py`, `__main__.py` | ~470 | `surfaces/cli/` | CLI generado por fastmcp (E2) |
| `cli/registry.py` | 2 151 | `surfaces/cli/` | Se borra con el CLI generado (E2) |
| `cli/model_introspection.py` | 325 | `surfaces/cli/` | `describe_model_fields` de sldb (E3) |
| `cli/commands/*` restantes (atoms, closeout, core, desk, drawer, faq, graph, issue, message, promote, retire, review, runtime) | ~2 400 | `surfaces/cli/commands/` | Cada uno queda en el parseo; su lógica baja a `operations` |
| `cli/commands/view.py` | 567 | `surfaces/view.py` | |
| `about.py` | 38 | `surfaces/cli/` | |

## Lo que se borra antes de mover

La tarea de capas depende del borrado de código muerto y del retiro de `atoms split` (E1), así que no los mueve:
`graph/atom_trace.py`, `ClosureService.close_auto` (`services/closure.py:720`) y
`split_atom` (`services/atoms.py:406`) con su comando.

## Los tres módulos que se parten

Son los que mezclan capas según el diagnóstico. La tarea de capas los parte por funciones, sin cambiar lo que hacen:

- `services/closure.py`: compuertas y decisión a `core/closure.py`; git, staging, commit y rollback a
  `runtime/git_closeout.py`.
- `dispatch.py`: texto del prompt a `core/prompt.py`; scion, reap y efectos a `runtime/dispatch.py`.
- `services/review.py`: recibos y disposición a `core/review.py`; lanzar el revisor a `runtime/review_launcher.py`.

`workspace.py` no se parte entre capas: se divide dentro de `ops` (scaffold y migraciones).

## Rutas que otros repos importan

Otros repos importan módulos internos de deskops (grep del 25-11 sobre `~/proyectos`). La mudanza deja en esas rutas
un módulo que solo reexporta desde su lugar nuevo, con un comentario que nombra a su consumidor. La tarea de migración
de los repos consumidores pasa esos imports a `deskops.operations` y borra los reexports.

| Ruta vieja | Consumidores |
|---|---|
| `deskops.doc_access` | `UIs/graph_ui/frontends/desk/serve.py`, `frontends/mindmap/deskops_routes.py` |
| `deskops.lifecycle` | `UIs/graph_ui/frontends/mindmap/deskops_routes.py` |
| `deskops.cli.commands.view` (`ViewError`, `project`, `task_params`) | `UIs/graph_ui/frontends/desk/serve.py` |
| `deskops.cli.main` (`main`) | tests de `scion` |
| `deskops.operations` (`DeskopsOperations`) | `UIs/graph_ui` (sigue siendo pública, no es reexport) |
| `deskops.models` (`TaskDoc`, `BoardDoc`, `AtomDoc`) | `UIs/graph_ui`, `legos` (pública: `deskops.models` reexporta `core.models`) |
| `deskops.testing.foreign_suites` | 5 tests de `scion` (pública, no se mueve) |

## Qué no decide este mapa

- Si `cli/commands/*` sobrevive: eso lo decide E2 (CLI generado).
- Qué se borra porque sldb ya lo hace: eso es E3. Este mapa solo pone cada cosa en su capa para que E3 la encuentre.
