# Diagnóstico de deskops (y de sldb en relación a deskops)

Fecha: 2026-11-25. Solo lectura, tres áreas en paralelo (workflow, relación con sldb, claridad). Lo marcado
**verificado** se comprobó a mano en el código; lo demás viene de los informes con su evidencia `archivo:línea`.
Este diagnóstico corrige el análisis previo en el que se basó `brief.md` y `alcance.md` de este plan.

## 1. El workflow declarado no se hace cumplir

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

No verificado: N7 (una dependencia inexistente satisface `all(depends_on: status = "closed")`) y N11 (una
referencia a la propia tarea exime del gate de vínculos).

## 2. deskops envuelve a sldb en vez de usarlo

Sobre ~13 700 de 27 236 líneas revisadas: reimplementa sldb ~2 600, dato escrito como código ~1 700, falta de verdad
en sldb ~1 200, propio ~5 500. El análisis previo (6 500 / 3 000 / 2 300) estaba inflado.

- Funciones que sldb hizo para deskops y deskops no usa: `template_anchors`, `describe_model_fields`,
  `catalog_store` (0 usos, verificado); también `referrers`/`rewrite_references` con grafo y el `on_write` de H4.
- deskops desactiva la lectura enlazada: `include_linked=False` en las cuatro consultas de aristas
  (`lifecycle.py:318-343`, verificado). Parte de la copia de semillas a cada desk la provoca deskops.
- Configuración como Python: `graph/desk_graph.py` (debería ser `project_graph:` en `store.yaml`), namespaces de
  tags duplicados (`atom_tags.py`), tablas `ARTIFACT_*` de `doc_access.py`, `services/issues.py` sin modelo.
- Frontmatter parseado a mano en 7 módulos; `workspace.py` escribe frontmatter fuera de sldb.
- Por módulo: `references.py`, `model_introspection.py`, `identity.py`, `bootstrap.py` (vs `apply_declaration`),
  `message.py` (vs `sldb inbox`), `domain_tree.py` (vs `tag_tree`), `graph/view.py`, `doctor_findings.py`.

Pedidos C1-C9 enviados a sldb el 25-11, revisados: C7 y C8 ya existen (`catalog_store`; `stores build --check`);
C1 existe para aristas (falta para reglas), C5 existe en MCP, C6 y C9 en parte; faltan de verdad C2, C3 y C4.

## 3. Claridad e higiene

1. La skill `.claude/skills/deskops-workflow` enseña comandos que no existen (`repo context`, `graph trace`,
   verificado), vocabulario retirado (routines, checklists, conditions, hooks), `deskops status` y el nombre opsys.
2. `AGENTS.md` se contradice: spec2viz dueño y retirado; kgdb inexistente; skills inexistentes o ignoradas (`.pi/`).
3. Los docs no materializan átomos; `operator-manual.md` (1 602 líneas) cita ids de átomos de ejemplo inexistentes.
4. 19 módulos grandes sin docstring; `workspace.py` (1 107) mezcla cinco responsabilidades.
5. Tests (muestra de 35): 12 capacidad, 8 implementación, 15 mixtos; 153 goldens de `--help` byte a byte;
   `cli/registry.py:_commands` mide 1 528 líneas y está diseñado alrededor de ese test.
6. Código muerto: `close_auto`, `graph/atom_trace.py`, `testing/foreign_suites.py`, funciones de `workspace.py`
   y `services/atoms.py`.
7. Lint: sin `[tool.ruff]`, 175 errores, 211 de 248 archivos sin formatear, sin pre-commit ni ruff en el CI.
8. El comentario del CI dice que `.sldb/core` no se versiona; se versiona (2 234 archivos).

CI rojo, causas: (A) `tests/test_output_goldens.py:123` no normaliza los alias largo+largo que Python 3.13 imprime
distinto (`help/deskops_add_atom.txt`, `deskops_add_inbox-note.txt`); (B) en `.sldb/store.yaml` los includes de
`AtomDoc` (l. 139-143) van antes que el de `CrossroadDoc` (l. 145), y al reconstruir desde cero la regla
`tag_namespace:domain` evalúa átomos antes de que exista su ancla (verificado).

## 4. Lectura de conjunto

Lo más grave no es el tamaño del código sino que los gates no se hacen cumplir y que la documentación para agentes
enseña cosas falsas. La reimplementación de sldb es real pero menor de lo estimado y fácil de atacar: sldb ya tiene
casi todo. El plan de este directorio debe revisarse contra este diagnóstico antes de seguir.
