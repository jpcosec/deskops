## REFORMULACION

Encargo ejecutable (`task.code`): hacer que los selectores de deskops acepten una ruta `desk/...` (relativa al repo o absoluta dentro del desk) resolviendo al mismo artefacto que su stem, y que un selector irresoluble devuelva un error que enumere las formas aceptadas (id exacto, nombre de archivo, stem, fragmento único, ruta `desk/...`). Resultado observable: `edit task` con la ruta del drawer funciona en test, error nombra formas aceptadas, goldens al día, ayuda de `edit task` con ejemplo del drawer. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Superficie: `deskops/desk_paths.py`, `deskops/doc_access.py`, `deskops/cli/registry.py`, tests y golden `tests/fixtures/golden/help/deskops_edit_task.txt`. Límites: fuera de alcance la legibilidad de `promote inbox-to-drawer-task`; resolución por fragmento único sin cambios; symlinks "no se tratan aparte"; `..` vía `resolve()`.

## AMBIGUEDADES

1. "si cae dentro de <root>/desk se usa su stem" — no dice qué ocurre si cae en `desk/` pero el archivo no existe o no es artefacto. Obliga a inventar si es "no encontrado" o "fuera de desk".
2. "'..' se resuelve con resolve(); los symlinks no se tratan aparte." — `resolve()` sigue symlinks por defecto; "no se tratan aparte" no aclara si se siguen o se rechazan. Obliga a inventar la semántica.
3. "el ejemplo de ayuda usa la ruta literal desk/drawer/tasks/<item>.md" — `<item>` es placeholder; el golden exige un literal concreto. Obliga a inventar el nombre del item.

## DRY-RUN

Lecturas: los cinco archivos listados, el golden de ayuda, tests de selector. Cambios previstos: normalización de selectores con `/` contra la raíz del repo, quedarse con stem si cae en `desk/`, error común listando formas, tests en `tests/test_desk_paths.py` y `tests/test_tracked_selector_resolution.py`, actualización de golden. Dependencias: venv `../.venv`, `TMPDIR=/dev/shm`, `origin/main` para worktree base. Validaciones futuras: los cinco comandos pytest del apartado Validation, incluida suite completa y comparación de fallas en worktree limpio. Sin ejecutar nada.

## FUTURO

Otro nodo/humano: decidir las tres ambigüedades (comportamiento archivo inexistente, semántica de symlinks, item concreto del ejemplo); ejecutar la implementación y los pytest; correr worktree base para fallas preexistentes; registrar informe de fallas; commit de cierre con tests.
