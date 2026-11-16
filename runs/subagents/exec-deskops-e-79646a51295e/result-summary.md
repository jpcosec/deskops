# Resultado del ejecutor deskops-e-79646a51295e

- run_id: run-deskops-e-79646a51295e
- task: task-desk-update-migra-las-claves-legacy-checklists-y-routine-del-frontmatter-de-las-tareas-para-que-supe
- session: scion://agent/deskops-e-79646a51295e (session_sha256: no disponible desde la sesión)

## Cambios (todos dentro de `files`)

- `deskops/workspace.py`
  - `LEGACY_FRONTMATTER_KEYS = ("checklists", "routine")` (lista cerrada), `LegacyFrontmatterKey`
    (`pending_line()` = `<ruta>: legacy frontmatter key <clave>`; `removed_line()` =
    `<ruta>: removed <clave> = <json.dumps(valor, ensure_ascii=False, default=str, separators=(',',':'))>`).
  - `legacy_frontmatter_keys(root)`: tareas de `<root>/desk/tasks` en orden de ruta y, dentro de cada
    archivo, checklists antes que routine. Un frontmatter ilegible se salta (ya lo reporta
    `legacy_task_states` como invalid task).
  - `migrate_legacy_frontmatter_keys(root)`: edición textual (`_without_top_level_keys`): borra solo
    la línea `clave:` y sus líneas de bloque (indentadas, `- ` y blancas dentro del bloque); el resto
    del archivo queda byte a byte. Antes de escribir verifica que el YAML resultante sea el anterior
    sin exactamente esas claves; si no, no toca el archivo y lo devuelve como invalid task (rc 1).
  - `_task_type_migration_plan`: un frontmatter ilegible se salta en vez de lanzar ParserError.
    Necesario para la precisión (4) del coordinador: hasta ahora `desk update` abortaba entero
    ("Unexpected error: ParserError", rc 3) ante una tarea con frontmatter malformado, antes de
    reportarla; ahora la reporta como invalid task y migra el resto.
- `deskops/cli/commands/desk.py`: dry-run reporta `- Legacy task frontmatter keys to remove: N key(s)`
  con una línea `  - <ruta>: legacy frontmatter key <clave>` por clave y da rc 1 (entra en la
  condición de "up to date"); `--apply` imprime `Removing legacy task frontmatter keys...` y
  `- <ruta>: removed <clave> = <json>` por clave, rc 0 si no hubo errores. Corre justo después de la
  migración de estados legacy, así el stores check posterior ve los hashes nuevos y refresca índices.
- `tests/test_legacy_task_states.py`: 4 tests en desk sandbox (tmp_path) con la forma de marcado
  (routine y luego checklists en bloque):
  - dry-run lista las 4 claves en orden, rc 1, no escribe, no menciona la clave `owner` (lista cerrada);
  - --apply quita solo esas líneas (archivo = original menos el bloque), conserva `owner`, TaskDoc lo
    lee, rc 0; luego dry-run "Desk is up to date." y segundo --apply sin cambios (idempotente);
  - supersede rechaza antes con "frontmatter key 'checklists'; frontmatter key 'routine'", tras
    --apply cierra la tarea (Closeout-Mode: superseded); la tarea mixta sigue rechazada solo por 'owner';
  - una tarea con frontmatter ilegible no se toca, se reporta como unreadable frontmatter, y las demás
    se migran (rc 1 en --apply por la inválida).

## Validación

- tests/test_legacy_task_states.py: rc 0 (50 passed)
- tests/test_cli.py: rc 0
- tests/test_review_doc.py: rc 0 (1 xfail preexistente)
- Suite completa: NO corrida. Quedó para el integrador por orden del coordinador wA:p1 (la corre él
  una vez por integración en copia limpia); la que estaba en cola esperando el lock se canceló
  (kill del pid 2421449, rc 143, nunca empezó). Sin comparación con origin/main por lo mismo.
- Comprobación extra, solo lectura sobre marcado: copia en /dev/shm de las 3 tareas reales de
  UIs/marcado (task-close-the-runtime-pipeline-baseline, task-close-the-source-and-marker-model-baseline,
  task-design-the-runtime-architecture-and-extension-model): se detectan las 6 claves y la migración
  quita exactamente las 5 líneas de cada una (diff), sin fallas. marcado no se tocó.

## Riesgos

- La edición textual asume claves top-level en columna 0 (como las escribe sldb); si un caso raro no
  cuadra, la verificación por YAML lo deja sin tocar y lo reporta, no lo corrompe.
- El cambio en `_task_type_migration_plan` también afecta a `desk update --apply` (migrate_task_types):
  la tarea ilegible ya no se planifica; antes todo el comando abortaba.
- Tras `--apply` el store queda con hashes viejos de esas tareas hasta el refresco de índices que el
  mismo `--apply` hace (verificado: el dry-run siguiente da "Desk is up to date.").
