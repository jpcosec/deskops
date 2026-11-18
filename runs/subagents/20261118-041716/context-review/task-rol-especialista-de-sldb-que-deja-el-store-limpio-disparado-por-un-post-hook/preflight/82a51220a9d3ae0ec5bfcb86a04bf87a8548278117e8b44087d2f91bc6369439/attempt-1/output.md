## REFORMULACION
Propósito: dotar a deskops de un rol especialista que, tras cada tarea, deje limpio el store del desk. Resultado: (1) RoleDoc `sldb-store-specialist`; (2) modo `specialist` en `deskops runtime template`, con renderer propio, resolución por sufijo `-specialist` e identidad `deskops-s-<12hex>`; (3) ejemplo de hook `encola-especialista-de-store` en el manual. Repo: checkout principal de deskops. Límites: fuera cambios en sldb, declarar el hook, despachar al especialista y el runner de la cola; sin worktree ni rama; no tocar los cinco archivos listados; borrar código/tests sin uso. Nodo ejecutable, no agregado.

## AMBIGUEDADES
1. «El modo escribe un agents.md propio» frente a la validación «escribe scion-agent.yaml, system-prompt.md y agents.md»: no queda claro si el modo genera solo `agents.md` o los tres; obliga a inventar el alcance del render.
2. «gana un ejemplo de hook [...] agrega una linea [...] al archivo `runs/hooks/store-specialist.queue`»: no se da el comando/cuerpo del hook ni la base de la ruta; obliga a inventar el mecanismo de append y si es relativa al desk.
3. «<fecha UTC ISO> <DESKOPS_TASK_ID>»: no fija precisión ni formato exacto; obliga a inventar el formato.
4. «Su cuerpo dice el encargo del punto 2»: no aclara si transcribe los apartados a–f o remite al `agents.md`; obliga a inventar el texto.
5. «Si el cambio deja codigo o tests sin uso, se borran»: no define cómo determinar «sin uso»; obliga a inventar el criterio.

## DRY-RUN
Lecturas: TaskDoc, `deskops/runtime/scion.py` (validación de `mode`, `scion_template_files`, renderers, `scion_child_identity`), `deskops/cli/registry.py`, tests vecinos de `tests/test_scion_runtime.py`, sección «Post-hooks on a transition» del manual y `desk/roles/deskops-tester.md` para `--model`. Cambios: ejecutar `deskops add role`; añadir `specialist` a validación/resolución y choices; crear `_render_specialist_agents_md`; ampliar identidad; tests; ejemplo de hook; `deskops advance task`. Dependencias: firmas CLI existentes, convención de `run_dir` del modo executor y esquema de hooks del manual. Validaciones futuras: pytest indicado, plantilla a `/dev/shm`, `deskops graph missing`, `sldb stores check` y `git status --short`. Nada ejecutado.

## FUTURO
Otro nodo declarará el hook en algún desk; el runner leerá la cola; el coordinador despachará con `deskops runtime template` y `scion start`, revisará y commiteará los cambios. El humano/JP valida el resultado conjunto.
