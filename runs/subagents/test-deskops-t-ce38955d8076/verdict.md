# Veredicto del tester deskops-t-ce38955d8076

Tarea: task-desk-update-migra-las-claves-legacy-checklists-y-routine-del-frontmatter-de-las-tareas-para-que-supe
Entrega: cambios sin commitear en deskops/workspace.py, deskops/cli/commands/desk.py y tests/test_legacy_task_states.py (ejecutor deskops-e-79646a51295e).

**VEREDICTO: APROBADO**

## Revisión del diff contra el contrato

- Lista cerrada: `LEGACY_FRONTMATTER_KEYS = ("checklists", "routine")` (deskops/workspace.py:949). La tarea mixta conserva `owner` y supersede la sigue rechazando solo por 'owner' (tests/test_legacy_task_states.py:704). No se tocan write_doc, supersede ni TaskDoc.
- Dry-run: `<ruta>: legacy frontmatter key <clave>` (workspace.py:969, desk.py:430-433), orden por ruta (`_task_files` ordena) y, dentro de cada archivo, checklists antes que routine (orden de la tupla, no del archivo; los fixtures ponen routine primero, así que el orden queda probado). Entra en la condición de "up to date" (desk.py:390), con rc 1.
- --apply: `<ruta>: removed <clave> = <json.dumps(v, ensure_ascii=False, default=str, separators=(',',':'))>`, rc 0 sin errores, idempotente (el segundo --apply no hace nada, el dry-run siguiente dice "Desk is up to date.").
- Edición textual (workspace.py:987): borra solo el bloque de la clave. Antes de escribir, workspace.py:1015 comprueba que el YAML resultante sea exactamente el anterior sin esas claves; si no lo es, no escribe y lo reporta como invalid task. Probé a mano los casos límite (claves al final del frontmatter, block scalar `|` con línea en blanco, flow `[..]`/`{..}`, lista indentada, comentarios, `routine:` anidada bajo otra clave, prefijo `routine_x:`): en todos se conservan las demás claves.
- Frontmatter ilegible: no se toca, se reporta como `unreadable frontmatter` y el resto se migra. El cambio en `_task_type_migration_plan` (workspace.py:632-635) **es necesario**: con HEAD, desk update aborta con `Unexpected error: ParserError` y rc 3 (reproducido en la copia de HEAD). Que esa tarea quede fuera del plan de migración de task_type no rompe nada: legacy_task_states ya la reporta y ningún writer la podría escribir.
- Fuera de scope: ninguno. Solo cambian los 3 archivos declarados en `files`.

## Validación (validation.log)

- tests/test_legacy_task_states.py: 50 passed, rc 0
- tests/test_cli.py: 102 passed, rc 0
- tests/test_review_doc.py: 19 passed, 1 xfailed (ya existía), rc 0
- Otros tests de desk update que pasaron: test_task_types, test_command_registry, test_domain_tree, test_lifecycle_graph, test_federated_models, test_doc_readability, test_task_lifecycle_validator, test_lifecycle_seed_drift, test_scaffold_golden y test_packaging, todos rc 0.
- Fallas transitorias, que pasaron al repetirlas en el checkout:
  - test_activation_rules: 8 errores de fixture en 7 s; al repetir, 10 passed.
  - test_desk_sync (2) y test_doctor_absolute_paths (1): `ScannerError ... line 475`; al repetir, 3 passed.
  - Las 3 de test_desk_sync y test_doctor_absolute_paths también pasan en HEAD.
  - Causa probable: lecturas concurrentes con mis otras corridas en /dev/shm.
- Falla que ya existía: test_review_command.py::test_preflight_writes_attempt_evidence_and_receipt falla igual en HEAD (subject con `@sha256:`). No tiene relación con esta tarea (validation-head-baseline.log).
- La suite completa y stores build --check no se corrieron, por orden del integrador.

## Reproducción

En una copia de `git archive HEAD` en /dev/shm con el test_legacy_task_states.py nuevo, los 4 tests nuevos fallan:
- el dry-run no lista las claves;
- --apply no las quita;
- supersede rechaza por 'checklists'/'routine';
- con una tarea ilegible, desk update da rc 3 por ParserError.

## Caso real, solo lectura (marcado-sandbox.log)

Desk mínimo en /dev/shm con `deskops init` y las 3 tareas de UIs/marcado:
- El dry-run lista las 6 claves en orden, rc 1, sin escribir nada (md5 idénticos).
- --apply imprime las 6 líneas con el valor JSON, rc 0.
- El diff de cada archivo muestra solo las 5 líneas de routine/checklists borradas.
- Después del --apply, el dry-run da "Desk is up to date." y un segundo --apply no cambia nada.
- `deskops edit task ... summary` reescribe la tarea vía el modelo sin rechazo, rc 0.
- UIs/marcado no se tocó.

## Riesgos y notas

- En --apply, una tarea ilegible hace que el comando dé rc 1, como los invalid_tasks de hoy; es coherente con la precisión (4).
- El venv tiene deskops instalado desde /mnt/ssd/herramientas/deskops. Los comandos `python -m` corridos desde el checkout usan el código del checkout (verificado). Un `deskops` del PATH usaría el otro, así que conviene tenerlo en cuenta al integrar.
- Supersede sobre las tareas reales de marcado no se probó en el sandbox (exige commit, que mis reglas prohíben). Lo cubre el test unitario de la línea 704.
