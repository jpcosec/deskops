PASA

# Veredicto del tester

El commit del ejecutor cumple el Done When: `docs/configuration.md` existe con el mapa de
configuración y las dos recetas, `tests/test_docs_recipes.py` ejecuta la receta del tipo nuevo en
un desk temporal (la tarea queda bloqueada y luego se activa) y comprueba que la vista responde,
y los enlaces/FAQ están presentes.

## Commit evaluado

- Commit: `b39f2fa86df977487034b3e0ebcbd584602391f7`
- Mensaje: `docs: configuration map with tested recipes for a new task type and a new view`
- Trailer: `Task-Id: task-cc53-docs-configuration-md-explica-que-es-configuracion-y-como-se-declara-un-tipo-de-tarea-nuevo-con`
- Archivos:
  - `docs/configuration.md` (nuevo)
  - `docs/workflow-policy-reference.md`
  - `docs/faq.md`
  - `deskops/data/faq.md`
  - `tests/test_docs_recipes.py` (nuevo)
  - `CHANGELOG.md`

## Pruebas ejecutadas

En un worktree limpio del commit (`git worktree add /dev/shm/wt-cc53 b39f2fa8`), con Python 3.11.2
y pytest 9.2.0:

- `TMPDIR=/tmp python -m pytest -q tests/test_docs_recipes.py`
  - Resultado: **2 passed**, exit 0.
- El commit no toca módulos de código, así que no hay `tests/test_<modulo>.py` adicionales del commit.

Además, en el árbol principal, para comprobar que no hay regresiones en la superficie documental
que la tarea exige:

- `TMPDIR=/tmp python -m pytest -q tests/test_output_goldens.py` — **7 passed**, exit 0.
- `TMPDIR=/tmp python -m pytest -q tests/test_cli_help_examples.py` — **13 passed**, exit 0.
- `TMPDIR=/tmp python -m pytest -q tests/test_operator_manual.py` — **1 passed**, exit 0.

No se ejecuta la suite completa: la integra el host, según el encargo del tester.

Nota de entorno: el `../.venv` del proyecto está roto en este host (symlink a Python 3.11 con
site-packages de 3.12 y sin pytest). Las pruebas se corrieron con `/dev/shm/t311/bin/python`
(Python 3.11 + pytest 9.2.0), apuntando a las fuentes de `sldb` y al checkout mediante `.pth`.
Esto es una limitación del entorno de prueba, no del commit.

## Comprobaciones de aceptación

- `docs/configuration.md` mapea modelos/tipos de tarea, ReviewDoc y recibos, RelationDoc con
  `attributes`, RuleDoc de activación/cierre/consistencia, ViewDoc, grafo, semillas y plantillas,
  con ubicación en paquete/desk y qué ejecuta sldb.
- Receta de tipo nuevo: subclase `TaskDoc` en `desk/models/*.py`, `desk update --apply`, RuleDoc
  propia, `sldb rules explain` y `deskops advance`. El test verifica el bloqueo
  (`is blocked by its rules` + `rule-activation-task-runbook`) y la activación posterior
  (`Advanced to ritual-testing via task_activates`).
- `docs/operator-manual.md` enlaza a `configuration.md` (línea 24) y
  `docs/workflow-policy-reference.md` añade el enlace.
- `docs/faq.md` y `deskops/data/faq.md` incluyen "Where is the rule for X?" y
  "How do I add a task type?".
- El grep de rituales
  (`spec/artifacts|desk_graph.py|doc_io|advance task .* --to`) sobre `desk/rituals` no devuelve
  coincidencias (rc 1), por lo que no había ritual que corregir y el commit correctamente no los toca.

## Observación no bloqueante

La receta de vista usa `sldb models add` + `sldb docs track` + `sldb views run`, en lugar del
literal `deskops desk update --apply` + `deskops view <nombre>` que menciona el enunciado. Es
coherente con el estado actual del CLI: `deskops desk update --apply` no tiene `include` para
ViewDoc y `deskops view` solo expone subcomandos fijos (`board`, `task`, `drawer`, `inbox`,
`agents`). Cambiar eso sería código de deskops, fuera de alcance, y el test ejecuta la receta real
y comprueba que la vista responde. Conviene que el closeout lo registre como precisión de la
receta, no como falla.
