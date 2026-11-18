FILE:desk/tasks/task-los-contenedores-scion-de-deskops-traen-un-python-que-puede-correr-los-tests-del-workspace.md
---
sldb:
  by: agent
  at: '2026-11-18T21:31:00Z'
  authority: generated
  via: save_document_payload
id: task-los-contenedores-scion-de-deskops-traen-un-python-que-puede-correr-los-tests-del-workspace
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/runtime/scion.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
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

p1 (medir antes de elegir): en un contenedor de la imagen scion-claude que usa el despacho, lanzado con el mismo --config que usa dispatch (/mnt/ssd/proyectos/SLDB_1/.bootstrap/ir-scion-env.yaml), probar las dos vías y medir tiempo de arranque y si 'python -m pytest -q tests/test_dispatch.py' corre en /mnt/ssd/proyectos/SLDB_1/deskops: (a) un paso de arranque del template (hook pre-start del harness o comando de inicio) que crea un venv propio del contenedor fuera del workspace con 'uv venv --python 3.12' (uv descarga 3.12 si hace falta) y 'uv pip install -e <repo>[dev]' del repo de la tarea, y lo pone primero en el PATH; (b) una imagen derivada con /usr/bin/python3.12. p2: elegir con esa medición; preferir (a) si arranca en menos de 3 minutos, porque no agrega imágenes de varios GB. p3: implementar la vía elegida en deskops/runtime/scion.py con test. p4: documentar en el manual (sección de dispatch) y registrar la decisión y la medición en un atom (deskops add atom). p5: informe con los tiempos medidos de ambas vías.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py
- en un contenedor despachado con el template nuevo: python -m pytest -q tests/test_dispatch.py corre y pasa (salida en el informe)

## Done When

_Name the observable condition that makes the task complete._

Un ejecutor despachado por la cola puede correr los tests del workspace dentro del contenedor sin improvisar un entorno; la vía elegida y su medición quedan en un atom y en el manual.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-los-contenedores-scion-de-deskops-traen-un-python-que-puede-correr-los-tests-del-workspace: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

