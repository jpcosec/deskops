PASA

# Veredicto del tester

Commit del ejecutor: `0e5c961c2b70613d625a46f83ef52890babc558c` ("edit task refreshes the Board task line", `Task-Id: task-board-no-refleja-deskops-edit-task-goal`).

Archivos del commit:
- `deskops/doc_access.py`: tras editar `title`, `goal` o `status` de una tarea, dentro de la misma `desk_transaction`, vuelve a guardar `desk/tasks/Board.md` (`refresh_board`), de modo que sldb re-renderiza la composición `task_summaries`.
- `tests/test_edit_task_refreshes_board.py`: test nuevo (init en `tmp_path`, add task con goal viejo, edit goal, y edit title; comprueba el Board).
- `CHANGELOG.md`: entrada en Fixed.

Tests ejecutados (de a uno, `TMPDIR=/tmp`, `-p no:cacheprovider`):
- `tests/test_edit_task_refreshes_board.py` -> 1 passed.
- `tests/test_cli.py` (validación declarada en el desk) -> 102 passed.
- `tests/test_edit_template_placeholder.py tests/test_task_files_of_other_repo.py` (regresión del camino `edit task`) -> 14 passed.

No existe `tests/test_doc_access.py` para el módulo tocado, así que no hubo test de módulo adicional que correr.

Observación de entorno: `python` no está en PATH y el `.venv` del workspace apunta a un Python 3.12 ausente; los tests se corrieron con el Python 3.13 de la herramienta uv (`/home/scion/.local/share/uv/tools/deskops/bin/python`) y pytest 9.2.0 en `/tmp/pytest-target`. No se modificó código ni tests del repo.
