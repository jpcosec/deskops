REFORMULACION
Nodo ejecutable `task.code`, no agregado. En deskops (checkout principal, sin worktree/rama) debe: crear el RoleDoc `sldb-store-specialist` con `deskops add role` y el modelo de `desk/roles/deskops-tester.md`; añadir modo `specialist` a `deskops runtime template` (resolución por sufijo, `_render_specialist_agents_md`, identidad `deskops-s-<12hex>`); y documentar el hook `encola-especialista-de-store`. Resultado: código, tests y manual actualizados, sin commitear. Límites: no tocar sldb, no declarar/despachar el hook, no implementar el runner, no tocar archivos ya modificados, borrar código/tests sin uso.

AMBIGUEDADES
1. "en la carpeta de roles del desk" / "el RoleDoc nuevo": falta ruta; obliga a inventar ubicación y archivo nuevo permitido.
2. "guardar ambas salidas en el run-dir asignado": no define cómo obtenerlo; obliga a inventar variable/argumento/convención.
3. "`sldb docs update <ruta>` para un documento registrado cuyo archivo cambio fuera del CLI" vs "cualquier cambio de contenido" NO se toca: contradicción; obliga a decidir si se repara o se nota.
4. "`deskops runtime template role-sldb-store-specialist --mode specialist`" vs `sldb-store-specialist`: obliga a inventar si `role-` es prefijo obligatorio, opcional o error.
5. "`--title "store: <id del documento>"`" para hallazgos sin documento registrado: obliga a inventar el id.
6. "los tests de message, inbox y repo identity": no enumera rutas; obliga a inventar cuáles evitar.

DRY-RUN
Un ejecutor leería el TaskDoc, `desk/roles/deskops-tester.md`, `scion.py`, `registry.py`, tests vecinos, manual y `git status`. Crearía el RoleDoc; añadiría `specialist` a validación/resolución, renderer, identidad y `choices`; añadiría tests; editaría el manual. Depende de convenciones CLI, modelo del tester, ubicación del run-dir, JSON de `sldb stores check` y `deskops message send`. Validaría con pytest, `runtime template`, `graph missing`, `stores check` y `git status`. Sin ejecutar nada.

FUTURO
El coordinador/humano resuelve ambigüedades, declara el hook en un desk, despacha al especialista, implementa el runner de cola y commitea. El repo sldb y la ejecución real del especialista quedan fuera.
