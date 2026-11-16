## REFORMULACION
Propósito: ampliar el closeout para aceptar tests de otros lenguajes y evidencia de commits de otros repos registrados. Resultado: `reference_points_to_test` acepta `*_test.go`, `*.test.sh`, `*.bats` y `runs/<run>/validation.log`; `repo:<nombre>@<sha>` se acepta si el repo está registrado, su raíz existe y el sha es ancestro de HEAD; igual para resolved-by. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: tocar `closeout_gates.py`, `closure.py`, doc y tests indicados; no cerrar las tareas de scion ni cambiar qué evidencia exige cada tipo.

## AMBIGUEDADES
1. «la misma funcion que usa message send --to (registro propio y luego el del ecosistema)»: no identifica función, módulo ni contrato; obligaría a inventar resolución, prioridad y errores.
2. «la nota a scion con el hash del commit»: no dice qué commit ni cómo obtener el hash antes de commitear; obligaría a inventar orden y contenido.
3. «el archivo debe estar en files o references de la tarea»: no define comparación literal/relativa/normalizada ni qué hacer con references que no son rutas; obligaría a inventar el matching.
4. «cuya primera linea empieza con '$ ' ... cuya ultima linea es 'rc=0'»: no aclara trim, CRLF, líneas vacías ni encoding; obligaría a inventar el parser.

## DRY-RUN
Lecturas: `closeout_gates.py:140-260`, rama resolved-by de `closure.py`, `docs/workflow-policy-reference.md`, tests citados, registro de repos y helper de `message send --to`. Cambios previstos: tabla de sufijos; validación de logs bajo `runs/`; resolución `repo:<nombre>@<sha>` mediante registro y `git merge-base --is-ancestor`; extensión de resolved-by; doc y tests. Dependencias: git, pytest, registro/helper y repos locales. Validaciones futuras: los tres pytest indicados, suite completa, baseline en worktree para fallas y envío de la nota. Sin ejecutar nada.

## FUTURO
Otro nodo implementará y commiteará, produciendo el hash para la nota; el coordinador de scion cerrará sus tres tareas; un humano decidirá la aceptación final si corresponde.
