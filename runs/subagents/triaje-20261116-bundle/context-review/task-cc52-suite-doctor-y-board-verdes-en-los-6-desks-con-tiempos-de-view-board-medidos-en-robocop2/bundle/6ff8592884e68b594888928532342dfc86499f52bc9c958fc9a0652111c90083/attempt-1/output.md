REFORMULACION
Nodo ejecutable `task.code` (no agregado). Propósito: verificar en robocop2, en deskops, sldb, spec2viz, scion, pron y graph_ui, `deskops desk update` (dry-run; sin `--apply` en ajenos), `deskops doctor`, `deskops view board`, `sldb stores check` y `sldb rules check`. Resultado: tabla en `docs/config-vs-code.md` (Verificación) y en el TaskDoc con rc y resumen; suites de deskops y sldb con `-n 4` sin fallas nuevas contra main; tiempos de `deskops view board --root .` en deskops: 3 frío/3 caliente, medianas, caliente < 1 s; arreglos de código de deskops con test y commit; mensajes a desks ajenos. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`; lectura en `/mnt/ssd/proyectos/SLDB_1/<repo>` y `UIs/graph_ui`. Límites: no arreglar desks ajenos ni UI de navegador; en deskops, `--apply` solo si el dry-run reporta divergencias, en commit aparte.

AMBIGUEDADES
1. “el resumen por comando es rc + numero de errores y de alertas”: no define qué salida cuenta como error/alerta ni cómo extraerlos; obligaría a inventar un parser.
2. “cada test que falle se corre con el mismo comando en un worktree limpio de origin/main”: no fija venv, dependencias ni `TMPDIR` del worktree; obligaría a inventar el entorno de comparación.
3. “3 corridas en frio” y “se reportan medianas; caliente < 1 s”: no fija umbral ni criterio de aceptación para frío; obligaría a inventar uno.
4. “las demas se reportan por inbox al repo dueño” frente a “`deskops message send --to <repo>`”: no aclara si son equivalentes ni el formato; obligaría a inventar canal/formato.

DRY-RUN
Lecturas: TaskDoc, `docs/config-vs-code.md`, `tests/`, DAG y ayuda/implementación de CLI. Cambios previstos: añadir tabla y tiempos; si la verificación delata causa en deskops, parche+test+commit; enviar mensajes. Dependencias: robocop2, venv `../.venv`, acceso a los 6 desks, borrado de `.sldb_cache` y `${XDG_CACHE_HOME:-$HOME/.cache}/sldb`, worktree de `origin/main`. Validaciones futuras: suites `-n 4`, comparación de fallas contra main, medianas de view board, tabla completa y mensajes. Sin ejecutar nada.

FUTURO
Un humano/Board decide la aceptación del informe y del umbral; los dueños de desks ajenos resuelven hallazgos; nodos posteriores consumen tabla y commits. No es ambigüedad.
