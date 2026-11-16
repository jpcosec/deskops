## REFORMULACION

El nodo debe eliminar código legacy sin consumidores en `/mnt/ssd/proyectos/SLDB_1/deskops`: el detector de `related_atoms`/`LEGACY_FIELD_VIOLATION` y los alias `scaffold_desk` y `ensure_lifecycle_graph`, junto con sus tests legacy. Resultado: esos nombres desaparecen de `deskops/` y `tests/`, los greps de validación quedan vacíos y la suite no presenta fallas nuevas. Límites: tocar solo `atom_references.py`, `graph/checks.py`, `workspace.py`, `lifecycle.py` y los casos legacy de `tests/test_atom_reference_convention.py`; no tocar scripts en `UIs/graph_ui/runs/` ni refactorizar fuera de alcance. Es una tarea concreta, no un agregado ni paquete ejecutable.

## AMBIGUEDADES

1. **Alcance del “detector”**: “LEGACY_FIELD_VIOLATION vive en deskops/atom_references.py:23 y se usa en deskops/graph/checks.py:13 y 196” y “Desaparecen el detector”. Solo se nombran constante y usos; no se define si también se elimina lógica de parseo/soporte de `related_atoms`. Obliga a inventar la frontera exacta.
2. **Tests legacy no enumerados**: “casos legacy = los tests de ese archivo que usan esos nombres”. No lista funciones concretas; obliga a decidir por inspección qué casos eliminar, especialmente si usan los nombres indirectamente.
3. **Cobertura de “nada”**: “nada fuera de runs/ los nombra” frente a “grep -rn --include=*.py”. No aclara docs, configuración u otros archivos no `.py`; obliga a decidir si se actualizan o se ignoran.
4. **Cierre y commit**: los átomos incluyen “atom-code-changes-close-with-tests-and-commit”, pero “Done When” solo exige greps vacíos y suite sin fallas nuevas. No se indica commit, mensaje ni actualización de `status`/`history`; obliga a inventar el procedimiento de cierre.

## DRY-RUN

Sin ejecutar: leer `atom_references.py`, `graph/checks.py`, `workspace.py`, `lifecycle.py` y `tests/test_atom_reference_convention.py`; ejecutar greps de consumidores excluyendo `runs/` y `.git`. Cambios previstos: quitar `LEGACY_FIELD_VIOLATION`, sus importaciones/usos y los casos legacy; borrar las definiciones de los dos alias y cualquier export/import asociado. Dependencias: que los greps confirmen ausencia de consumidores y que exista una baseline de tests. Validaciones futuras: los comandos de grep y pytest listados, incluida la suite completa y la comparación de fallas en worktree limpio de `origin/main`.

## FUTURO

Un nodo ejecutor realizará lecturas, greps, ediciones y tests, y entregará un informe con fallas nuevas o preexistentes. Un humano decidirá la aceptación de fallas no reproducidas, el commit/cierre y la transición de estado de la tarea.
