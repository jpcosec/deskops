---
sldb:
  by: agent
  at: '2026-11-18T22:20:12Z'
  authority: generated
  via: save_document_payload
id: task-los-contenedores-scion-de-deskops-traen-un-python-que-puede-correr-los-tests-del-workspace
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- deskops/runtime/scion.py
- tests/test_scion_runtime.py
- 4a8c984f1d1623a9bba0efc5a4dfdec50311ad09
depends_on: []
pills: []
files:
- deskops/runtime/scion.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-contenedores-scion-venv-propio-con-uv-python-3-12-via-a
---

# Los contenedores scion de deskops traen un python que puede correr los tests del workspace

## Rationale

_Explain why this task exists or the business driver behind it._

El 2026-11-18 ejecutores y testers despachados por scion (imagenes scion-claude y scion-pi) no pudieron usar el entorno virtual del workspace: sus enlaces apuntan a un interprete python 3.12 que las imagenes no traen (solo tienen 3.13). Cada agente improviso un entorno con PYTHONPATH y a veces un test fallo solo por eso.

## Goal

_Describe the concrete result this task must produce._

Decidir e implementar una de dos vias y dejarla documentada en el manual del operador: (a) el template scion que genera deskops runtime template declara un paso de arranque que crea un entorno virtual propio del contenedor desde el pyproject del workspace y lo pone primero en el PATH; o (b) las imagenes traen python 3.12 en la misma ruta que usa el entorno del workspace. La tarea empieza por medir cual es viable con la version de scion instalada y registra la decision en un atom.

## Scope

_State what is in scope and what is out of scope._

Hecho de partida (integrador, 2026-11-18): el .venv del workspace (/mnt/ssd/proyectos/SLDB_1/.venv) es un venv sin pip sobre /usr/bin/python3.12 del host (pyvenv.cfg: home = /usr/bin, version = 3.12.3). Las imágenes scion (scion-claude y scion-pi, ~3.5 GB) traen python 3.13 vía uv y no tienen /usr/bin/python3.12, así que el .venv no arranca (pydantic_core ImportError) y el ejecutor deskops-e-c6c01f72e2a3 quedó bloqueado sin poder correr tests. Dentro: deskops/runtime/scion.py (el template que genera 'deskops runtime template'), sus tests, el manual del operador y, solo si se elige (b), el archivo de build de imagen. Fuera: cambios en el código de scion. El ejecutor trabaja en el checkout principal y commitea su código con rutas nombradas y Task-Id, como dice su RoleDoc.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1 (medir la vía a en el propio contenedor): el ejecutor ya corre en un contenedor scion-claude lanzado por deskops dispatch con --config /mnt/ssd/proyectos/SLDB_1/.bootstrap/ir-scion-env.yaml, y ahí mide. Con TMPDIR=/tmp y cronometrando: uv venv /tmp/ws-venv --python 3.12 (uv descarga 3.12 si no está); VIRTUAL_ENV=/tmp/ws-venv uv pip install -e /mnt/ssd/proyectos/SLDB_1/deskops[dev] -e /mnt/ssd/herramientas/sldb (el repo de la tarea con su extra dev, más sldb, que deskops importa); y después /tmp/ws-venv/bin/python -m pytest -q -p no:cacheprovider tests/test_dispatch.py en /mnt/ssd/proyectos/SLDB_1/deskops. Anotar los tiempos y el resultado. p2 (mecanismo de la vía a): implementarlo en deskops/runtime/scion.py como un paso que corre al inicio del agente. Si el template de scion que genera 'deskops runtime template' admite un comando o hook de inicio (ver cómo scion.py arma scion-agent.yaml y los hooks pre-start del harness), usar eso. Si no, dispatch start antepone a prompt.md un bloque 'Antes de empezar' con esos comandos y el export de PATH. El repo a instalar es la raíz de la tarea (--root) con su extra dev, más /mnt/ssd/herramientas/sldb cuando la tarea no es de sldb. p3 (vía b, solo si a falla o tarda más de 3 min): un Dockerfile en deskops/runtime/images/scion-claude-py312/Dockerfile, FROM ghcr.io/jpruizantonia/scion-claude:latest, que instala python3.12 en /usr/bin/python3.12. El contenedor no lo construye: el informe deja el comando docker build para el integrador. p4: test en tests/test_scion_runtime.py del paso de arranque (que el template o el prompt.md generado lo contenga). p5: documentar en docs/operator-manual.md, sección 'Launching the executor and tester through scion'. p6: atom con deskops add atom (--five-wh-one-plus how, tags system:deskops topic:scion) con la vía elegida y los tiempos medidos. p7: informe en result-summary.md del run dir.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py
- en un contenedor despachado con el template nuevo: python -m pytest -q tests/test_dispatch.py corre y pasa (salida en el informe)

## Done When

_Name the observable condition that makes the task complete._

Un ejecutor despachado por la cola puede correr los tests del workspace dentro del contenedor sin improvisar un entorno; la vía elegida y su medición quedan en un atom y en el manual.
