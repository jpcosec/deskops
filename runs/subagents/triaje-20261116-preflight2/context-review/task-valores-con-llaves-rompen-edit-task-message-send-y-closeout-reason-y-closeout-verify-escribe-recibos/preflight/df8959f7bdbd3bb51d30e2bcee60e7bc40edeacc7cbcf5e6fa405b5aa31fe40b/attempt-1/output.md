## REFORMULACION

Encargo: tarea de depuración (`task.debug`) en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Propósito: reproducir en sandbox tres fallos —(a) `closeout verify` escribe recibos pese a su ayuda, (b) `--reason` con llaves rompe tras commitear y deja sin commitear la proyección, (c) `edit task`/`message send` fallan con `TemplateSyntaxError` con dos llaves de apertura— y corregirlos. Resultado: recibo de reproducción vía `deskops review record`, tests verdes para (a) y (b), y para (c) test verde o xfail citando la nota a sldb. Límites: solo `deskops/services/closure.py`, `deskops/cli/commands/closeout.py`, rutas hasta sldb y tests; sldb no se modifica. Es un nodo ejecutable simple, no un agregado.

## AMBIGUEDADES

1. "`--evidence <logs en runs/subagents/<run>/>`" y "runs/<run>/repro-<caso>.log": `<run>` no se define; obligaría a inventar el id/directorio del run y su relación con la ruta del input.
2. "si el traceback muestra frames del paquete sldb, el origen es sldb": no fija umbral ni rutas; obligaría a inventar el criterio de atribución.
3. "con las llaves exactas": no aclara si aplica a llaves simples, dobles o ambas; el resto del texto solo menciona "dos llaves de apertura seguidas".
4. "el cierre no deja archivos sin commitear": no dice si la proyección debe commitearse o excluirse; obligaría a inventar el comportamiento esperado de (b).
5. "un test xfail que cita el nombre de archivo de esa nota": la nota aún no existe; obligaría a inventar cómo obtener/registrar su nombre; tampoco fija `strict`.
6. "`--root .`" aparece en Goal/Path mientras la validación hace `cd .../deskops`; no queda claro el directorio raíz efectivo.
7. `tests/test_output_goldens.py` figura en Validation pero no en `files` ni en Scope; obligaría a inventar su pertinencia.

## DRY-RUN (hipotético)

Lecturas: TaskDoc, `closure.py` (línea ~788, `success_line.format`), `closeout.py`, `tests/test_closeout.py`, `tests/test_message_cli.py`, nota referenciada. Cambios previstos: `deskops init` en sandbox; logs por caso; `review record --kind reproduction`; escapar llaves en reason; impedir escrituras en `verify`; localizar Jinja en ruta edit/message. Dependencias: render de sldb, CLI, sandbox. Validaciones futuras: los cuatro pytest listados, suite completa y comparación en worktree de `origin/main`.

## FUTURO

Humano/otro nodo: clasificar el origen de (c) según traceback; si es sldb, `message send --to sldb` y recepción de la nota; aceptación del recibo de reproducción; decisión sobre fallas preexistentes de la suite.
