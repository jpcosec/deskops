## REFORMULACION

Encargo: eliminar código legacy sin consumidores en el repo `/mnt/ssd/proyectos/SLDB_1`, paquete `deskops`. Resultado: en `deskops/atom_references.py` desaparecen `LEGACY_FIELDS`, `LEGACY_FIELD_VIOLATION` y la frase del docstring que presenta `related_atoms` como alias; en `deskops/graph/checks.py` sus imports (13-14) y el bloque que los usa (~188-196); en `deskops/workspace.py:754` el alias `scaffold_desk = seed_desk`; en `deskops/lifecycle.py:431` el alias `ensure_lifecycle_graph = write_lifecycle_graph`; en `tests/test_atom_reference_convention.py` los casos que esperan `legacy_atom_reference_field`. Se conserva `test_fenced_yaml_examples_are_not_scanned`. Límites: no tocar `UIs/graph_ui/runs/` ni scripts viejos; verificar consumidores con grep excluyendo `runs/` y `.git`; los tests `test_graph_checks.py` y `test_cli.py` solo se ejecutan.

## AMBIGUEDADES

1. “la frase del docstring que presenta related_atoms como alias legacy” — el docstring es un párrafo continuo; no se especifica hasta dónde recortar ni la redacción resultante. Obliga a inventar el texto final del docstring.
2. “en tests/test_atom_reference_convention.py los tests que esperan el hallazgo legacy_atom_reference_field” frente a “casos legacy = los tests de ese archivo que usan esos nombres” — `test_fenced_yaml_examples_are_not_scanned` contiene `related_atoms` dentro de un bloque cercado pero no espera el hallazgo. Obliga a decidir si “usan esos nombres” incluye ese test; la instrucción posterior de conservarlo resuelve solo parcialmente.
3. “Sin fallas nuevas […] se corre con el mismo comando en un worktree limpio de origin/main” — no define si la comparación es por test o por mensaje de fallo. Obliga a inventar el criterio de equivalencia.

## DRY-RUN

Lecturas: los cinco archivos nombrados y greps de consumidores. Cambios: borrar constantes, imports, bloque `LEGACY_FIELDS`, aliases, import `LEGACY_FIELD_VIOLATION` en el test y `test_related_atoms_produces_one_legacy_finding`; ajustar docstring. Dependencias: `parse_atom_reference`/`iter_atom_reference_values` deben quedar intactos; ningún consumidor fuera de `runs/`. Validaciones futuras: los greps de cierre vacíos y las cuatro invocaciones de pytest (tres archivos y suite completa), con baseline en worktree de `origin/main` para fallas.

## FUTURO

El executor realiza borrados y corridas; el commit descriptivo lo exige `atom-code-changes-close-with-tests-and-commit`. Un humano decide las ambigüedades 1-3 y valida el informe de fallas preexistentes.
