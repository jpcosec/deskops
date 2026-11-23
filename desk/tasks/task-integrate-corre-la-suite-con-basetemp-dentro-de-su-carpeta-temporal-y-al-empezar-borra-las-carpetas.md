---
sldb:
  by: agent
  at: '2026-11-23T04:37:25Z'
  authority: generated
  via: create_document
id: task-integrate-corre-la-suite-con-basetemp-dentro-de-su-carpeta-temporal-y-al-empezar-borra-las-carpetas
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- deskops/integrate.py
depends_on: []
pills: []
files:
- deskops/integrate.py
- tests/test_integrate.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# integrate corre la suite con --basetemp dentro de su carpeta temporal y al empezar borra las carpetas deskops-integrate-* de corridas muertas

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de la sesión de Governance del 2026-11-23, registrado en ~/coordinacion/respuesta-deskops-2026-11-22-despacho-por-pr.md. En deskops/integrate.py, _steps (alrededor de la línea 303) crea `work` con tempfile.mkdtemp(prefix="deskops-integrate-") y el finally de integrate (alrededor de la línea 283) borra `temps`. Pero _run_suite (línea 195) corre cfg.suite sin basetemp: pytest usa su basetemp por defecto, /dev/shm/pytest-of-<usuario>, fuera de `work`, y conserva 3 corridas de unos 5 GB cada una. El 2026-11-23 eso dejó /dev/shm al 99 % (13 GB de pytest-of-robocop) y el intento 20261123T032514Z del integrate del modo pr falló con 6 ENOSPC en tests/test_view.py y tests/test_view_goldens.py. Además, un SIGKILL u OOM (dos el mismo día, 02:55 y 03:12 UTC) se salta el finally y la carpeta deskops-integrate-* queda para siempre.

## Goal

_Describe the concrete result this task must produce._

(1) _run_suite le da a la suite --basetemp=<work>/pytest: agrega `--basetemp=<work>/pytest` a PYTEST_ADDOPTS en el env del proceso (conservando lo que ya traiga PYTEST_ADDOPTS, separado por un espacio). Va por env y no por argv porque la suite configurada en desk/config.json es `sh -c "... pytest ..."` y agregar un argumento al final no llega a pytest. (2) Cada carpeta de trabajo deja un archivo owner.pid con el pid del proceso de integrate. Al empezar la suite, ya con el lock de la suite tomado (_suite_lock(cfg.tests_lock)), integrate borra las carpetas deskops-integrate-* de tempfile.gettempdir() que son de corridas muertas: las que tienen owner.pid con un pid que no vive (os.kill(pid, 0) da ProcessLookupError) y las que no tienen owner.pid y tienen mtime más viejo que cfg.suite_timeout. Nunca borra la carpeta propia ni la de un pid vivo. Cada carpeta borrada se imprime en una línea ("limpieza: <ruta>").

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/integrate.py (_run_suite, _steps, una función nueva de limpieza) y tests/test_integrate.py. No entra: cambiar la suite de desk/config.json, la limpieza de /dev/shm/pytest-of-scion de los testers (tarea aparte), la cola (deskops/queue.py).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests nuevos en tests/test_integrate.py (fallan antes del cambio): test_suite_gets_basetemp_inside_work: una suite falsa ["sh", "-c", "echo \"$PYTEST_ADDOPTS\" > <archivo>"] corrida por _run_suite recibe --basetemp=<work>/pytest y conserva un PYTEST_ADDOPTS previo (-p no:cacheprovider); test_stale_integrate_dirs_are_removed_under_the_lock: con TMPDIR apuntando a tmp_path, una carpeta deskops-integrate-a con owner.pid de un pid muerto y una deskops-integrate-b sin owner.pid y mtime viejo se borran; una deskops-integrate-c con owner.pid = os.getpid() y la carpeta propia quedan. p2: implementar en deskops/integrate.py. p3: correr los tests del archivo y la suite con -n 4. p4: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_integrate.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar; cada falla se compara contra un worktree limpio de origin/main)

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos de tests/test_integrate.py pasan, el resto de tests/test_integrate.py sigue verde, y una corrida real de integrate deja los temporales de pytest dentro de su carpeta deskops-integrate-* (y por lo tanto los borra el finally).
