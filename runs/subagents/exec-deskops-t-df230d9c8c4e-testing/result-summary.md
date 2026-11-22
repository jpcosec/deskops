PASA

# Resultado del tester

Tarea: task-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas-reales
Tester: deskops-t-df230d9c8c4e

## Commit del ejecutor

`97007d8085fe4414128642e5584a2fece72448d7` — "graph missing: planned_target para archivos que una tarea abierta va a crear".
Trailer verificado: `Task-Id: task-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas-reales`.

Archivos del commit:
- `deskops/graph/checks.py`: `_classify_planned_target` convierte en `planned_target` (informational, `record=True`) los `missing_declared_target` cuyo origen es `task:*`, cuyo destino tiene prefijo `source_file:`, `test_file:` o `doc:` y cuyo TaskDoc de origen no tiene un `status` de cierre (`closed`, `superseded`, `cancelled`, `retired`). El `reason` se conserva.
- `deskops/cli/commands/graph.py`: el resumen pasa a `N missing, M informational (P planned_target)`.
- `tests/test_graph_checks.py`: 4 tests nuevos (tarea draft abierta, status ausente, tarea cerrada, documento no-tarea).
- `tests/test_graph_declared_edges.py`: expectativas del resumen actualizadas.

Los archivos de código y tests son idénticos entre el commit del ejecutor y HEAD; las dos commits posteriores solo tocan `.sldb`/`desk`/`runs`.

## Pruebas ejecutadas (de a uno)

Entorno: el `.venv` del checkout apunta a un Python 3.12 ausente y `python` no está en PATH. Usé un venv temporal en `/tmp/deskops-test-venv` (Python 3.12.16 instalado con `uv`, `pip install -e '.[dev]'`), sin modificar el repo.

```text
TMPDIR=/tmp /tmp/deskops-test-venv/bin/python -m pytest -q tests/test_graph_checks.py
  -> 9 passed, exit 0

TMPDIR=/tmp /tmp/deskops-test-venv/bin/python -m pytest -q tests/test_graph_declared_edges.py
  -> 12 passed, exit 0

TMPDIR=/tmp /tmp/deskops-test-venv/bin/python -m pytest -q tests/test_graph_cli.py
  -> 18 passed, exit 0
```

Casos objetivos nuevos (seleccionados con `-v`): 4 passed.

No se corrió la suite completa (la corre integrate en el host).

## Verificación del comportamiento en el desk de deskops

`deskops graph missing --root .`:

```text
12 missing, 14 informational (14 planned_target)
exit=1
```

- Los faltantes de tareas abiertas con destino `source_file`/`test_file`/`doc` desaparecen de la lista de missing y aparecen como `planned_target` informational, con el mismo `reason`; incluye, entre otros, `deskops/specs/loader.py` y `docs/spec/spec-procesos-modelables.md` citados en el Rationale.
- Los mismos tipos de destino desde documentos que no son tareas abiertas siguen como `missing_declared_target` (cubierto por `test_non_task_citing_same_missing_file_stays_missing`).

## Observación no bloqueante

El desk sigue saliendo con exit 1 porque quedan 12 `missing_declared_target` de tareas abiertas cuyo destino es un `.yaml`/`.md` bajo `desk/drawer/plans/...` que el extractor no marca como `source_file`/`test_file`/`doc` (sale la ruta sin prefijo de kind). El Goal acota `planned_target` a esos tres kinds, así que quedan fuera del alcance de este cambio; no afectan la separación pedida ni el Done When.

## Veredicto

PASA. Los tres archivos de test relevantes pasan y `graph missing` separa `planned_target` de los missing reales.
