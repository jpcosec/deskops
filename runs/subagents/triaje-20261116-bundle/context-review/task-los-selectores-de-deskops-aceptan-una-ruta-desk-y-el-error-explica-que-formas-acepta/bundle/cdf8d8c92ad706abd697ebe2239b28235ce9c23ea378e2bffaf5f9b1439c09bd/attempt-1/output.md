REFORMULACION

Encargo del nodo: tarea de código en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Propósito: que los selectores de deskops acepten una ruta relativa al repo (`desk/...`) o absoluta dentro de `desk` y resuelvan al mismo artefacto que su stem; que un selector no resuelto dé un error que enumere las formas aceptadas (id exacto, nombre de archivo, stem, fragmento único, ruta `desk/...`); y que la ayuda de `edit task` incluya un ejemplo con un item del drawer. Resultado: cambios en `deskops/desk_paths.py`, `deskops/doc_access.py`, `deskops/cli/registry.py` y goldens; tests en `tests/test_desk_paths.py` y `tests/test_tracked_selector_resolution.py`. Límites: no toca `promote inbox-to-drawer-task`; la resolución por fragmento único conserva el error de ambigüedad actual; normalización con `resolve()`, symlinks sin trato aparte. El bundle no incluye Board ni rituales enrutados: solo TaskDoc, pill, átomos y archivos.

AMBIGUEDADES

1. «si el selector contiene '/', se resuelve con Path(root, selector).resolve() (o tal cual si es absoluto); si cae dentro de <root>/desk se usa su stem» — no aclara si `root` es la raíz del repo o `desk_root`; `resolve_selector` recibe `desk_root`. Obligaría a inventar la base y el punto de aplicación.
2. «un selector que no resuelve da un error que lista las formas aceptadas» frente a «La resolucion por fragmento unico no cambia (sigue dando el error de ambiguedad actual)» — no dice si el mensaje de ambigüedad también enumera formas. Obligaría a inventar el alcance del mensaje.
3. «el ejemplo de ayuda usa la ruta literal desk/drawer/tasks/<item>.md» — no aclara si `<item>` es literal o un nombre concreto. Obligaría a inventar el texto del golden.
4. «si cae fuera, error 'el selector apunta fuera de desk/'» — no da el mensaje completo (prefijo, selector interpolado). Obligaría a inventar el literal exacto.
5. «edit task con la ruta del drawer funciona en un test» — no indica en qué archivo. Obligaría a inventar ubicación.

DRY-RUN

Lecturas: `desk_paths.py`, `doc_access.py`, `cli/registry.py`, los dos tests y el golden `deskops_edit_task.txt`. Cambios previstos: normalizar en `resolve_selector`/`resolve_document`; mensaje común; ayuda; tests; golden. Dependencias: decidir si la normalización va en `desk_paths` (recibe `desk_root`) o en `doc_access` (recibe `root`); que golden y test coincidan. Validaciones futuras: los cinco comandos pytest del TaskDoc y, ante fallas, worktree limpio de `origin/main`. Sin ejecutar.

FUTURO

Un humano o el ejecutor decide la base de normalización, los literales exactos de error y ejemplo, y la ubicación del test de `edit task`; después corre las validaciones y el worktree.
