## REFORMULACION

Encargo: añadir a DeskOps la forma explícita de fijar `project_identity`, hoy solo derivada de `root.name` (`data.setdefault("project_identity", root.name)` en `deskops/workspace.py`). Resultado esperado: (1) `deskops init [path] --id <identidad>` escribe esa identidad y, si el desk ya existe con otra, no la pisa y remite a `repo whoami --set`; (2) `deskops repo whoami --set <slug> --root <desk>` reescribe solo `project_identity` en `desk/config.json` e imprime el cambio; (3) `repo register <nombre> <ruta> --id X` avisa por stderr si la identidad del desk difiere de X. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: entran `deskops/workspace.py`, `deskops/cli/registry.py`, `deskops/cli/commands/repo.py`, goldens de ayuda y `tests/test_repo_identity.py`; quedan fuera fusionar desks, editar la portada de pills y renombrar referencias en otros desks.

## AMBIGUEDADES

1. "si el desk ya existe con otra identidad, no la pisa y avisa que se use repo whoami --set": no fija texto del aviso, canal ni exit code; obliga a inventar contrato CLI.
2. "como set_job_field de deskops/queue.py": ese código no está en el input; obliga a inventar si se importa esa función o se replica la técnica.
3. "imprime \"project_identity: <vieja> -> <nueva>\"": no dice stdout/stderr ni qué mostrar cuando no existe identidad previa.
4. "avisa en stderr cuando el desk de <ruta> tiene project_identity distinto de X": no aclara si el aviso aborta el registro o solo advierte.
5. "valida que <identidad> sea un slug (minúsculas, dígitos, guiones)": no define guiones extremos, longitud ni mensaje/exit de rechazo.
6. "goldens de ayuda": no nombra ficheros ni formato; obliga a inventar qué golden actualizar.
7. "alrededor de la línea 366": la cita no corresponde al `workspace.py` adjunto; obliga a localizar por contenido.

## DRY-RUN

Lecturas: TaskDoc, `workspace.py`, `repo.py`, `tests/test_repo_identity.py`, goldens de scaffold/output y `deskops/queue.py` (citado, ausente). Cambios previstos: argumento `--id` en `cli/registry.py`, escritura condicional en `workspace.py`, rama `--set` en `RepoCLI.whoami`, aviso en `register`, cuatro tests y goldens. Dependencias: API sldb (`render_model_markdown`, store), `DeskopsOperations`. Validaciones futuras: los cuatro `pytest` de la sección Validation; suite completa con `-n 4`. Sin ejecutar nada.

## FUTURO

Decisión de JP sobre puntos 1 y 3 de la nota 20261122-222005; el worktree y commit que entrega dispatch; revisión/merge posterior.
