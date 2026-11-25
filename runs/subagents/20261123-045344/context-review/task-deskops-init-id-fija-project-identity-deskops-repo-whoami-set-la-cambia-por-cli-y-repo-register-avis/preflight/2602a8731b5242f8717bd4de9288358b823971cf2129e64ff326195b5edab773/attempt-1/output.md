## REFORMULACION

**Propósito:** eliminar la edición manual de `project_identity` añadiendo una vía CLI explícita y una advertencia de desalineación. **Resultado:** `deskops init [path] --id` fija la identidad al crear; `deskops repo whoami --set <identidad> --root <desk>` la cambia validando slug y mostrando “vieja -> nueva”; `deskops repo register <nombre> <ruta> --id X` advierte por stderr si la identidad del desk difiere de X. Incluye cuatro tests y goldens de ayuda. **Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`. **Límites:** entran `workspace.py`, `cli/registry.py`, `cli/commands/repo.py`, goldens y `tests/test_repo_identity.py`; quedan fuera editar la portada de pills, fusionar desks y renombrar referencias antiguas. Es un nodo ejecutable `task.code`, no un agregado ni paquete.

## AMBIGUEDADES

1. “valida que <identidad> sea un slug (minúsculas, dígitos, guiones)”: no define longitud, si admite guion inicial/final, guiones consecutivos ni cadena vacía; obligaría a inventar la regex exacta.
2. “si el desk ya existe con otra identidad, no la pisa y avisa que se use repo whoami --set”: no aclara qué hacer si coincide, si existe sin `project_identity`, si la ruta no es un desk ni qué código de salida usar; obligaría a inventar esos casos.
3. “reescribe solo project_identity en desk/config.json … sin tocar el resto del archivo”: no especifica comportamiento si falta la clave, hay duplicados o comentarios; obligaría a inventar la política de edición.
4. “avisa en stderr cuando el desk de <ruta> tiene project_identity distinto de X”: no define si la advertencia cambia el exit code ni qué hacer si falta o no puede leerse `desk/config.json`; obligaría a inventar el manejo de errores.
5. “goldens de ayuda”: no identifica qué salidas de ayuda ni qué archivos golden deben actualizarse; obligaría a inventar el alcance exacto.

## DRY-RUN

**Lecturas:** TaskDoc; `deskops/workspace.py` (zona de `setdefault`); `deskops/cli/registry.py`; `deskops/cli/commands/repo.py`; `set_job_field` en `deskops/queue.py`; tests y goldens existentes. **Cambios previstos:** escribir primero los cuatro tests; añadir `--id` a init; implementar `whoami --set` con validación y reescritura mínima; añadir advertencia a register; actualizar goldens de ayuda. **Dependencias:** parser CLI existente, lectura/escritura de `desk/config.json`, helper de slug y patrón de `set_job_field`. **Validaciones futuras:** ejecutar los tres pytest indicados y luego la suite completa con `-n 4`; comprobar que init sin `--id` conserva el scaffold actual.

## FUTURO

Dispatch debe entregar el worktree para el commit con `Task-Id`. JP decide los puntos 1 y 3 de la nota 20261122-222005, fuera de alcance. Un revisor o CI valida tests y goldens; la alineación de otros desks queda para otro nodo o decisión humana.
