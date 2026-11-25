REFORMULACION
Propósito: que `deskops view task` entregue los recibos (ReviewDoc) de la tarea para que graph_ui pueda dibujarlos. Resultado: `task.receipts` en la salida de la vista, con `id`, `kind`, `verdict`, `anchor_state` y `created_at`, ordenado por `created_at`; contrato documentado y pruebas. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: tocar `deskops/cli/commands/view.py`, `docs/deskops-ui.md` y tests; no `view board`, ni la UI de graph_ui, ni ReviewDoc. `anchor_state` se reutiliza de `deskops review status`.

AMBIGUEDADES
1. “json, yaml y text” frente a “`--format json` trae task.receipts” y “`--format json` es el contrato estable”: ¿yaml es obligatorio? Obligaría a inventar soporte y contrato yaml.
2. “un objeto por ReviewDoc cuyo subject es la tarea”: no define si `subject` es id, ruta, prefijo o referencia; obligaría a inventar el criterio de pertenencia.
3. “anchor_state se lee como lo calcula hoy deskops review status para la tarea”: no dice si es por ReviewDoc o un estado global; obligaría a inventar el mapeo.
4. “ordenada por created_at”: falta desempate y formato; obligaría a inventar orden estable y parseo.
5. “campo receipts” / “task.receipts”: no fija si va en `CARD` o solo en `task`; obligaría a inventar la ubicación contractual.
6. La validación cita `tests/test_view_goldens.py`, pero `files` solo lista `tests/test_view.py`: ¿se pueden actualizar goldens? Obligaría a inventar alcance.
7. “un recibo registrado por deskops review record”: faltan comando, flags y datos mínimos; obligaría a inventar el fixture sandbox.

DRY-RUN
Lecturas: TaskDoc, `view.py`, docs, tests, implementación de `review status`, modelo ReviewDoc, render y fixtures. Cambios: helper que liste ReviewDocs de la tarea y calcule `anchor_state`; añadir `receipts` al payload de `task`; render text con una línea por recibo; documentar; tests con desk sandbox. Dependencias: semántica de ReviewDoc, `review status`, soporte yaml y goldens. Validaciones futuras: los dos pytest citados; commit descriptivo y aviso a graph_ui. Sin ejecutar.

FUTURO
graph_ui consume `task.receipts` y dibuja los recibos. Un humano decide el alcance de yaml, el criterio de `subject`, la ubicación del campo y la actualización de goldens. Otro nodo puede cambiar ReviewDoc o `review status`; este nodo solo reutiliza su cálculo.
