# Atribución: deskops

- Frame: `TaskService._lifecycle_gates` en `deskops/services/tasks.py:181`
  (`"holds": lifecycle.condition_holds(t.condition, payload)`), llamado desde
  `TaskService.show_task` (`deskops/services/tasks.py:155-164`) y entregado tal cual por
  `ViewService._gates` (`deskops/cli/commands/view.py:202-213`).
- `holds` evalúa solo la condición de la arista (`where_matches`; la de task_activates ->
  ritual-testing está vacía, así que da True). Los findings `on_transition` se calculan aparte
  (`_transition_findings`, línea 187) y se pegan al gate sin afectar `holds`.
- sldb no tiene la falla: con el mismo payload y `document=TaskCodeDoc:task-repro-holds`,
  `sldb.api.edges_holding` no devuelve la arista y `edges_blocked` sí la devuelve (ver repro.log,
  últimas líneas). El frame más interno de código propio está en deskops → se arregla en deskops,
  sin nota a sldb ni xfail.
- Nota de alcance para la fase 2: el arreglo natural cae en `deskops/services/tasks.py`
  (o en `view.py::_gates`, que está en files). `show task` imprime "open" con el mismo cálculo.
