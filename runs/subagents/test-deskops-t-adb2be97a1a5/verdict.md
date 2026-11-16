# Veredicto tester deskops-t-adb2be97a1a5

Tarea: task-los-selectores-de-deskops-aceptan-una-ruta-desk-y-el-error-explica-que-formas-acepta

**VEREDICTO: APROBADO**

## Contrato vs entrega
- Normalización (deskops/desk_paths.py:28-44 `selector_stem`): '/' → Path(repo, sel).resolve() o absoluto tal cual; `..` vía resolve(); dentro de desk/ → stem; fuera (o desk/ mismo) → ValueError "el selector apunta fuera de desk/: '<sel>'". Cumple la precisión del preflight 1.
- Aplicada en ambas rutas: disco (desk_paths.py:77 `resolve_selector`) y SLDB (doc_access.py:689-694 `resolve_document`); los mensajes citan el selector original.
- Error de no encontrado (desk_paths.py:23-25 `not_found_message`) lista id exacto, nombre de archivo, stem, fragmento único y ruta desk/...; usado también en doc_access.py:698 y :713.
- Ayuda de edit task (deskops/cli/registry.py:53-60, 251-252): ejemplo con la ruta literal `desk/drawer/tasks/<item>.md`; solo para `task`, otros subjects intactos (verificado `edit atom --help`).
- Fragmento único / ambigüedad: lógica intacta; probado en CLI (fragmento único resuelve, `task-l` da Ambiguous).
- Done_when: tests/test_tracked_selector_resolution.py `test_deskops_edit_task_edits_a_drawer_item_named_by_its_desk_path` (vía main, tmp_path) + prueba manual en desk sandbox.
- Test existente actualizado (test_tracked_selector_resolution.py:85-88): legítimo, el contrato cambia el texto del mensaje.
- Sin cambios fuera de scope en código; golden tests/fixtures/golden/help/deskops_edit_task.txt está nombrado en el scope. Los cambios en .sldb/ e inbox son del despacho/otras sesiones, no del ejecutor.

## Validación (validation.log)
test_desk_paths 16 passed; test_tracked_selector_resolution 15 passed; test_output_goldens 7 passed; test_cli_help_examples 13 passed; test_cli 102 passed. Todos rc=0.
Reproducción en HEAD: los 11 tests nuevos + el actualizado fallan; el golden difiere de la ayuda de HEAD.
Goldens: solo deskops_edit_task.txt modificado; nada borrado ni reescrito de más.

## Riesgos / observaciones (no bloqueantes)
- Una ruta se reduce a su stem: si desk/tasks tiene una tarea con el mismo stem (o con ese prefijo) gana sobre el archivo del drawer nombrado por la ruta. Es lo que pide el contrato.
- `selector_stem` acepta una ruta a un directorio dentro de desk/ (usa su nombre como stem); inocuo.
- `deskops show task` envuelve FileNotFoundError en su propio "No task found for ..." (operations.py:168/203), así que ahí no se ven las formas aceptadas; operations.py está fuera del scope de esta tarea. Candidato a drawer.
- Mensaje "fuera de desk/" en español entre mensajes en inglés (literal del contrato).
- En este host, `deskops`/`python -m deskops` fuera del checkout importa /mnt/ssd/herramientas/deskops: los cambios no se verán ahí hasta que se integren/actualice esa instalación.
- Suite completa no corrida (la corre el integrador, según el encargo).
