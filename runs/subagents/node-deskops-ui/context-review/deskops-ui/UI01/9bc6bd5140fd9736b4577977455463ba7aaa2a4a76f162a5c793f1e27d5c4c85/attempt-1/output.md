## REFORMULACION

**Propósito:** dotar a deskops de una vista de datos de solo lectura que componga, desde operaciones existentes, lo que la UI necesita mostrar.

**Resultado:** `deskops/services/desk_view.py` con cinco vistas JSON —board, task, drawer, inbox, agents—; subcomando `deskops view {board,task <id>,drawer,inbox,agents}` con `--root` y `--format json|text`; tests, golden de help y `docs/deskops-ui.md` con los cinco contratos.

**Repo dueño:** deskops.

**Límites:** solo lectura, nada escribe; toda referencia no resoluble va a `errors` con causa, nunca como dato; sin servidor HTTP; no inventar valores ni copiar datos de Stitch.

## AMBIGUEDADES

1. “agents (runtime workers y las últimas N corridas de runs/subagents/index.jsonl)”. `N` no está definido; el ejecutor tendría que inventar el número de corridas a devolver y el criterio de “últimas”.
2. “primeras líneas del cuerpo” en drawer. No se fija cuántas líneas ni cómo se truncan; el ejecutor tendría que inventar el corte del contrato JSON.
3. “estado de ack” en inbox. El input no indica de dónde se obtiene: los campos listados de `InboxNoteDoc` no incluyen ese estado; el ejecutor tendría que inventar su fuente o forma de derivarlo.

## DRY-RUN

**Lecturas previstas:** BoardDoc y tareas; `list_tasks`/`show_task`; `next_action_report`; `verify_task_closeout`; PillDoc y AtomDoc; archivos de drawer; notas de inbox; `runtime workers`; `runs/subagents/index.jsonl`.

**Cambios previstos:** crear `deskops/services/desk_view.py`, `deskops/cli/commands/view.py`, `tests/test_desk_view.py`, `tests/fixtures/golden/help/` y `docs/deskops-ui.md`; registrar el subcomando en `deskops/cli/registry.py`.

**Dependencias:** ninguna (`depends_on: []`, `requires: []`).

**Validaciones futuras:** pytest con desks temporales reales; agrupación por `current_node` y conteo de gates contra `show_task`; `revision` igual a la guarda de graph_ui; referencias irresolubles en `errors`; drawer, inbox y agents contra disco; hash del árbol antes/después; `view --help` y golden; existencia y contenido de los cinco contratos; suite completa en robocop2.

## FUTURO

UI02 consume la vista por Python y expone `/api/view/*`. Un humano promueve el nodo con TaskDoc, hace el preflight de una ronda (DU6), decide el merge y registra el cierre; robocop2 ejecuta la suite completa.
