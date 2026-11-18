---
sldb:
  by: agent
  at: '2026-11-18T05:55:35Z'
  authority: generated
  via: create_document
id: task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-un-runner-del-host-toma-de-una-cola-los-trabajos-pesados-que-encolan-los-post-hooks
pills: []
files:
- deskops/config.py
- deskops/cli/registry.py
- docs/operator-manual.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops integrate corre los gates de una tarea cerrada en copia limpia y pushea codigo y tip

## Rationale

_Explain why this task exists or the business driver behind it._

La integracion (copia limpia, suite completa, checks del desk, push del commit de codigo y luego del tip, actualizar la instalacion de herramientas) la hace hoy a mano el integrador siguiendo la receta escrita en el archivo integrate-recipe.md de la carpeta .bootstrap del workspace. JP quiere que corra sola como trabajo de la cola del host.

## Goal

_Describe the concrete result this task must produce._

Un comando nuevo, deskops integrate --task <id> --root . , que ejecuta en orden y se detiene en el primer fallo: (1) gates de memoria de la cola; (2) clon limpio del repo en un directorio temporal bajo TMPDIR, en el sha del closeout de la tarea, y comprobacion de que es avance directo (fast-forward) de la rama remota configurada; (3) si el rango toca algo fuera de desk/, .sldb/ y runs/, la suite declarada en la configuracion bajo el cerrojo de tests configurado; (4) checks del desk en la copia: todas las rutas de .sldb/store.yaml existen en el commit y deskops graph missing no sube respecto de la rama remota; (5) push del commit de codigo y despues del tip, sin force, con el comando de credenciales configurado; (6) actualizacion del checkout de herramientas configurado; (7) borrado de la copia y una linea en runs/hooks/events.log. Si falla, no pushea, borra la copia, deja el log y sale con codigo distinto de cero (la cola deja la nota). La configuracion vive en DeskConfig, campo integrate: remote_url, branch, suite (argv), tests_lock (ruta), tools_checkout (ruta opcional), push_env (argv que imprime el token, opcional). Con --dry-run hace todo menos los pasos 5 y 6 e imprime lo que pushearia.

## Scope

_State what is in scope and what is out of scope._

Dentro: un modulo nuevo integrate.py en el paquete deskops, el campo en deskops/config.py, el registro en deskops/cli/registry.py, tests con repos git reales creados en tmp_path (un remoto bare local hace de GitHub), manual. Fuera: declarar la configuracion en desks reales; el timer del host; cambios en sldb. Checkout principal, sin worktree ni rama, sin git add ni git commit.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_lifecycle_graph.py

## Done When

_Name the observable condition that makes the task complete._

En tmp_path, con un remoto bare local, integrate pushea codigo y tip de una tarea cerrada cuando los gates pasan, y no pushea cuando la suite falla, cuando falta una ruta de store.yaml o cuando no es fast-forward.
