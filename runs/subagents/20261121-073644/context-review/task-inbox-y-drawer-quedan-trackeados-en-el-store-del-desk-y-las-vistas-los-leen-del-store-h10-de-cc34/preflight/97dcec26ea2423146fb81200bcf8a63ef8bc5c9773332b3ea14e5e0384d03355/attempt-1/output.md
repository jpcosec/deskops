## REFORMULACION

Encargo ejecutable (task.code) en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`: hacer que inbox y drawer sean documentos trackeados del store del desk y que `deskops view` los lea de `run_view`, igual que board y task. Resultado: globs en `deskops/data/desk_declaration.yaml` para `desk/inbox/*.md` (InboxNoteDoc) y `desk/drawer/tasks/*.md` (TaskDoc); dos ViewDocs (`drawer.md`, `inbox.md`); `view.py` leyendo del store; los comandos que escriben en el drawer trackean al escribir; tests en los tres archivos indicados; `desk update --apply`; commit y nota a `graph_ui` con el hash. Límites: no verificación en navegador (la hace graph_ui, no condiciona cierre) ni migración de desks ajenos.

## AMBIGUEDADES

1. "los subcomandos de deskops/cli/commands/drawer.py que creen archivos": no se enumeran; obliga a inventar cuáles crean archivos y cuáles no.
2. "el alta de items del drawer": no identifica comando ni función; obliga a inventar el entrypoint.
3. "la misma llamada que usa message send al escribir la nota": no nombra la función API; obliga a inferirla del código.
4. "con el mismo formato que board.md y task.md": `task.md` no figura en `files:`; obliga a asumir que existe o a inventar el formato.
5. "con el mismo formato que los globs existentes de esa seccion": no se reproduce el formato; obliga a inspeccionar y decidir la sintaxis exacta (p. ej. tipo de doc, patrón).
6. "trackean al escribir": no define si el tracking es best-effort, atómico o con qué error si falla; obliga a inventar el contrato.
7. "se avisa a graph_ui para que verifique": no fija formato/canal del aviso más allá de `message send --to graph_ui`; el contenido queda a criterio.

## DRY-RUN

Lecturas: los nueve archivos de `files:`. Cambios previstos: globs en `desk_declaration.yaml`; nuevos `views/drawer.md` y `views/inbox.md`; `view.py` sustituye lectura de disco por `run_view`; `promote.py` y `drawer.py` llaman al tracking al escribir; tests en `test_view.py`, `test_message_delivery.py`, `test_inbox_promote_cli_gaps.py`. Dependencias: tipos InboxNoteDoc/TaskDoc registrados, API de tracking de `message.py`, formato de ViewDocs de `board.md`. Validaciones futuras: los tres pytest indicados, luego suite `-n 4` con triage de fallas contra worktree de `origin/main`, `desk update --apply`, commit y `message send` con hash.

## FUTURO

graph_ui verifica en navegador (no condiciona cierre). Un nodo de commit genera el hash. Un humano decide el triage de fallas preexistentes.
