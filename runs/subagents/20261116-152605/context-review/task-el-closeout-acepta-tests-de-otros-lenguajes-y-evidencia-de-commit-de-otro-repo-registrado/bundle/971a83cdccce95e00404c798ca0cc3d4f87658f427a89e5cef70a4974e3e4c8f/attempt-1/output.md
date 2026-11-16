## REFORMULACION

Propósito: ampliar las puertas de evidencia de closeout para que acepten tests no‑Python y commits de otros repos registrados. Resultado: (1) `reference_points_to_test` acepta además `*_test.go`, `*.test.sh`, `*.bats`, `*.test.ts`, `*.test.tsx`; (2) un log bajo `runs/` con primera línea `$ ` y última línea `rc=0` cuenta como test para cualquier tarea; (3) `RepositoryReferences` resuelve `<repo-id>:<sha>` también contra el registro del ecosistema (`find_registered_desk`); (4) `closeout resolved-by` acepta esos sufijos en `--test` y `<repo-id>:<sha>` en `--ref`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no cerrar las tareas de scion ni cambiar qué evidencia exige cada tipo; `tests/test_closeout_test_paths.py` solo se ejecuta.

## AMBIGUEDADES

1. "que existan en el repo y esten citados en references de la tarea" vs Scope "el archivo debe estar en files o references de la tarea": ¿basta `references`, o también `files`, y sigue rigiendo la condición de directorio `tests/`? Obliga a inventar la regla de ubicación de los sufijos nuevos.
2. "acepta en --test los sufijos de (1)": `--test` es CLI, no `references`; no dice si el archivo debe existir en la raíz, bajo `tests/` o estar en `files`. Obliga a inventar el criterio.
3. "debe buscar tambien en el registro del ecosistema": no nombra ruta/archivo del registro ni qué hacer si el id existe en ambos registros (prioridad, colisión). Obliga a inventar resolución y precedencia.
4. No dice quién construye/inyecta las entradas del ecosistema en `RepositoryReferences` (firma, llamadores en `closure.py`). Obliga a inventar el punto de integración.
5. "la doc de evidencia en docs/workflow-policy-reference.md": no identifica sección (tabla de tipos, Closeout rules, Commit Rules). Obliga a elegir destino.
6. Done When exige "la nota a scion"; Implementation Path pide también nota a marcado-ui, no repetida en Done When. Obliga a decidir si es requisito de cierre.
7. "cuya primera linea empieza con '$ '": no aclara si tolera espacios iniciales (solo la última línea tiene regla de recorte).

## DRY-RUN

Lecturas: `closeout_gates.py:140-300`, `identity.py:find_registered_desk`, rama resolved‑by de `closure.py`, `tests/test_closeout_test_paths.py`, doc. Cambios: tabla de sufijos cerrada; predicado de log `runs/` (primera línea, última no vacía sin espacios `rc=0`, dentro de root); `RepositoryReferences` con registro local+ecosistema; validación `--test`/`--ref` en resolved‑by; sección documental; tests nuevos. Dependencias: forma de `RegisteredRepository` devuelta por `find_registered_desk`, wiring CLI→servicio, `rg` de `.py` en resolved‑by. Validaciones futuras: los cuatro pytest del TaskDoc, comparación en worktree limpio de `origin/main` de fallas, informe con la lista.

## FUTURO

El ejecutor implementa; un Tester independiente valida; el coordinador envía las notas a scion y marcado-ui con el hash y cierra las tareas de scion; un humano aprueba el producto.
