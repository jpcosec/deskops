## REFORMULACION
- **Propósito:** retirar código legacy sin consumidores: el detector de `related_atoms` (`LEGACY_FIELDS`, `LEGACY_FIELD_VIOLATION`) y los alias `scaffold_desk`/`ensure_lifecycle_graph`.
- **Resultado:** esos símbolos, sus imports/usos y los tests legacy desaparecen; greps de validación vacíos y suite sin fallas nuevas.
- **Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops` (con verificación cruzada en `UIs/graph_ui`, excluyendo `runs/`).
- **Límites:** no tocar scripts en `UIs/graph_ui/runs/`; `test_fenced_yaml_examples_are_not_scanned` se conserva; `test_graph_checks.py` y `test_cli.py` solo se ejecutan.

## AMBIGUEDADES
1. "el bloque que los usa (alrededor de 188-196)" — el rango es aproximado; obligaría a inventar los límites exactos del bloque a borrar.
2. "la frase del docstring que presenta related_atoms como alias legacy" — no se cita la frase; obligaría a inventar cuál texto eliminar.
3. "los tests que importen los alias" — no se nombran; aunque el preflight afirma que ninguno los importa, obligaría a inventar qué hacer si el grep los hallara.

## DRY-RUN
- **Lecturas:** `deskops/atom_references.py`, `deskops/graph/checks.py`, `deskops/workspace.py`, `deskops/lifecycle.py`, `tests/test_atom_reference_convention.py`; greps de consumidores en `/mnt/ssd/proyectos/SLDB_1` y en `UIs/graph_ui` excluyendo `runs/`.
- **Cambios previstos:** eliminar `LEGACY_FIELDS`, `LEGACY_FIELD_VIOLATION` y la frase de docstring; imports (13-14) y bloque ~188-196 en `checks.py`; asignaciones en `workspace.py:754` y `lifecycle.py:431`; casos legacy del test.
- **Dependencias:** `.venv` en `../.venv`, `origin/main`, `git worktree`, `pytest -n 4`, `TMPDIR=/dev/shm`.
- **Validaciones futuras:** greps vacíos; pytest de los tres archivos; suite completa; comparación de fallas en worktree limpio.

## FUTURO
- Un humano confirma los límites exactos del bloque y la frase del docstring, y acepta la lista de fallas preexistentes.
- Otro nodo ejecuta los borrados, corre validaciones y cierra con commit (según `atom-code-changes-close-with-tests-and-commit`).
