REFORMULACION
El nodo es un preflight solo-TaskDoc, no ejecutable y sin hijos; revisa la tarea `task-el-closeout-...`. Propósito: comprobar que su TaskDoc sea comprensible y ejecutable sin contexto adicional. Resultado: informe con reformulación, ambigüedades citadas y dry-run. Repo: `deskops`. Límites: solo input explícito; sin herramientas, historial, ejecución ni decisión sobre cerrar tareas de scion. La tarea revisada pide ampliar closeout y `resolved-by` para tests no-Python, logs bajo `runs/` con `rc=0` y evidencia `<repo-id>:<sha>` del ecosistema; fuera: cambiar qué evidencia exige cada tipo.

AMBIGUEDADES
1. “que existan en el repo” / “existir en el repo”: no se especifica si “el repo” es deskops, scion o el repo UI. Obliga a inventar la resolución repo→raíz para `_test.go` y `*.test.ts(x)`.
2. “Un archivo bajo runs/ citado en references”: no se define la raíz de `runs/` (desk, workspace o repo). Obliga a inventar la base de búsqueda.
3. “cuya ultima linea no vacia es 'rc=0'” frente a “cuya ultima linea es 'rc=0'”: una permite líneas vacías finales y la otra no. Obliga a fijar un criterio.
4. “tests/test_closeout_test_paths.py existe y solo se corre”: no aclara si debe modificarse o solo ejecutarse. Obliga a decidir el alcance.

DRY-RUN
Un ejecutor futuro leería el TaskDoc, `closeout_gates.py:140-300`, `find_registered_desk` en `identity.py`, la doc de evidencia y los tests existentes. Prevé: tabla de sufijos; detector de logs `runs/`; consulta de `RepositoryReferences` al registro del ecosistema; rama `resolved-by`; doc y tests nuevos. Dependencias: raíces/registro disponibles, pytest, `TMPDIR=/dev/shm` y venv. Validaría con los tres `pytest` indicados y la suite `-n 4`; para fallas, baseline en worktree limpio de `origin/main`. Sin ejecutar nada.

FUTURO
El coordinador de scion cierra sus tres tareas; un humano decide la aceptación de fallas baseline y revisa la doc; se envían mensajes con el hash real. No son ambigüedades.
