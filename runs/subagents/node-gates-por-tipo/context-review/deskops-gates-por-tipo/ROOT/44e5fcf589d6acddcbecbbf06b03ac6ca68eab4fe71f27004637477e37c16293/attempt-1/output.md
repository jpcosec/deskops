REFORMULACION

ROOT es un agregado no ejecutable del plan «Gates por tipo de tarea en deskops». Propósito: que deskops exprese sus gates de ciclo de vida como documentos que evalúa sldb —tipos de tarea con jerarquía y evidencia declarada, `ReviewDoc` como recibo atado al contrato, `RuleDoc` de activación, efectos en las aristas—, cierre las dos vías que saltan gates (`advance --to`, `edit task`) y sustituya los scripts de revisión en frío por `deskops review`; además, incorpora composición y lectura del grafo. Repo dueño: deskops. Límites: no reimplementa el evaluador ni escribe Python que supla una regla; no toca sldb salvo `deskops message send`; no autentica actores; los hechos externos (git, tests, URL) siguen siendo de deskops; `closeout commit` sigue siendo la única puerta de cierre; no implementa el runtime de Scion ni migra desks ajenos. Aceptación: hijos cerrados, G_TYPES, G_RECEIPTS y G_CONSUMER satisfechos, G_CONSUMER informado a sldb, y CHANGELOG/docs cumplidos por cada hijo sin criterio adicional de ROOT.

AMBIGUEDADES

Ninguna. ROOT no ejecuta; su aceptación remite a los hijos y a gates con evidencia comprobable.

DRY-RUN

Hipotético, sin ejecutar: ROOT termina cuando cierran PC01, PC02 y PC03; el orden lo fijan sus aristas. PC01 aporta lo independiente de sldb: GC01 registra tipos y jerarquía, GC02 define `ReviewDoc`, GC03 entrega `deskops review` y retira los scripts; entrega a PC02 tipos registrados, modelo de recibo y comando. PC02 espera GO05–GO09: GC04 lleva efectos y `advance` a `edges_holding`; GC05 escribe RuleDocs de activación y produce G_CONSUMER; GC06, que solo requiere GC01, cierra `advance --to` y `edit task`; GC07 lee herencia del grafo; GC08 actualiza rituales y manual. PC03 recibe tipos y grafo: GC09 añade composición y `task.aggregate`, GC10 promueve nodos desde `dag.yaml`, GC11 hace que `deskops graph` lea aristas de sldb. Validación conjunta futura: `pytest tests`; `add task --task-type` rechaza tipos no registrados; `model <= TaskCodeDoc` incluye `task.refactor` y excluye `task.debug`; no quedan `context_review.py`; `task_lifecycle.yaml` no tiene `sets_status` ni `terminal`; una tarea sin recibo no activa y el finding nombra la cláusula; con recibo aceptado activa y el efecto escribe `status`; en desk temporal se comprueba G_CONSUMER; nota a sldb con hash de commit.

FUTURO

GO05–GO09 de sldb y sus gates `G_SLDB_*`; la disposición humana de cada revisión en frío; la confirmación del dueño sobre `--evidence`, DC7, `task.external` y contrato de Scion; la recepción de G_CONSUMER en sldb; la adopción por otros desks vía `desk update --apply`.
