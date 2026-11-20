---
sldb:
  by: agent
  at: '2026-11-20T19:22:46Z'
  authority: generated
  via: create_document
id: task-dispatch-start-sincroniza-el-template-de-scion-por-su-ruta-no-por-su-nombre-para-que-un-repo-con-su
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
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# dispatch start sincroniza el template de scion por su ruta, no por su nombre, para que un repo con su propio .scion no lo pierda

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-20, IR: dispatch-executor de la tarea specir extract falló con 'scion templates sync fallo (1): template deskops-executor not found locally'. dispatch escribe el template en dispatch.templates_dir (~/.scion/project-configs/sldb-1__b0899ed7/.scion/templates/<rol>) y después corre 'scion templates sync <nombre> --project sldb-1' con cwd en la raíz del desk. IR tiene su propio proyecto scion versionado (IR/.scion, settings.yaml enlazado al hub, con templates/ir-executor), así que scion busca el nombre en ese grove local y no lo encuentra. En sldb y deskops no pasa porque no tienen .scion propio.

## Goal

_Describe the concrete result this task must produce._

dispatch start llama a 'scion templates sync' con la ruta absoluta del directorio del template que acaba de escribir (la variable target de deskops/dispatch.py, cerca de la línea 297) en lugar del nombre del rol, que scion acepta según 'scion templates sync --help'. El sync funciona igual en un desk con .scion propio (IR) que sin él (sldb, deskops). Si scion start también resuelve el template por nombre en el grove local, se corrige igual o se corre con un cwd sin grove local, y se informa.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/dispatch.py (start), tests/test_dispatch.py (un test con un desk que tiene .scion/settings.yaml propio, con _scion simulado, que verifique que sync recibe la ruta), CHANGELOG. Fuera: borrar o cambiar IR/.scion.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: con un .scion local en el root, la llamada a sync usa la ruta absoluta del template. p2: cambiar el argv del sync. p3: revisar scion_start_argv: si pasa el template por nombre, verificar con 'scion start --help' si acepta ruta o si hace falta cwd; aplicar lo mismo. p4: CHANGELOG; commit con 'git commit -- <rutas>' y trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo y tests/test_dispatch.py pasan; el integrador relanza el dispatch de la tarea de IR y el sync no falla.
