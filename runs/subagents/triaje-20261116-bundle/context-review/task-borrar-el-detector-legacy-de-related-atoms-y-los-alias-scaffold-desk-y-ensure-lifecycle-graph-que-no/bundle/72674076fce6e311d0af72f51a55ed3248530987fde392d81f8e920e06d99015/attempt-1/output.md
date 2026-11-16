## REFORMULACION

**Propósito:** retirar código legacy sin consumidores: el detector de `related_atoms` (`LEGACY_FIELD_VIOLATION` y su rama en `checks.py`) y los alias `scaffold_desk` y `ensure_lifecycle_graph`.
**Resultado:** esos símbolos y los tests legacy desaparecen; los greps de validación quedan vacíos y la suite no presenta fallas nuevas.
**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`, tocando `deskops/atom_references.py`, `deskops/graph/checks.py`, `deskops/workspace.py`, `deskops/lifecycle.py` y `tests/test_atom_reference_convention.py`.
**Límites:** no se tocan scripts en `UIs/graph_ui/runs/`; el punto 2 del drawer ya se resolvió (120bb672); fuera `.git`; solo borrado y ajuste de tests, sin refactor.

## AMBIGUEDADES

1. **“Desaparecen el detector, los dos alias y sus tests legacy”**: ¿“el detector” incluye `LEGACY_FIELDS = ("related_atoms",)` y la mención en el docstring (“`related_atoms` is a legacy alias”)? El grep de validación no las cubre. Obligaría a inventar hasta dónde llega el borrado de código muerto.
2. **“casos legacy = los tests de ese archivo que usan esos nombres”**: `test_fenced_yaml_examples_are_not_scanned` contiene `related_atoms` dentro de un bloque YAML. ¿Se borra como “caso legacy” o se conserva porque valida el escaneo de ejemplos cercados también para `atoms`? Obligaría a inventar el alcance de la eliminación de tests.
3. **Validación “`! grep -rn 'LEGACY_FIELD_VIOLATION\|def scaffold_desk\|def ensure_lifecycle_graph' deskops tests`”**: el patrón `def scaffold_desk` no detecta la asignación `scaffold_desk = seed_desk`. Obligaría a inventar un criterio adicional para verificar que el alias no sobrevive como asignación.

## DRY-RUN

**Lecturas:** los cuatro módulos, `tests/test_atom_reference_convention.py`, y los tests que solo se corren (`test_graph_checks.py`, `test_cli.py`); grep de consumidores en todo `SLDB_1` excluyendo `runs/` y `.git`.
**Cambios previstos:** quitar import y rama legacy en `checks.py`; eliminar `LEGACY_FIELD_VIOLATION` (y decidir `LEGACY_FIELDS`/docstring) en `atom_references.py`; borrar ambas asignaciones de alias en `workspace.py` y `lifecycle.py`; borrar los casos legacy del test.
**Dependencias:** `sldb.api`, pytest, `.venv`, `origin/main` para el worktree de comparación; los tests de CLI deberían usar raíces sandbox, no el `desk/` real.
**Validaciones futuras:** los cinco comandos del TaskDoc; comparar fallas con un worktree limpio de `origin/main` y listarlas en el informe.

## FUTURO

Otro nodo ejecutor corre greps y pytest, resuelve las ambigüedades y redacta el informe de fallas. Un humano o el flujo de cierre valida el informe y el commit descriptivo exigido por el átomo `code-changes-close-with-tests-and-commit`; no se generan artefactos nuevos.
