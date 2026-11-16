FILE:desk/tasks/task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc.md
---
sldb:
  by: agent
  at: '2026-11-16T05:02:10Z'
  authority: generated
  via: save_document_payload
id: task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-materialization-contracts-declare-source-intent-and-target.md
files:
- deskops/services/closure.py
- tests/test_materialization_targets_outside_package.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
- atom-materializations-declare-source-atoms
from_drawer: desk/drawer/tasks/task-closeout-una-materialization-con-target-identity-de-paquete-no-cubre-los-archivos-del-paquete.md
---

# closeout: una materialization cuyo target_identity es un directorio cubre los archivos bajo ese directorio

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (cierre de SV01-SV04 en sldb, 2026-11-06): la compuerta atom|materialization exige un enlace por archivo; una materialization con target_identity src/sldb/notations (directorio) no cubrio ninguno de sus archivos y hubo que crear 62 materializations para 66 archivos. Hoy deskops/services/closure.py:1325-1340 busca la ruta exacta, y en sldb src/sldb/api/edges/project_graph/declared_target_nodes.py:52 exige is_file().

## Goal

_Describe the concrete result this task must produce._

En deskops, un archivo cambiado queda cubierto si alguna materialization de la tarea tiene un target_identity que es el mismo archivo o un directorio que lo contiene (comparacion por prefijo de ruta normalizada, con separador). Si `deskops graph missing` reporta missing_declared_target para un target que es directorio, se manda una nota a sldb pidiendo que declared_target_nodes acepte directorios, y esta tarea no espera esa respuesta.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/closure.py (alrededor de 1325-1340) y tests. No entra: modificar sldb (solo la nota), cambiar la compuerta de atomos. Precisiones del preflight 1: la funcion se llama target_covers(target, path) y vive junto a la cobertura de materializations en closure.py (se ubica por nombre, los numeros de linea son orientativos). Normalizacion: rutas POSIX relativas a la raiz del repo, sin resolver symlinks, sin barra final, sensibles a mayusculas; un target cubre un archivo si es igual o si path empieza con target + '/'. No hace falta que el directorio exista. La nota a sldb: titulo 'declared_target_nodes: aceptar un directorio como target declarado', cuerpo con la salida de graph missing y el caso; exito = nota entregada.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Funcion covers(target, path) por prefijo. 2) Usarla en la cobertura. 3) Test en tests/test_materialization_targets_outside_package.py: materialization con target 'pkg/sub' cubre 'pkg/sub/a.py' y no 'pkg/subzero.py'. 4) Correr graph missing en un desk sandbox con target directorio y, si falla, `deskops message send --to sldb`.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_materialization_targets_outside_package.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_gates.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El test del paso 3 pasa; si el paso 4 fallo, la nota a sldb esta enviada y citada en el commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

