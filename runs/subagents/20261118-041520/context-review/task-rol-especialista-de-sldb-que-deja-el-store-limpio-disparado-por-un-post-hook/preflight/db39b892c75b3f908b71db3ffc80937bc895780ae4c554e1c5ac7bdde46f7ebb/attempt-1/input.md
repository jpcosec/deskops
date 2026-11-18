FILE:desk/tasks/task-rol-especialista-de-sldb-que-deja-el-store-limpio-disparado-por-un-post-hook.md
---
sldb:
  by: agent
  at: '2026-11-18T04:15:09Z'
  authority: generated
  via: save_document_payload
id: task-rol-especialista-de-sldb-que-deja-el-store-limpio-disparado-por-un-post-hook
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
- deskops/cli/registry.py
- tests/test_scion_runtime.py
- docs/operator-manual.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-scion-coordinator-progresses-authorized-work
- atom-automatic-routines-vs-llm-tasks
---

# Rol especialista de sldb que deja el store limpio, disparado por un post-hook

## Rationale

_Explain why this task exists or the business driver behind it._

JP pidio un agente especialista de sldb que deje siempre limpio el store del desk despues de cada tarea (documentos sin registrar, anclas perdidas, mutaciones fuera del CLI). Hoy eso lo revisa a mano el coordinador o el integrador, y el ejecutor de la tarea de post-hooks edito un atom a mano sin que nada lo frenara.

## Goal

_Describe the concrete result this task must produce._

Tres entregables en el repo deskops.

1. Un RoleDoc de nombre `sldb-store-specialist` en la carpeta de roles del desk, creado con `deskops add role --name sldb-store-specialist --kind pi --tools read grep find ls bash` y la misma `--model` que declara `desk/roles/deskops-tester.md`. Su cuerpo dice el encargo del punto 2.

2. `deskops runtime template` acepta `--mode specialist` (ademas de executor, coordinator, tester). Un rol cuyo nombre o id termina en `-specialist` resuelve ese modo sin pasar `--mode`. El modo escribe un agents.md propio, generado por una funcion nueva `_render_specialist_agents_md` en `deskops/runtime/scion.py`, que ordena al agente, parado en la raiz del desk (variable `DESKOPS_DESK_ROOT`):
   a. Correr `sldb stores check --store .sldb --format json` y `deskops doctor --root .` y guardar ambas salidas en el run-dir asignado.
   b. Reparar SOLO con estos cuatro comandos, que son la definicion de "mecanico": `sldb docs track <ruta>` para un Markdown bajo `desk/` que el check informa sin registrar; `sldb docs update <ruta>` para un documento registrado cuyo archivo cambio fuera del CLI; `sldb docs untrack <id>` para un documento del indice cuyo archivo ya no existe; `sldb stores rebuild-index --store .sldb` cuando el check informa indice derivado desfasado.
   c. Todo hallazgo que no se arregla con esos cuatro comandos (incluidas las anclas perdidas y cualquier cambio de contenido) NO se toca: se deja una nota con `deskops message send "<hallazgo textual y documento afectado>" --kind unclear --title "store: <id del documento>" --root .`, una nota por hallazgo.
   d. Volver a correr el check, escribir `result-summary.md` en el run-dir con: hallazgos antes, comandos corridos, hallazgos despues, notas enviadas.
   e. Prohibido: editar archivos a mano, tocar codigo o tests, `git commit`, `git add`, `deskops closeout`, `deskops advance task`. Los cambios quedan sin commitear para el coordinador.
   f. Terminar con `sciontool status task_completed "<resumen de una linea>"`.
   `scion_child_identity` acepta ademas el rol `specialist` y nombra al agente `deskops-s-<12hex>`.

3. `docs/operator-manual.md`, dentro de la seccion "Post-hooks on a transition", gana un ejemplo de hook llamado `encola-especialista-de-store` para la transicion `testing-task_hands_to_closeout`: agrega una linea `<fecha UTC ISO> <DESKOPS_TASK_ID>` al archivo `runs/hooks/store-specialist.queue`. El manual dice que el hook solo encola y que el coordinador despacha al especialista con `deskops runtime template role-sldb-store-specialist --mode specialist` y `scion start`.

## Scope

_State what is in scope and what is out of scope._

Dentro: `deskops/runtime/scion.py`, la lista `choices` de `--mode` en `deskops/cli/registry.py`, `tests/test_scion_runtime.py`, `docs/operator-manual.md`, el RoleDoc nuevo. Fuera: cambios en el repo sldb; declarar el hook en algun desk; despachar al especialista; el runner que lee la cola. Se trabaja en el checkout principal de deskops, sin worktree ni rama. Si el cambio deja codigo o tests sin uso, se borran en la misma tarea. No se tocan archivos ya modificados por otros en el checkout (`deskops/cli/commands/message.py` y los tests de message, inbox y repo identity).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. `deskops add role` para el RoleDoc. 2. En `deskops/runtime/scion.py`: sumar `specialist` a la validacion de `mode` y a la resolucion por nombre en `scion_template_files`; nueva `_render_specialist_agents_md` al lado de `_render_tester_agents_md`; sumar `specialist` (letra `s`) en `scion_child_identity`. 3. `deskops/cli/registry.py`: sumar `specialist` a `choices` de `--mode`. 4. Tests nuevos en `tests/test_scion_runtime.py`. 5. Manual. 6. `deskops advance task` de esta tarea y aviso de termino.

## Validation

_List the checks required before this task can close._

- `TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py` pasa, con tests nuevos que, sobre un desk temporal de `tmp_path` creado como los tests vecinos del archivo, comprueban: (a) `--mode specialist` escribe scion-agent.yaml, system-prompt.md y agents.md; (b) ese agents.md contiene `sldb stores check`, `deskops doctor`, `sldb docs track`, `sldb docs update`, `sldb docs untrack`, `sldb stores rebuild-index` y `deskops message send`, y su seccion de prohibidos nombra `deskops closeout` y `deskops advance task`; (c) un rol llamado `x-specialist` resuelve el modo sin `--mode`; (d) un modo desconocido sigue levantando ValueError; (e) `scion_child_identity` con rol `specialist` devuelve un nombre que empieza con `deskops-s-`.
- `deskops runtime template sldb-store-specialist --root .` con `--out` apuntando a un directorio temporal bajo /dev/shm termina con codigo 0; el directorio se borra despues.
- `deskops graph missing --root .` termina con codigo 0.
- `sldb stores check --store .sldb` no informa el RoleDoc nuevo como no registrado.

## Done When

_Name the observable condition that makes the task complete._

Los tres entregables existen, las cuatro validaciones pasan y `git status --short` no muestra archivos nuevos fuera de los listados en Scope.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-rol-especialista-de-sldb-que-deja-el-store-limpio-disparado-por-un-post-hook: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

