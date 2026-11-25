FILE:desk/drawer/plans/deskops-como-config/context-review-guide.md
# Guía para revisar un nodo de este plan

Va en todo input de revisión en frío. Deriva de brief.md, alcance.md y decisiones.md; no agrega requisitos.

## Qué evalúas

Si este nodo, tal como está escrito, se entiende como **encargo de planificación**: propósito, resultado, repo dueño, límites, dependencias y aceptación comprobable. No evalúas si el diseño es bueno ni ejecutas nada.

## Cómo leer

- `dag.yaml` es la fuente de ids, aristas y gates. El plan tiene ejecución autorizada; un nodo se ejecuta solo promovido y con su preflight dispuesto.
- ROOT y PF son agrupaciones; un nodo `aggregate` no se ejecuta: termina cuando terminan sus hijos.
- Una flecha `depends_on` significa prerrequisito → dependiente. Hermanos sin arista no se entregan nada entre sí.
- Un gate `pending` es intencional, no un defecto. Los gates `G_GO*` y `G_GD*` los producen planes de sldb (`grafo-operable`, `generalizar-desde-deskops`); lo que esos planes fijan es contrato suministrado, no ambigüedad de este nodo.
- DK1–DK3, DK5, DK6, DA1–DA6, D2, D3 y D4 están tomadas por el dueño; DP1–DP4 quedaron autorizadas con el plan y se leen como dadas.
- El invariante de `alcance.md` (formato del desk, gramática del CLI, borrar en el mismo paso) aplica a todo nodo aunque su aceptación no lo repita.

## Qué cuenta como ambigüedad

Solo lo que obligaría al ejecutor de ESTE nodo a inventar: resultado indefinido, aceptación no comprobable, repo o actor ausente, dependencia que falta o sobra, contradicción con otra fuente suministrada, o un límite que permita exceder el alcance (en particular: escribir en sldb, suplir con Python una regla que sldb debería evaluar, o dejar dos caminos vivos).

No cuentan: nombres exactos de archivos, funciones o tests que el TaskDoc fijará al promover; contratos que produce una dependencia nombrada; trabajo de nodos dependientes; lo excluido en brief.md §Fuera de alcance.

Cita la frase del input que origina cada ambigüedad.

FILE:desk/drawer/plans/deskops-como-config/brief.md
# Brief: deskops como configuración sobre sldb

Fecha: 2026-11-05. Repo dueño: deskops. Estado: plan autorizado por el dueño (2026-11-05, decisiones.md DA1-DA6 y DK6), `execution_authorized: true`; CC30 promovido el 2026-11-06. Ramas P3 y P5 del árbol aprobado por el dueño (`~/proyectos/SLDB_1/deskops-como-config-arbol.md`). Consume `grafo-operable` (sldb, P1) y `generalizar-desde-deskops` (sldb, P2); sucede a `gates-por-tipo`, que queda congelado tras GC03 (DK2).

## Encargo

Que deskops deje de tener motor propio: el ciclo de vida, los gates de activación y de cierre, las vistas de la UI, las escrituras y las plantillas del desk pasan a ser configuración (modelos, documentos `RelationDoc`/`RuleDoc`/`ViewDoc`, semillas declaradas) que sldb evalúa, sirve y escribe. En código queda lo que es del caso y no es general: hechos de git, runtime (Herdr/Scion), materializadores, bootstrap, identidad y un CLI delgado cuya gramática no cambia.

## Por qué ahora

- El dueño decidió el 2026-11-05 (DK1): lo general va a sldb y lo específico del caso deskops va a deskops; deskops es configuración sobre sldb.
- deskops son ~18.7k líneas (`deskops/deskops` en `827f3db7`: `cli/` 5.5k, nivel superior 4.6k, `services/` 3.6k, `graph/` 2.3k, `models/` 1.1k, `runtime/` 1.0k) que reimplementan lo que sldb tiene o está construyendo: grafo propio por regex (el Board tardaba ~100 s), reglas de closeout en Python (`closeout_gates.py`, `operations.py verify_task_closeout`), motor de transiciones (`lifecycle.py`), transacción propia (`doc_io.py`), vistas armadas a mano (`desk_view.py`), plantillas como strings (`workspace.py`).
- `gates-por-tipo` ya entregó en rama (`wt/gates-por-tipo`) tipos de tarea con jerarquía (GC01), `ReviewDoc` (GC02), cierre de las vías de escape (GC06) y `deskops review` (GC03). Su resto (efectos en aristas, reglas de activación, herencia, composición) se rehace aquí sobre la API general en lugar de sobre código de deskops.

## Resultado esperado del plan completo

1. `operations.py` es una fachada sin lógica propia; los `spec/**.yaml` duplicados desaparecen (CC30).
2. El ciclo de vida es grafo: efectos en `RelationDoc.attributes`, `advance` por `edges_holding` + `apply_effects`; `lifecycle.py` solo carga configuración y llama a sldb (CC31).
3. Cada tipo de tarea declara sus gates de activación como `RuleDoc` por familia; `advance` explica un bloqueo con `edges_blocked`; produce `G_CONSUMER` para sldb (CC32).
4. El cierre es una regla sobre recibos de evidencia; en código solo quedan los productores de hechos de git y archivos (CC33).
5. Las vistas de la UI son `ViewDoc` servidas por `sldb serve`; `desk_view.py` desaparece; graph_ui lee de sldb (CC34).
6. Toda escritura va por `sldb.api.transaction` con guarda; `doc_io.py`, los selectores propios y los escaneos de referencias desaparecen (CC35).
7. Las plantillas del desk son datos del paquete y las escribe el scaffold de sldb (CC36).
8. Ninguna vía de escritura pone el ciclo de vida en un estado que las reglas no permiten (CC37).
9. Cierre medido: líneas de código vs configuración, suite y `doctor` verdes en los 6 desks, Board < 1 s caliente, documentación de cómo se declara un tipo nuevo (CC51–CC53).

## Invariante (no negociable, ver `alcance.md`)

El formato del desk y la gramática del CLI de deskops no cambian. Cada superficie se cambia y su código viejo se borra en el mismo paso.

## El límite (lo que este plan no promete)

- **No escribe en sldb.** Lo que falte se pide con `deskops message send --to sldb` (D3) y se espera al nodo de sldb que lo entregue.
- **No suple con Python una regla que sldb debería evaluar.** Si el lenguaje de sldb no expresa algo, el nodo registra la hipótesis en su TaskDoc y manda la nota; no escribe un evaluador.
- **Los hechos externos siguen en deskops.** Commit en HEAD, test que existe, URL alcanzable: deskops los verifica y los deja como recibos; sldb no ejecuta git.
- **No cambia la autoridad de cierre.** `deskops closeout commit` sigue siendo la única puerta que cierra una tarea.
- **No toca P4.** `closure.py` (git), `runtime/` (Herdr/Scion), `materializers/`, `bootstrap.py`, `identity.py` siguen como código.

## Vocabulario

- **Configuración**: lo que deskops declara y sldb ejecuta: modelos (tipos de tarea, `ReviewDoc`), documentos de ciclo de vida (`RitualDoc`, `RelationDoc` con `attributes`), reglas (`RuleDoc`), vistas (`ViewDoc`), grafo de proyecto (`project_graph`), semillas y plantillas.
- **Superficie**: un comando o salida de deskops con contrato (CLI, `deskops view`, graph_ui).
- **Recibo de evidencia**: `ReviewDoc` de `kind: evidence` que deskops escribe al verificar un hecho de git o archivos para una tarea, anclado al contrato de la tarea.
- **Habilitador**: nodo de sldb que una superficie necesita antes de cambiarse (GO06, GO08, GO09, GD21–GD27); aquí es un gate.

## Fuera de alcance

Cambiar código de sldb; migrar desks ajenos más allá de `deskops desk update --apply` (cada desk lo corre al adoptar la versión); el runtime de Scion; autenticación; rediseñar el formato del desk o la gramática del CLI.

FILE:desk/drawer/plans/deskops-como-config/alcance.md
# Alcance y estado de partida

## Invariante de toda la migración

1. **El formato del desk no cambia.** Los archivos que hoy existen en `desk/` (Board, tareas, rituales, pills, átomos, drawer, inbox, `desk/lifecycle/`, `desk/reviews/`, `tag-namespaces.yaml`, `config.json`) conservan su ruta, su modelo y su forma. Excepción (DO1, decidida por el overlord el 2026-11-09, revisable): desde CC35a, el bloque de proveniencia `sldb:` que sldb escribe en el frontmatter es la forma nativa de sldb y no cuenta como cambio de forma. Un nodo puede agregar documentos nuevos en carpetas que ya existen (`RuleDoc` en `desk/lifecycle/`; las `ViewDoc` viven solo en el paquete, sin `desk/views/`, DA4), siempre escritos por `deskops desk update --apply` y nunca a mano; no reescribe los existentes salvo los que ya eran gestionados por deskops (`desk/lifecycle/`).
2. **La gramática del CLI no cambia.** Los goldens de ayuda (`tests/fixtures/golden/help/*.txt`, 120 archivos, `test_output_goldens.py:316 test_help_goldens`) y de salida (`tests/fixtures/golden/output/`, `test_command_output_goldens` :669) quedan iguales. Excepción ya decidida: lo que `gates-por-tipo` GC06 retiró (`advance --to`), que entra con GC06 antes de este plan.
3. **Cada superficie borra su código viejo en el mismo paso.** Un nodo que cambia una superficie a sldb borra en el mismo commit el código de deskops que la implementaba, con un grep en su aceptación. No hay periodo con dos caminos.
4. **En cada paso**, los tests de los archivos tocados verdes, `deskops doctor` y `deskops view board` correctos en los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui), y la suite completa del repo tocado sin fallas nuevas contra main (la corre el supervisor sobre el resultado integrado; ver regla 3).

## Estado de partida de deskops (verificado 2026-11-05, `main` en `827f3db7`)

- **Ramas sin integrar que cambian la base.** `wt/gates-por-tipo` (`deskops-wt-gates`, `e80fdef5`): GC01 `9c95ac90`, GC02 `b344d24f`, GC06 `6179e567`, GC03 `e80fdef5`; 81 archivos (+4576/-504): `models/task_types.py`, `services/review.py` (865 líneas), `operations.py` +169, `workspace.py` +279, `registry.py` +188. `wt/closeout-graph-sldb` (`deskops-wt-graph`): `graph/desk_graph.py` nuevo, `extract_docs|edges|sources.py` movidos a `tests/graph_oracle_v1/`, `read_snapshot` en `operations.py`/`desk_view.py`, Board ~1.63 s frío / ~0.355 s caliente. Este plan parte de las dos integradas (gates `G_GATES_FROZEN`, `G_P0`).
- **`operations.py` (1356) y `services/` se llaman en ambas direcciones.** Las funciones de operations delegan en servicios (`create_task_bundle` :344 → `tasks.py:80`; `advance_task` :347 → `tasks.py:172`; átomos :468-525 → `atoms.py`; drawer :358-362) y los servicios vuelven a operations por ~25 pass-throughs privados (`tasks.py:44-78`, `atoms.py:51-79`), construyendo un `DeskopsOperations` si no se les pasa uno (`tasks.py:35-37`, `atoms.py:42-44`, `closure.py:63-65`). Duplicados reales: `_normalize_task_payload` (`operations.py:537-567`) y `compile_task_spec` (`specs/compiler.py:25-61`), los dos llamados en `tasks.py:84-88`; `task_lifecycle.yaml` cargado dos veces (`lifecycle.py:78` y `workflow/next_actions.py:9`). La CLI solo llama a la fachada `operations.*`. graph_ui importa privados: `ops._read_doc`, `_resolve_glob`, `_registered_repositories`, `_repository_root` (`UIs/graph_ui/frontends/mindmap/deskops_routes.py:34,41,46,67`; `frontends/desk/serve.py:66-75`).
- **Specs YAML.** `spec/artifacts/*.yaml` (10), `spec/fields/*.yaml` (49), cargados por `specs/loader.py:17-31`; `registry.fields` solo lo usa `tests/test_specs.py`; `id_pattern` lo leen `compiler.py:33-40` y `operations.py:1118-1123`; `cli/model_introspection.py` (365) ya deriva los campos de los modelos pero repite `id_pattern`, `status_default` y `tags` en `_ARTIFACT_DEFAULTS` (:302-349). Dos fuentes de verdad.
- **Ciclo de vida.** `lifecycle.py` (382): `Transition.sets_status/terminal` (:40-49), `LifecycleSpec.effect` (:62-66), `transitions_from` toma topología y condición del grafo y el efecto del YAML (:123-151), `advance` (:154-190), `ensure_lifecycle_graph` no reescribe existentes (:328, :354). `task_lifecycle.yaml`: `task_activates` sin condición; `task_completes` exige `has(closeout_evidence_verified)`, hecho inyectado por `_add_closeout_facts` (`operations.py:441-450`) y borrado por `tasks.py:196-199`.
- **Closeout.** `verify_task_closeout` (`operations.py:602-723`); productores de hechos de git/archivos: `reference_points_to_commit` (`closeout_gates.py:197-229`), `_to_test` (:177-195), `_to_document` (:160-175), `_closeout_link_gate` (`operations.py:732-794`), `_skill_guard_test_evidence` (:895-926), `_generated_artifact_source_finding` (:939-984), `_reference_points_to_atom`/`_routed_follow_up` (:806-849). Reglas sobre campos: vocabulario, alerta de código implícito, `python_changes_without_declared_tests`, forma de URL, graduación de pills.
- **Vistas.** `services/desk_view.py` (534): `board` :249, `task` :286, `drawer` :331, `inbox` :377, `agents` :438; `_closeout` llama a `verify_task_closeout` por tarjeta (:184-213); contrato en `docs/deskops-ui.md`, `CONTRACT_VERSION = 1` (:26). graph_ui importa `DeskView` en proceso (`frontends/desk/serve.py:158-162`) y llama a `deskops.cli.main.main` para acciones (:217-238).
- **Escrituras.** `doc_io.DocTransaction` (:250) es el único escritor al store vía `sldb.api`; callers en `operations.py:266,1327`, `tasks.py:92`, `atoms.py:179,294,356`, `drawer.py:116,168`, `retire.py:103`, `closure.py:429`, `issues.py:337`, `replace.py:85`, `runtime/scion.py:394`. `message send/ack` escribe crudo sin transacción (`cli/commands/message.py:123,181`).
- **Plantillas.** Strings en `workspace.py` (`scaffold_desk` :166-233, `_write_if_missing` :251, Board :292, pills :322, rituales :340-398, drawer :412, namespaces :419); FAQ empaquetada `deskops/data/faq.md`; `desk update` adivina modelos por ruta (`cli/commands/desk.py:100 guess_model_for_path`).

## Habilitadores (gates) y qué consume cada nodo

| Gate | Lo produce | Lo consumen |
|---|---|---|
| `G_P0` | P0 del árbol: T0.1 (`wt/board-perf` / `read_snapshot`) y T0.3 (`wt/closeout-graph-sldb`) integrados en main | CC30 |
| `G_GATES_FROZEN` | `gates-por-tipo`: GC01, GC02, GC03 y GC06 cerrados en main; dag.yaml de gates-por-tipo marcado congelado | CC30, CC32 |
| `G_GO06` | sldb grafo-operable GO06 (`RuleDoc`, `rules check/explain`) | CC32, CC33 |
| `G_GO08` | sldb GO08 (evaluación en escritura/transición, `edges_blocked`; GO07 anclas incluido transitivamente) | CC32, CC33, CC37 |
| `G_GO09` | sldb GO09 (`attributes.sets/terminal`, `effects`, `apply_effects`) | CC31 |
| `G_GD21` … `G_GD27` | sldb generalizar-desde-deskops GD21 … GD27 | ver `dag.yaml` (`requires` de cada nodo) |

Un gate de sldb se satisface cuando el nodo cerró en `main` de sldb, mandó su nota de cierre a deskops y deskops pinnea en `pyproject.toml` una versión de sldb que lo contiene. Hasta entonces, los nodos que lo requieren no se promueven.

## Qué produce este plan para sldb

`G_CONSUMER` de `grafo-operable` (antes asignado a GC05 de gates-por-tipo, que queda congelado): lo produce CC32 como test de integración y lo informa con `deskops message send --to sldb`.

## Reglas comunes de ejecución

1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de deskops, con `--task-type` y `files` completos. Las revisiones en frío (preflight, cold-bundle con `deskops review`) las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`. Nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de deskops por nodo o grupo de nodos que el coordinador fije.
3. Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor una vez sobre el resultado integrado, sin fallas nuevas contra main. Un nodo no cierra con tests rojos ni saltados.
4. Antes de cambiar una superficie, el nodo captura sus goldens de salida (si no existen) sobre un desk de prueba; después del cambio deben ser idénticos, salvo lo que su aceptación nombre.
5. Toda capacidad entra con prueba, `CHANGELOG.md` y doc en `docs/`; los rituales del desk que nombran el comportamiento cambiado se actualizan con `deskops` en el mismo nodo.
6. Compatibilidad de desks: lo que un nodo agrega o reescribe en `desk/` lo escribe `deskops desk update --apply` de forma idempotente (segunda corrida sin cambios), probado.
7. Nada de Python supliendo una regla: si el lenguaje de sldb no la expresa, hipótesis en el TaskDoc y nota a sldb.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

FILE:desk/drawer/plans/deskops-como-config/decisiones.md
# Decisiones registradas

Cada entrada dice quién decidió, con qué fuente y en qué fecha. D2, D3 y D4 son del dueño y están en `sldb/desk/drawer/plans/grafo-operable/decisiones.md`; se copian con el mismo id porque este plan las consume. Las DP eran propuestas de este plan; el dueño autorizó el plan el 2026-11-05 y con él las DP. DA1–DA6 son las respuestas del dueño a los pendientes de ambos planes (`deskops-como-config` y `generalizar-desde-deskops` de sldb), con el mismo id en los dos `decisiones.md`.

| Id | Decisión | Actor | Fuente | Fecha |
|---|---|---|---|---|
| DK1 | Lo general va a sldb y lo específico del caso deskops va a deskops; deskops es configuración sobre sldb. | Dueño | Aprobación del árbol de tareas `~/proyectos/SLDB_1/deskops-como-config-arbol.md` (brief `planes-config-brief.md`) | 2026-11-05 |
| DK2 | `gates-por-tipo` queda congelado tras GC03: se integran y cierran GC01, GC02, GC03 y GC06 (ya implementados en `wt/gates-por-tipo`); su resto (GC04 efectos en aristas, GC05 reglas de activación y `G_CONSUMER`, GC07 herencia, GC08 rituales, GC09–GC11 composición) no se ejecuta en ese plan y se rehace aquí en CC31, CC32 y CC33 sobre la API general. | Dueño | Árbol aprobado, T0.2 ("Terminar GC03 y congelar gates-por-tipo → su resto se rehace en P3") | 2026-11-05 |
| DK3 | Invariante: el formato del desk y la gramática del CLI no cambian; en cada paso la suite y `deskops doctor` en los 6 desks quedan verdes; cada superficie se cambia y su código viejo se borra en el mismo paso. | Dueño | Árbol aprobado, §Contexto | 2026-11-05 |
| DK5 | Orden: P3 empieza con CC30 (sin habilitador) y cada nodo sigue a su habilitador: CC31←GO09, CC32/CC33←GO06+GO08, CC34←GD25, CC35←GD22+GD23+GD24, CC37←CC31+CC32. Todo se ejecuta en robocop2. | Dueño | Árbol aprobado, §Orden y paralelismo | 2026-11-05 |
| DK6 | Las invariantes viven en el modelo: una invariante de UN documento es un validador pydantic del modelo (field_validator / model_validator) y la cumple toda vía de escritura (deskops, sldb fields/docs update, /save, transacción); una invariante ENTRE documentos es una RuleDoc de sldb; el test deja de ser el lugar de la invariante y solo prueba que el modelo o la regla rechaza el caso malo. En este plan: nodo CC38 (depende de CC30) mueve los chequeos de un documento al modelo y borra el chequeo viejo en el mismo paso; CC37 lo consume para TaskDoc. | Dueño | Brief `planes-autorizados-brief.md` ("confío en tu criterio"): "los documentos los declaramos en pydantic; algunos tests/invariantes tendrían que mudarse allá" | 2026-11-05 |
| DA1 | Hechos de git en vistas (GD25 de sldb): no hay punto de extensión `computed` en Python. deskops deja esos hechos como recibos (ReviewDoc kind evidence, DP2) y la vista solo los lee. | Dueño | Brief `planes-autorizados-brief.md` ("confío en tu criterio"), punto 1 | 2026-11-05 |
| DA2 | `/save` atómico (GD24 de sldb): sí. Revierte todo ante falla; el cambio de contrato se anota en el CHANGELOG de sldb. | Dueño | Brief `planes-autorizados-brief.md` ("confío en tu criterio"), punto 2 | 2026-11-05 |
| DA3 | N de CC51: se fija después de CC30, con lo que quede medido. | Dueño | Brief `planes-autorizados-brief.md` ("confío en tu criterio"), punto 3 | 2026-11-05 |
| DA4 | ViewDoc (DK4): solo como semillas del paquete deskops; sin carpeta `desk/views/`. | Dueño | Brief `planes-autorizados-brief.md` ("confío en tu criterio"), punto 4 | 2026-11-05 |
| DA5 | Evidencia de closeout: solo por tipo; `--evidence` por tarea solo suma kinds. | Dueño | Brief `planes-autorizados-brief.md` ("confío en tu criterio"), punto 5 | 2026-11-05 |
| DA6 | Escrituras fuera de deskops (CC37): se resuelven con DK6. La consistencia status ↔ current_node ↔ history es un validador del modelo TaskDoc, que sldb ya aplica en toda escritura (roundtrip en `sldb/src/sldb/api/documents/payload_save_steps.py:62`); no se pide a sldb un campo "solo por transición". | Dueño | Brief `planes-autorizados-brief.md` ("confío en tu criterio"), punto 6 | 2026-11-05 |
| D2 | Los gates de activación son bloqueo duro, sin bandera de salto; la vía de escape es especializar tipos de tarea. | Dueño | sldb `grafo-operable/decisiones.md` D2 | 2026-11-04 |
| D3 | No hay coordinación central entre desks; cada desk pide feedback por `deskops message send`. | Dueño | sldb `grafo-operable/decisiones.md` D3 | 2026-11-04 |
| D4 | El revisor barato es pi deepseek(-flash). | Dueño | sldb `grafo-operable/decisiones.md` D4 | 2026-11-04 |
| DP1 | Los tipos de tarea siguen siendo modelos con herencia (GC01, DC1 de gates-por-tipo); sus gates pasan de atributos de clase Python (`__activation_receipts__`, `__closeout_evidence__`) a `RuleDoc` por familia. La herencia de familias (`model <= X`) da gratis "un subtipo suma gates, nunca quita". | Propuesta de este plan; autorizada con el plan (Dueño, 2026-11-05) | gates-por-tipo DC1; sldb GO06 | 2026-11-05 |
| DP2 | Un hecho de git o archivos verificado por deskops queda como recibo `ReviewDoc` `kind: evidence` (campo `fact`) anclado al contrato de la tarea; la regla de cierre exige esos recibos intactos. Se retira la inyección de hechos en el payload (`closeout_evidence_verified`, `pill_graduation_verified`). | Propuesta de este plan; autorizada con el plan (Dueño, 2026-11-05) | Árbol T3.3 ("en código solo los hechos que vienen de git"); gates-por-tipo §El límite | 2026-11-05 |
| DP3 | Las reglas, vistas y documentos de ciclo de vida de fábrica son semillas del paquete deskops (`deskops/data/`), declaradas y pasadas en proceso a `sldb.api.scaffold_store` (GD26, `declaration=`); `store.yaml` de cada desk no cambia de forma. | Propuesta de este plan; autorizada con el plan (Dueño, 2026-11-05) | sldb GD26; DK3 | 2026-11-05 |
| DP4 | graph_ui lee las vistas de `sldb serve` (`GET /views/<nombre>`) y sigue escribiendo por el CLI de deskops en proceso hasta que CC35 deje las escrituras sobre la transacción de sldb; no habla con `sldb serve /save` directamente para tareas (las transiciones son de deskops). | Propuesta de este plan; autorizada con el plan (Dueño, 2026-11-05) | Árbol T3.4; `frontends/desk/serve.py:217-238` | 2026-11-05 |

| DO1 | CC35a: todo documento que deskops crea o edita lleva el bloque de proveniencia `sldb:` (by/at/via/authority) en el frontmatter; se acepta como la forma nativa de sldb. El invariante 1 de alcance.md ("conservan su forma") se lee sin contar ese bloque. | Overlord (decidido 2026-11-09, revisable por el dueño) | Entrega de CC35a (wt/cc35a e6b95b21) | 2026-11-09 |
| DO2 | CC32 punto 1: `deskops review` no tiene comando para los recibos reproduction, goldens ni owner, así que task.debug, task.refactor y task.decision no se pueden activar. Se agrega una tarea de seguimiento que suma esos kinds a `deskops review` y se promueve apenas CC32 esté en main. | Overlord (decidido 2026-11-09, revisable por el dueño) | TaskDoc de CC32 a9 | 2026-11-09 |
| DO3 | CC32 punto 2: se acepta que, al aplicar las reglas, las tareas en ritual-execution sin recibos aceptados e intactos queden bloqueadas. Con CC35a, un update sin cambios fija el ancla y las destraba; las task.refactor esperan a DO2. | Overlord (decidido 2026-11-09, revisable por el dueño) | TaskDoc de CC32 a10; reports/coordinador-proyecto.md | 2026-11-09 |
| DO4 | main-en-verde: `deskops review record` acepta también preflight y bundle con evidencia del operador (engine human, operador y motivo "no model available" visibles), para que el quickstart y los e2e del CI activen task.code sin modelo. CONTRADICE la pill `pill-zero-context-preflight-precedes-executor` (la aprobación de un experto no sustituye a la revisión barata sin contexto). Solo para el CI (quickstart/e2e): no se usa para activar tareas reales en ningún desk hasta que JP lo confirme. | Coordinador de proyecto (decidido 2026-11-09, revisable por JP; condiciones del overlord) | Fallos 1-3 del run 42694709414; CC32 | 2026-11-09 |
| DO6 | CC33a, dos desvíos de la entrega (wt/cc33a, informe `runs/subagents/cc33a-worker-report.md` §Desvíos 1-2): (a) los recibos `ReviewDoc kind: evidence` se escriben solo desde `deskops closeout verify` (CLI, `write_receipts=True`); la vista del board y `closeout commit` llaman a verify sin escribir. CC33b decide si `closeout commit` escribe recibos antes de leerlos con las reglas. (b) Si el link gate pasa sin documento enlazante (desk exento, solo follow-up o guard-test de skill) no se escribe recibo atom ni materialization; si falla, se escribe un rejected por kind aparecido (o atom si ninguno). CC33b lo contempla al escribir la regla. | Coordinador (decidido 2026-11-10, revisable) | Entrega de CC33a; TaskDoc de CC33b | 2026-11-10 |
| DO7 | CC35d se corta: entrega solo a4 (desk replace por `sldb.replace_text`). Árbol de dominios, `require_domain_parents`, `tag_namespaces` y `tag_folder` (b6) esperan a sldb H1-H3 (drawer de sldb 6b34cd5f): `anchored_by` con valor sin namespace, namespaces acotados por modelos y segmentos vacíos. B3: cuando se retome, files suma doc_access.py, services/atoms.py y cli/commands/atoms.py. | Coordinador (decidido 2026-11-10, revisable) | Informe cc35d (wt/cc35d 568d2140) | 2026-11-10 |
| DO8 | CC33c, dos desvíos de b14/b17. (a) `sldb.api.project_graph(store)` no sirve porque deskops no declara `project_graph` en store.yaml y su `closed_document` es un callable; se usa `ProjectGraph(root, desk_graph_config())` de `sldb.api.edges.project_graph`, como desk_graph.py y closeout. (b) El grafo no crea nodos para dag.yaml ni model_contract_hashes.json, así que `declared_target_is_a_file` y su test quedan (b15); no hacen rglob, y el grep de rglob en deskops/graph/ queda vacío. Ambos esperan a sldb H1-H2 (drawer de sldb 61e9c7a9). | Coordinador (decidido 2026-11-10, revisable) | Informe cc33c (wt/cc33c 0571d23d) | 2026-11-10 |
| DO5 | CC30, CC36 y CC38 (task.refactor sin archivo de goldens honesto) se cierran con `closeout resolved-by` (código en main: 93cc1943, d4b49ff6, 4a1aae81). | Coordinador de proyecto (decidido 2026-11-09, revisable; aprobado por el overlord) | DO2; closeout resolved-by (cdce4ca2) | 2026-11-09 |

## Pendientes del dueño

Ninguno: los cuatro pendientes (N de CC51, DK4, evidencia por tarea, escrituras fuera de deskops) los resolvió el dueño el 2026-11-05 (DA3, DA4, DA5, DA6).

FILE:desk/drawer/plans/deskops-como-config/dag.yaml#node:ROOT
id: ROOT
title: deskops como configuración sobre sldb
owner_repo: deskops
children:
- PF1
- PF2
- PF3
- PF4
scope: 'deskops deja de tener motor propio: ciclo de vida, gates, vistas, escrituras
  y plantillas pasan a ser configuración que sldb evalúa, sirve y escribe; en código
  queda P4 (git, runtime, materializadores, bootstrap, identidad, CLI delgado). Cuatro
  paquetes: base (CC30, CC36), reglas (CC38, CC31, CC32, CC33, CC37), lecturas y escrituras
  (CC34, CC35), cierre (CC51, CC52, CC53). El orden lo imponen las aristas depends_on
  y los gates (DK5).'
acceptance: Todos los hijos cerrados; G_CONSUMER satisfecho e informado a sldb; el
  invariante de alcance.md se cumplió en cada hijo (cada uno lo prueba en su aceptación);
  CHANGELOG y docs al día significa que cada hijo cumplió su propia aceptación; ROOT
  no agrega criterio.

FILE:desk/drawer/plans/deskops-como-config/dag.yaml#edge:PF1
id: PF1
title: Base - fachada limpia y plantillas como datos
owner_repo: deskops
node_role: aggregate
children:
- CC30
- CC36
scope: 'Lo que no espera a ninguna capacidad nueva de reglas: operations.py como fachada
  sin lógica y sin specs YAML duplicados (CC30); plantillas del desk como datos escritos
  por el scaffold de sldb (CC36, espera a GD26).'
acceptance: grep de spec/artifacts y spec/fields en deskops/ vacío; workspace.py sin
  strings de plantilla; deskops init en un directorio temporal produce el mismo árbol
  y bytes que antes.

FILE:desk/drawer/plans/deskops-como-config/dag.yaml#edge:PF2
id: PF2
title: Reglas - ciclo de vida, activación, cierre y vías de escape
owner_repo: deskops
node_role: aggregate
children:
- CC38
- CC31
- CC32
- CC33
- CC37
scope: Invariantes de un documento como validadores del modelo (CC38), ciclo de vida
  como grafo con efectos (CC31), gates de activación por tipo como RuleDoc y G_CONSUMER
  (CC32), cierre como regla sobre recibos de evidencia (CC33), consistencia del ciclo
  de vida ante cualquier escritura como validador de TaskDoc (CC37).
acceptance: task_lifecycle.yaml sin sets_status ni terminal a nivel de transición;
  una tarea task.code sin recibos no se activa y advance muestra el finding; el cierre
  no inyecta hechos en el payload; grep de closeout_evidence_verified y TASK_TYPE_EVIDENCE
  en deskops/ vacío.

FILE:desk/drawer/plans/deskops-como-config/dag.yaml#edge:PF3
id: PF3
title: Lecturas y escrituras vía sldb
owner_repo: deskops
node_role: aggregate
children:
- CC34
- CC35
scope: Vistas de la UI como ViewDoc servidas por sldb (CC34); toda escritura por la
  transacción de sldb, con selectores y referencias entrantes de sldb (CC35).
acceptance: desk_view.py y doc_io.py no existen; deskops view board en JSON igual
  al golden previo; graph_ui lee /views de sldb serve.

FILE:desk/drawer/plans/deskops-como-config/dag.yaml#edge:PF4
id: PF4
title: Cierre (P5)
owner_repo: deskops
node_role: aggregate
children:
- CC51
- CC52
- CC53
scope: Medir lo que quedó como código y como configuración, verificar los 6 desks
  y el Board, documentar cómo se declara un tipo de tarea nuevo.
acceptance: docs/config-vs-code.md con el inventario; los 6 desks verdes; Board <
  1 s caliente sobre el desk real; docs/configuration.md publicada.

FILE:desk/drawer/plans/deskops-como-config/dag.yaml#gates
G_CONSUMER:
  title: deskops prueba el gate de activación con RuleDoc (gate externo de sldb grafo-operable)
  state: satisfied
  satisfied_by: 'CC32 cerrado en main de deskops: squash 6afc78b0, closeout 2ce88abd
    (2026-11-09); tests/test_activation_rules.py (G_CONSUMER en 3 pasos); nota en
    el inbox de sldb'
  produced_by: CC32
  resolver: cierre de CC32 y nota a sldb por deskops message send --to sldb con el
    hash del commit (antes asignado a GC05 de gates-por-tipo, congelado por DK2)
  evidence: en un desk temporal, una tarea sin recibo de revisión no se activa y la
    explicación nombra la cláusula; con recibo atado al hash de contrato vigente,
    se activa; con el contrato editado, el recibo queda changed y vuelve a bloquear

FILE:instruccion
Revisa el nodo ROOT siguiendo context-review-guide.md. Es un agregado: reformula el resultado sustantivo del paquete y da un DRY-RUN hipotético de sus hijos en orden, con entradas y salidas entre ellos y la validación conjunta. Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada.

