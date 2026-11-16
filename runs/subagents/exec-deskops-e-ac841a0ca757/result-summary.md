# Result summary — exec-deskops-e-ac841a0ca757

- run_id: run-deskops-e-ac841a0ca757
- task: task-los-selectores-de-deskops-aceptan-una-ruta-desk-y-el-error-explica-que-formas-acepta
- session: scion://agent/deskops-e-ac841a0ca757 (session_sha256: no disponible para el ejecutor)

## Cambios

- `deskops/desk_paths.py`: nuevo `selector_stem(desk_root, selector)` — si el selector contiene `/`, se resuelve con `Path(<repo>, selector).resolve()` (tal cual si es absoluto; `..` resuelto por `resolve()`, sin trato especial de symlinks); dentro de `<repo>/desk` devuelve su stem, fuera (o el propio `desk/`) lanza `ValueError("el selector apunta fuera de desk/: '<selector>'")`. Nuevo `ACCEPTED_SELECTOR_FORMS` + `not_found_message(what, selector)`: el error de "no encontrado" ahora es `No <what> file found for selector '<sel>'. Accepted forms: an exact id, a file name, a stem, a unique fragment, or a desk/... path.` `resolve_selector` normaliza el selector y cita el selector original en los mensajes. Fragmento único/ambigüedad sin cambios.
- `deskops/doc_access.py`: `resolve_document` consulta SLDB con el stem del selector-ruta (superficies trackeadas) y usa `not_found_message`; `resolve_artifact_selector_multi` también. `editable_artifact` no cambia: su fallback al drawer ya funciona con la ruta.
- `deskops/cli/registry.py`: `edit task` gana epílogo (RawDescription) con ejemplo `deskops edit task desk/drawer/tasks/<item>.md scope ...` y una línea sobre rutas desk/... . `SELECTOR_HELP` global no se tocó (cambiaría decenas de goldens fuera de scope).
- `tests/fixtures/golden/help/deskops_edit_task.txt`: golden al día (en scope por nota del coordinador, fuera del campo files).
- `tests/test_desk_paths.py`: ruta relativa, absoluta, `..`, fuera de desk, sin `/`, mensaje con las formas aceptadas.
- `tests/test_tracked_selector_resolution.py`: test existente de igualdad del mensaje actualizado a propósito (el mensaje ahora lista formas); nuevos: ruta en superficie trackeada (relativa y absoluta), fuera de desk, `editable_artifact` con ruta del drawer, error de edit task con formas, y `deskops edit task desk/drawer/tasks/<item>.md scope ...` vía `main` sobre un desk sandbox (`lifecycle_desk`, tmp_path) — cumple el done_when.

## Validación (detalle en validation.log)

1. test_desk_paths.py: 16 passed, rc 0
2. test_tracked_selector_resolution.py: 15 passed, rc 0
3. test_output_goldens.py: 7 passed, rc 0
4. test_cli_help_examples.py: 13 passed, rc 0
5. Suite completa (-n 4, bajo lock): 3 failed, 1079 passed, 3 skipped, 1 xfailed. Las 3 fallas son las de entorno conocidas (rc 127, `pytest` no está en PATH): `tests/e2e_agent/test_agent_scenarios.py::test_reference_solutions[first-task-to-closeout]`, `tests/test_ci_integration.py::test_ci_check_passes_on_a_fresh_desk`, `tests/test_ci_integration.py::test_ci_check_fails_on_a_dangling_source_atom`. Fallan igual en un worktree limpio de origin/main (6d94cf26) en /dev/shm/wt-base, ya removido. Sin fallas nuevas.

## Riesgos / notas

- Según el contrato, la ruta se reduce a su stem: en `edit task` se busca primero en desk/tasks; si existe allí una tarea activa con ese mismo stem (o cuyo nombre empiece por él), gana sobre el archivo del drawer que nombraba la ruta. Es el comportamiento pedido ("se usa su stem"), pero una ruta no garantiza el archivo exacto.
- Las rutas relativas se resuelven contra la raíz del repo (`--root`), no contra el cwd.
- Mensaje "fuera de desk/" en español literal por el contrato; el resto de mensajes del módulo están en inglés.
- `pytest tests/test_output_goldens.py --update-golden` en este entorno reescribió además 4 goldens de ayuda (ancho de terminal) y borró 5 goldens de output de otros tests; los restauré con `git checkout` y solo quedó el cambio de `deskops_edit_task.txt`. Los goldens restaurados pasan en la validación 3.
- `.sldb/` modificado/untracked (RunDoc, store_index, store.yaml) no es mío: venía del despacho.
- Las notas nuevas en desk/inbox/ y .sldb/core/{models/InboxNoteDoc.yaml,documents/InboxNoteDoc/} que aparecen en git-status.txt las escribieron otras sesiones durante mi corrida; no son mías.
