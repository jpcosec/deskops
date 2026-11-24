# Resultado (intento a2): tags migrate reindexa documentos con indice semantico viejo

run_id: run-deskops-e-e558315aff21-a2
session: scion://agent/deskops-e-e558315aff21-a2
session_sha256: n/a (sesion Scion sin archivo local)

## Cambio
- `deskops/tag_migration.py`: `stale_semantic_documents(root)` (compara `describe_model(...).documents[].semantic_tags` de sldb con `flatten_model_semantics(modelo)`) y `reindex_stale_documents(root, stale)` (untrack + track por documento en una transaccion del desk).
- `deskops/cli/commands/tags.py`: `tags migrate` informa los documentos con indice viejo; `--apply` reescribe tags y luego reindexa lo que sigue atrasado.
- `tests/test_tag_vocabulary.py`: regresion `test_tags_migrate_apply_reindexes_a_canonical_document_behind_its_model` (documento canonico indexado antes de que el modelo sume `board.tareas`; tras `migrate --apply` aparece).

## Por que por documento
sldb guarda el shard semantico bajo `source_hash`. `reindex_model`, `stores update/build`, `track(reindex=True)` y reescribir el mismo texto NO lo refrescan (probado); solo `untrack_document` (borra el shard) + `track_document_file`. No hay operacion en bloque: nota enviada a sldb (`deskops message send --to sldb`).

## Validacion
- `tests/test_tag_vocabulary.py tests/test_cli_grammar.py`: 9 passed (validation.log).
- Dry-run sobre el desk real (`dryrun-real-desk.txt`): detecta 1 documento, `TaskDocsDoc` (el de agents-md-readme).
- NO apliqué `--apply` sobre el desk real: los datos los aplica el coordinador tras traer el commit; luego `sldb find board.tareas --in semantic --type doc --store .sldb` debe dar 50.

## Revisar
Archivos: deskops/tag_migration.py, deskops/cli/commands/tags.py, tests/test_tag_vocabulary.py. No corri suite completa (pedido).
