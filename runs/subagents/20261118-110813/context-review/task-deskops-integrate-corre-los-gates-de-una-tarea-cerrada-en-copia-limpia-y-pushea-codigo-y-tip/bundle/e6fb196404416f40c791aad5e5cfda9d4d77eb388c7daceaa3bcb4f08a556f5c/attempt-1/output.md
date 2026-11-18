REFORMULACION

Propósito: automatizar como trabajo de cola del host la receta manual de integración (copia limpia, suite, gates del desk, push de código y tip, actualización del checkout de herramientas) que hoy ejecuta a mano el integrador. Resultado: comando `deskops integrate --task <id> --root .` (con `--dry-run` y `--task-from-env`), campo `integrate` en `DeskConfig`, módulo `deskops/integrate.py`, registro en `deskops/cli/registry.py`, tests nuevos y sección `Integrate` en `docs/operator-manual.md`. Repo: workspace `desk`/deskops, checkout principal, sin worktree ni rama, sin `git add`/`git commit`. Límites: fuera declarar configuración en desks reales, el timer del host, reintentos/rebase y cambios en sldb; los tests usan un remoto bare en `tmp_path`, nunca remoto real.

AMBIGUEDADES

1. "El tip es el commit de cierre de la tarea, que se busca con `git log` por el asunto exacto `closeout: <id de la tarea>`". No dice sobre qué repositorio/ref corre ese `git log` antes de clonar; obliga a inventar repo, rango y flags (`--all`, rama, profundidad).
2. "el commit de codigo es el sha de 40 caracteres que aparece en `references` de la tarea". No especifica entrada ni formato; obliga a inventar la regla de extracción (primera coincidencia hex, prefijo, campo concreto).
3. "el comando acepta `--task-from-env`, que toma el id de `DESKOPS_TASK_ID`". No define exclusividad ni precedencia con `--task`; obliga a inventar la gramática del parser.
4. "su ultima entrada de history es el registro de cierre". No describe la forma del registro; obliga a inventar cómo reconocerlo (campo, texto o tipo).

DRY-RUN

Lecturas previstas: TaskDoc, `desk/config.json` y `config.local.json`, `.sldb/store.yaml` del tip, `deskops/queue.py` (para reutilizar `_wait_reason`), `deskops graph missing`, tests de closeout vecinos y fixtures golden de ayuda. Cambios previstos: crear `deskops/integrate.py`; añadir submodelo `integrate` en `deskops/config.py`; registrar comando como `mutates` en `registry.py`; crear `tests/test_integrate.py`; declarar el comando en `tests/test_cli.py`, `test_cli_grammar.py` y `test_command_registry.py`; regenerar goldens; ampliar `docs/operator-manual.md`. Dependencias: `_wait_reason`, `graph missing`, CLI de tareas/closeout, git local y repos bare en `tmp_path`. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/test_integrate.py`, guardianes del CLI con ayuda, y `pytest -q tests/test_queue.py`.

FUTURO

Declarar `integrate` en `desk/config.json` reales; instalar el timer del host; regenerar/revisar goldens de ayuda; ejecutar la suite y los guardianes; commit de cierre y push real del integrador; decidir política de reintentos o rebase (fuera de alcance).
