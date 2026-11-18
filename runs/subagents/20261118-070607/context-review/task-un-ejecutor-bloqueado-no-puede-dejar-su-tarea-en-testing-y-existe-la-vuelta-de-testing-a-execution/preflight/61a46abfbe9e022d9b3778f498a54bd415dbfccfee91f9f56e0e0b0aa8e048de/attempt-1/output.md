## REFORMULACION
Propósito: evitar que un ejecutor bloqueado deje su tarea en `ritual-testing` y habilitar una vuelta manual a `ritual-execution`. Resultado: transición manual `task_returns_to_execution`, CLI `advance task --back --reason "<texto>"`, regla de bloqueo en el `agents.md` del executor, tests y documentación. Repo: `deskops`, cwd `/mnt/ssd/proyectos/SLDB_1/deskops`, según el TaskDoc indicado. Límites: solo los archivos listados; no aplicar a desks reales; checkout principal sin worktree ni rama, sin `git add` ni `git commit`; este preflight no ejecuta nada.

## AMBIGUEDADES
1. “`atom-code-changes-close-with-tests-and-commit`” frente a “sin git add ni git commit”. Obliga a inventar si el commit es requisito, está excluido o lo hará otro.
2. “copiando la forma de `...testing-task_hands_to_closeout.md` y `...type-task_hands_to_closeout.md`”. Obliga a inventar el esquema exacto, nombres, frontmatter y orden de la transición y su archivo de tipo.
3. “corre los post-hooks de esa transicion” y “un post-hook declarado en la transicion de vuelta corre”. Obliga a inventar qué hook declarar, su comando y cómo verificarlo.
4. “agrega a `history` la cadena `task_returns_to_execution: <texto>`”. Obliga a inventar la serialización exacta dentro de la estructura actual de `history`.
5. “`--back` en un nodo sin transicion manual sale bloqueado”. Obliga a inventar código de salida y formato exacto del mensaje.

## DRY-RUN
Un ejecutor futuro leería el TaskDoc, `deskops/data/lifecycle/`, `desk_declaration.yaml`, `lifecycle.py`, `services/tasks.py`, `cli/registry.py`, `runtime/scion.py`, los dos tests, el manual y goldens de ayuda. Añadiría la transición y su tipo, registraría `manual`, adaptaría carga/validación, implementaría `--back`/`--reason`, historia y hooks, la opción CLI, la regla en `_render_agents_md`, docs y tests; regeneraría goldens afectados. Dependencias: cargador lifecycle, servicio de tareas, firma del comando, renderer scion y sandbox de tests. Validaría con los dos pytest, goldens y `deskops doctor --root .` sobre desk nuevo. Sin ejecutar.

## FUTURO
Otro nodo aplicará la transición a desks reales con `deskops desk update --apply`. Un humano decidirá y ejecutará commit/merge y revisará la redacción del manual. La suite/CI determinará si el conjunto pasa.
