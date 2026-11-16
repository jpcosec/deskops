# Resultado: deskops-e-bae0befe2582

- run_id: run-deskops-e-bae0befe2582
- task: task-desk-update-deja-de-exigir-desk-reviews-vacio-y-en-un-clon-limpio-el-dry-run-da-rc-0
- session: scion://agent/deskops-e-bae0befe2582 (agente claude); session_sha256: no disponible desde dentro de la sesión
- Estado: ENTREGA LISTA (sin commit, como pide el brief)

## Cambios

- `deskops/cli/commands/desk.py`: quitado el `if` que agregaba `desk/reviews/` a `missing_desk_files`. desk update ya no cuenta la carpeta como estructura faltante.
- `tests/fixtures/golden/scaffold/update.json`: su línea de reporte nombraba `desk/reviews/`; ahora es `Missing desk structure: desk/tasks/Board.md, desk/rituals/phase.md, desk/runtimes/runtime-pi-deepseek-flash.md`. Lo verifica `tests/test_scaffold_golden.py`.
- `tests/test_cli.py`: nuevo `test_desk_update_dry_run_is_clean_in_a_fresh_clone_and_the_first_receipt_creates_reviews`. Usa tmp_path y subprocess: `git init -b main`, `deskops init .`, `git add` + `commit`, `git clone`, comprueba que el clon no tiene desk/reviews y corre `deskops desk update --root <clon>` sin --apply esperando rc 0, sin "desk/reviews/" en la salida y sin crear la carpeta. Luego `add task` y `review record task-x --kind owner`, y comprueba que existe `desk/reviews/task-x/owner-1.md` (done_when: el primer recibo crea desk/reviews/). Comprobé a mano que este test FALLA con el desk.py de HEAD ("Missing desk structure: desk/reviews/", rc 1) y pasa con el cambio.

### Archivos fuera del campo `files` (rotos legítimamente por el cambio; nota del coordinador)

- `tests/test_review_doc.py`: `test_desk_update_recreates_the_reviews_directory` afirmaba justo el comportamiento que la tarea quita (desk update --apply recrea desk/reviews). Pasa a llamarse `test_desk_update_does_not_require_the_reviews_directory`: borra la carpeta, `desk update --apply` da rc 0 y no nombra desk/reviews/.
- `tests/test_legacy_task_states.py`: `test_desk_update_apply_repairs_everything_with_an_invalid_document[warm|cold]` usaba borrar desk/reviews como "estructura faltante" para probar que --apply sigue reparando con un documento inválido. Ahora borra `desk/drawer` (sigue siendo estructura exigida y re-andamiada); la intención del test (g2/g4b) no cambia.

## Verificación de review.py

`ReviewService._write_review` escribe vía `doc_access.create_doc` -> `_write_text`, que hace `path.parent.mkdir(parents=True, exist_ok=True)`: el primer recibo crea desk/reviews/<task>/. Lo cubre el test nuevo.

## Validación (detalle en validation.log)

- tests/test_cli.py: 102 passed, rc 0
- tests/test_output_goldens.py: 7 passed, rc 0
- tests/test_review_command.py: 21 passed, rc 0
- tests/test_scaffold_golden.py (extra, por el golden): 3 passed, rc 0
- Suite completa (`-n 4`, bajo lock): 6 failed, 1065 passed, 3 skipped, 1 xfailed.
  - 3 rotos por el cambio (test_review_doc 1, test_legacy_task_states 2): ajustados como se describe arriba; re-corridos: 2 passed + 2 passed.
  - 3 fallas de entorno, que fallan igual en un worktree limpio de origin/main (/dev/shm/wt-base, ya removido):
    - tests/e2e_agent/test_agent_scenarios.py::test_reference_solutions[first-task-to-closeout] (rc 127, `pytest` no está en el PATH)
    - tests/test_ci_integration.py::test_ci_check_passes_on_a_fresh_desk (`python: command not found`)
    - tests/test_ci_integration.py::test_ci_check_fails_on_a_dangling_source_atom (misma causa)
- No volví a correr la suite completa tras ajustar los 2 archivos de test (el brief pide una sola vez); los tests ajustados se corrieron sueltos.

## Riesgos

- Un desk sin desk/reviews ya no se "repara" con desk update --apply. Es lo buscado: los lectores toleran que falte (`review status` mira `exists()`, `_review_docs` en tests también) y los escritores la crean.
- En el worktree hay cambios en `.sldb/` (InboxNoteDoc.yaml, RunDoc.yaml, store_index.yaml, store.yaml) y el RunDoc de este run que no son míos (de otras sesiones o del despacho); no los toqué.
