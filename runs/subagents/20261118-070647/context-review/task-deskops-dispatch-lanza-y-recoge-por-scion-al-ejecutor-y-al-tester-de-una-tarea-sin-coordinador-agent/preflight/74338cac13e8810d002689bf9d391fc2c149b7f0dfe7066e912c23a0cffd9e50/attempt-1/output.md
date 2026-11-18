## REFORMULACION

Encargo: crear en el repo deskops el grupo de comandos `deskops dispatch` (`start` y `reap`) para que la cola del host lance y recoja sola a ejecutor y tester de una tarea, sin coordinador agente. Resultado: módulo `deskops/dispatch.py`, campo `dispatch` en `DeskConfig`, registro en `deskops/cli/registry.py`, tests nuevos y declaraciones en los tests guardianes, goldens de ayuda y ejemplo en `docs/operator-manual.md`. Límites: no integrar/push (otra tarea), no tocar desks reales ni scion, checkout principal sin worktree/rama, sin `git add`/`git commit`.

## AMBIGUEDADES

1. "El run_dir es `runs/subagents/exec-<nombre del agente>`" frente a "el nombre del agente": no se aclara si el nombre ya incluye el prefijo `exec-`; obligaría a inventar si el resultado es `exec-exec-…`.
2. "con `role` (id o nombre del RoleDoc)" y "en la carpeta `<templates_dir>/<nombre del rol>`": si la config trae un id, no se dice cómo obtener el nombre; obligaría a inventar resolución id→nombre.
3. "prompt: una linea que nombra la ruta absoluta de prompt.md y pide leerlo completo y cumplirlo": texto literal no especificado; obligaría a inventar la frase.
4. "existe `result-summary.md` en su run_dir, que se deduce del nombre y del rol como en (1)b": `scion list` solo aporta `labels["deskops.task_id"]`; no se dice de dónde sale el rol; obligaría a inventar la deducción.
5. "Sin campo `dispatch` ... salen con codigo 2 y un mensaje": mensaje no especificado; obligaría a inventar su texto.

## DRY-RUN

Lecturas: TaskDoc y RoleDocs, `deskops/runtime/scion.py`, `config.py`, `registry.py`, tests y goldens existentes, `docs/operator-manual.md`, `deskops show task` en runtime. Cambios: módulo nuevo con una única función que envuelve `subprocess.run` para scion; campo de config; registro del grupo; tests nuevos; declaraciones de ayuda; goldens. Dependencias: tarea de cola del host (ya cumplida) y binario `scion` en PATH. Validaciones futuras: `pytest -q tests/test_dispatch.py` con `TMPDIR=/dev/shm`, `tests/test_scion_runtime.py`, guardianes CLI y regeneración de goldens de ayuda.

## FUTURO

Integrar y pushear corresponde a otra tarea; declarar config/hooks en desks reales y cambios en scion quedan fuera; la regeneración de goldens requiere decisión/revisión humana sobre qué archivos conservar.
