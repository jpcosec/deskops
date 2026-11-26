# Diagnóstico de deskops (y de sldb en relación a deskops), por capas

Fecha: 2026-11-25. Solo lectura, tres áreas en paralelo (workflow, relación con sldb, claridad) más una prueba de
`doctor` en un clon limpio. Lo marcado **verificado** se comprobó a mano; lo demás viene de los informes con su
evidencia `archivo:línea`. Corrige el análisis previo en el que se basaron `brief.md` y `alcance.md`.

## El problema de fondo (JP, 25-11)

La lógica interna, la de mantenimiento y operación y la de uso están mezcladas. Se ve en el CLI: 33 verbos de primer
nivel al mismo nivel, que mezclan las tres. Y dentro de los módulos: `services/closure.py` junta gates (modelo), git,
staging y rollback (operación) y salida (uso); `dispatch.py` junta ciclo de vida, scion y el texto del prompt;
`workspace.py` junta scaffold y cuatro migraciones. Por eso los tests no pueden probar el workflow sin arrastrar git,
scion y el formato de la ayuda.

Este diagnóstico ordena los hallazgos en tres capas:

1. **Núcleo**: el modelo del workflow (tareas, aristas, reglas, gates, vistas). Debe ser dato en sldb, sin saber de
   git, scion ni prompts, y probarse con escenarios contra las reglas. Verbos de hoy: `add`, `edit`, `bind`, `show`,
   `list`, `next`, `advance`, `closeout`, `promote`, `retire`, `drawer`, `issue`, `atoms`.
2. **Operación y mantenimiento**: que el desk esté sano y coherente con el código (doctor, migraciones, lint, CI, un
   agente que vigila mutaciones). Consume el núcleo para verificarlo. Verbos: `doctor`, `bootstrap`, `init`, `desk`,
   `repo`, `owner`, `tags`, `graph`, `drift`, `materialize`, `runtime`, `queue`, `status`.
3. **Uso**: superficies delgadas sobre el núcleo (CLI, MCP, UI, adaptadores de despacho claude/pi/scion que comparten
   un prompt generado como vista del núcleo). Verbos: `dispatch`, `review`, `integrate`, `message`, `view`, `faq`, `about`.

## Capa 1. Núcleo: el workflow declarado no se hace cumplir


Los ritos, `desk/lifecycle` y las RuleDocs describen un proceso coherente; el código lo deja pasar.

| Id | Hallazgo | Evidencia | Consecuencia |
|---|---|---|---|
| W3 | `closeout commit` fuerza `current_node = ritual-closeout` y no evalúa la arista `task_completes` | `services/closure.py:988-1001` (verificado) | Se cierra sin pasar por testing |
| N6 | Ningún prompt generado ordena tomar `task_hands_to_closeout` | `runtime/scion.py` ~706, `dispatch.py` | Las tareas se cierran desde `ritual-testing` |
| N3 | La evidencia `tests` solo exige que exista un `.py` bajo `tests/`; nadie lee el PASA/FALLA del tester | `services/closeout_gates.py:174-210` (verificado) | Se cierra con tests rojos |
| W4 / N10 | Las compuertas solo corren si la tarea está en el Board; `advance` y `next` no lo comprueban | `closure.py:765-770`, `services/tasks.py:300-311` | Una tarea fuera del Board se activa y cierra sin gates |
| N1 | Una tarea sin `task_type` solo tiene reglas de cierre de severidad `alert` | `desk/lifecycle/rule-closeout-alert-*.md` (verificado) | `verify` falla pero `commit` cierra |
| N2 | `commit` no exige el `ok` de verify; los recibos anclan el contrato de la tarea, no el código | `closure.py:963-985, 1243, 1346` | Un recibo viejo sigue valiendo con el código roto |
| N9 | `review record` acepta preflight y bundle `engine: human`; las reglas no miran el motor; quien dispone puede ser el mismo actor | `services/review.py:83, 740-837` | El gate de comprensión se cumple sin revisión en frío |
| N4 | El ejecutor corre `advance` después de implementar; `dispatch start` no comprueba nodo ni recibos | `dispatch.py:409, 440-470` | El gate llega tarde para frenar un brief ambiguo |
| N5 | `prompt.md` dice "commitea"; el `agents.md` del mismo agente dice "no commitees" | `dispatch.py:403-409`, `runtime/scion.py:954-955` (verificado) | Comportamiento según qué lea primero |
| W5 / N8 | supersede, resolved-by y retire escriben `status` directo; `resolved-by` no está en ningún rito | `closure.py:250, 286-420, 552-581` | Puertas laterales al cierre |
| N13 | El ritual de fase no tiene implementación | `services/tasks.py:219-251` | Depende de disciplina humana |
| W1 | Nombres: `task_activates` lleva a `ritual-testing`; `task_hands_to_closeout` escribe `ready_for_testing` | `desk/lifecycle/*.md`, `docs/operator-manual.md:155` | Confunde a quien lee |
| W2 | `next_actions` de `spec/workflows/task_lifecycle.yaml` contradice `closeout.md` y `execution.md`; `deskops next` lo imprime | `services/tasks.py:257, 289` | El CLI guía contra el rito |
| W6 | El validador lee el grafo del paquete; `_check_against_package` rechaza aristas del desk distintas | `models/task_lifecycle.py:8-13`, `lifecycle.py:482-507` | Contradice `workflow-policy-reference.md:173` |
| W7 | Cuatro compuertas solo en Python (su veredicto llega a la regla por recibos) | `closure.py:1464-1533, 1600, 1678, 1723` | No se ven en las reglas |
| N12 | `integrate` busca el cierre por asunto exacto; `--message` lo cambia; no distingue `Closeout-Mode` | `integrate.py:79-91` | Cierres no integrables; superseded integrables |
| N14 | La vista board muestra el `ok` de verify, no lo que aplica commit | `cli/commands/view.py:216-240` | La UI miente en ambos sentidos |


No verificado: N7 (una dependencia inexistente satisface `all(depends_on: status = "closed")`) y N11 (una referencia
a la propia tarea exime del gate de vínculos).

Además, en el núcleo:
- La evidencia de "tests" no corre tests (N3); los tests de la suite prueban implementación más que el workflow:
  muestra de 35 → 12 capacidad, 8 implementación, 15 mixtos; ningún test de escenario del tipo "una tarea en
  ejecución no puede cerrar".
- Configuración del núcleo escrita como Python en vez de dato: tablas `ARTIFACT_*` de `doc_access.py`,
  `deskops/spec/workflows/task_lifecycle.yaml` duplicando las aristas, `services/issues.py` sin modelo.

## Capa 2. Operación y mantenimiento

- **`doctor` marca mutaciones como errores** (verificado 25-11 en un clon limpio de main, sin tocar nada): rc=1 y 220
  líneas bajo "Errors (the desk is broken)": 195 "fields differ … what extracts it changed (an sldb upgrade)" y 25
  "fields changed under the model's contract (a real data change)", todas en RunDoc. Ninguna es una rotura. El
  docstring de `deskops/doctor_findings.py` dice que una mutación es una alerta, pero en las líneas 86-90 todo error
  que devuelve sldb pasa como error salvo `missing` y `doc_invalid`. No verificado si el que lo marca como error es
  sldb o deskops. Consecuencia: un doctor siempre rojo deja de ser señal.
- No hay vigilancia de mutaciones: `doctor`, `graph missing`, `drift` (que solo compara agentes de rol) y `queue`
  corren bajo demanda y dispersos. Nada reacciona a un cambio. Con git exigido (D4), la detección puede salir de
  `git status` y `git diff --name-only` (35-70 ms medidos).
- Lint: sin `[tool.ruff]`, 175 errores, 211 de 248 archivos sin formatear, sin pre-commit ni paso en el CI.
- CI rojo, causas: (A) `tests/test_output_goldens.py:123` no normaliza los alias largo+largo que Python 3.13 imprime
  distinto (`help/deskops_add_atom.txt`, `deskops_add_inbox-note.txt`); (B) en `.sldb/store.yaml` los includes de
  `AtomDoc` (l. 139-143) van antes que el de `CrossroadDoc` (l. 145) y al reconstruir desde cero la regla
  `tag_namespace:domain` evalúa átomos antes de que exista su ancla (verificado). El comentario del CI dice que
  `.sldb/core` no se versiona; se versiona.
- Mantenimiento que reimplementa sldb: `bootstrap.py` (vs `StoreDeclaration` + `build_store`; `apply_declaration` es interno, corregido el 26-11), `workspace.py` y `cli/commands/desk.py`
  (secuencia de `stores build`/`scaffold`/`check` por subprocess), `doctor_findings.py` (vs `diagnosis_findings`),
  los cuatro módulos de tags (vs `tag_namespaces` y `tag_tree`), `identity.py` (vs `catalog_store`), y deskops pasa
  `include_linked=False` en `lifecycle.py:318-343` (verificado), lo que obliga a copiar semillas a cada desk.
- Código muerto: `close_auto`, `graph/atom_trace.py`, `testing/foreign_suites.py`, funciones de `workspace.py` y
  `services/atoms.py`. Frontmatter parseado a mano en 7 módulos.

## Capa 3. Uso

- **Despacho**: `deskops dispatch` solo lanza por scion. Existen perfiles de runtime `claude` y `pi`
  (`desk/runtimes/`) pero solo los usa el revisor en frío. No hay forma de obtener el prompt de una tarea para
  despachar con claude o pi (pedido de MEPU: `dispatch start --only-prompt`). El ejecutor recibe dos prompts que se
  contradicen (N5) y corre `advance` después de implementar (N4).
- **MCP**: nada en deskops; sldb ya tiene `mcp --extension`.
- **UI**: existe fuera de deskops (`UIs/graph_ui/frontends/desk`, lee `deskops view` y `sldb serve`); sus botones de
  operación están deshabilitados porque deskops no expone las operaciones. La vista board muestra el `ok` de verify,
  no lo que aplica commit (N14).
- **Documentación para agentes**: la skill `.claude/skills/deskops-workflow` enseña comandos que no existen
  (`repo context`, `graph trace`, verificado), vocabulario retirado y el nombre opsys; `AGENTS.md` se contradice
  (spec2viz, kgdb, skills inexistentes o ignoradas); los docs no materializan átomos; `operator-manual.md` cita ids de
  átomos de ejemplo inexistentes; 19 módulos grandes sin docstring.
- **CLI**: 33 verbos de primer nivel sin separar capas; `cli/registry.py:_commands` mide 1 528 líneas y está diseñado
  alrededor de 153 goldens de `--help` byte a byte.

## Relación con sldb
Sobre ~13 700 de 27 236 líneas revisadas: reimplementa sldb ~2 600, dato escrito como código ~1 700, falta de verdad
en sldb ~1 200, propio ~5 500. El análisis previo (6 500 / 3 000 / 2 300) estaba inflado.

- Funciones que sldb hizo para deskops y deskops no usa: `template_anchors`, `describe_model_fields`,
  `catalog_store` (0 usos, verificado); también `referrers`/`rewrite_references` con grafo y el `on_write` de H4.
- deskops desactiva la lectura enlazada: `include_linked=False` en las cuatro consultas de aristas
  (`lifecycle.py:318-343`, verificado). Parte de la copia de semillas a cada desk la provoca deskops.
- Configuración como Python: `graph/desk_graph.py` (debería ser `project_graph:` en `store.yaml`), namespaces de
  tags duplicados (`atom_tags.py`), tablas `ARTIFACT_*` de `doc_access.py`, `services/issues.py` sin modelo.
- Frontmatter parseado a mano en 7 módulos; `workspace.py` escribe frontmatter fuera de sldb.
- Por módulo: `references.py`, `model_introspection.py`, `identity.py`, `bootstrap.py` (vs `StoreDeclaration` + `build_store`; `apply_declaration` es interno, corregido el 26-11),
  `message.py` (vs `sldb inbox`), `domain_tree.py` (vs `tag_tree`), `graph/view.py`, `doctor_findings.py`.

Pedidos C1-C9 enviados a sldb el 25-11, revisados: C7 y C8 ya existen (`catalog_store`; `stores build --check`);
C1 existe para aristas (falta para reglas), C5 existe en MCP, C6 y C9 en parte; faltan de verdad C2, C3 y C4.

## Lectura de conjunto

Lo más grave está en el núcleo: los gates no se hacen cumplir. Lo más visible para quien opera está en la capa 2:
doctor siempre rojo, CI rojo, sin lint, sin vigilancia. Lo que frena el uso está en la capa 3: un solo motor de
despacho, sin MCP, sin prompt reutilizable, y documentación para agentes que enseña cosas falsas. La reimplementación
de sldb es real pero menor de lo estimado y reparte sobre las capas 1 y 2. El plan de este directorio, ordenado por
fases F0-F5, debe reorganizarse por estas tres capas.
