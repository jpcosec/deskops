## REFORMULACION

Encargo: eliminar de `deskops` el detector legacy `LEGACY_FIELD_VIOLATION` (definido en `deskops/atom_references.py:23`, usado en `deskops/graph/checks.py:13` y `:196`) y los alias `scaffold_desk` (`deskops/workspace.py:754`) y `ensure_lifecycle_graph` (`deskops/lifecycle.py:431`), junto con sus tests legacy, dejando vacíos los greps de verificación y la suite sin fallas nuevas. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no tocar scripts viejos en `UIs/graph_ui/runs/`; el punto 2 ya se resolvió en CC33c. Resultado observable: nada fuera de `runs/` nombra esos símbolos.

## AMBIGUEDADES

1. "los tests que importen los alias" — no enumera archivos; obligaría a inventar el conjunto exacto de tests a borrar/editar más allá de `tests/test_atom_reference_convention.py`.
2. "sin fallas nuevas respecto de main" — no fija rama, commit ni método de comparación; obligaría a inventar el baseline.
3. "Verificar antes con `grep -rn 'scaffold_desk\|ensure_lifecycle_graph' /mnt/ssd/proyectos/SLDB_1/UIs/graph_ui ...` vacio" — solo cubre `graph_ui`; obligaría a asumir si hay consumidores en otros directorios de `deskops` o `UIs`.
4. Validación cita `tests/test_graph_checks.py` y `tests/test_cli.py`, ausentes en `files:`; obligaría a decidir si se permite editarlos.
5. "casos legacy" en `tests/test_atom_reference_convention.py` — no delimita qué casos son legacy; obligaría a inventar el criterio de selección.

## DRY-RUN

Lecturas: task doc, `atom_references.py`, `graph/checks.py`, `workspace.py`, `lifecycle.py`, tests citados; greps de consumidores en `deskops` y `graph_ui` excluyendo `/runs/`. Cambios previstos: borrar definición y usos de `LEGACY_FIELD_VIOLATION`; borrar alias y sus reexports; eliminar casos e imports legacy en tests. Dependencias: verificación previa de consumidores y baseline de `main`. Validaciones futuras: greps vacíos, pytest de los tres archivos, suite completa `-n 4`, comparación con `main`.

## FUTURO

Un humano confirma el baseline `main`, el universo de consumidores y si se editan los tests no listados; otro nodo ejecuta el borrado y corre las validaciones.
