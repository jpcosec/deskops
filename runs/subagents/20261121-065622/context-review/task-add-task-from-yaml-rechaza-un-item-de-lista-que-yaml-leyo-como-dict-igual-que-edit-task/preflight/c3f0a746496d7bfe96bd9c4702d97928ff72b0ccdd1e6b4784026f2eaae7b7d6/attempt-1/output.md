## REFORMULACION

Encargo ejecutable (`task.code`) en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`: corregir `deskops add task --from-yaml` —y el payload JSON inline— para que rechace, con código distinto de 0 y sin crear la tarea, cualquier item no-string en campos de lista de strings del `TaskDoc`, nombrando campo, índice y sugiriendo entrecomillar. Los strings válidos conservan el comportamiento actual. Límites: tocar `deskops/cli/parse_input.py` (`_load_yaml_mapping`, `_ensure_mapping_payload`) o el punto de conversión a `TaskDoc`, añadir un test; no convertir silenciosamente dicts a string ni modificar `edit task`.

## AMBIGUEDADES

1. «validation, depends_on, inherits_from, atoms, evidence, references»: no se explicita el esquema real del `TaskDoc`; obligaría a inventar si `evidence` existe y si hay otros campos lista.
2. «(y el payload JSON inline)»: no se indica su ruta de entrada ni si comparte validación con YAML; obligaría a inventar el punto exacto de intercepción.
3. «un mensaje que nombra validation y el indice»: no fija texto, formato ni base del índice (0 o 1); obligaría a inventar el contrato del mensaje.
4. «no se crea ningun archivo»: no aclara si incluye temporales, directorios o escrituras parciales; obligaría a inventar el alcance de atomicidad.

## DRY-RUN

Lecturas hipotéticas: TaskDoc, `parse_input.py`, ruta `add task`, esquema `TaskDoc`, `tests/test_cli.py` y `tests/test_add_task_from_drawer.py`. Cambios previstos: validar items de listas contra `str` antes de crear la tarea; emitir error con campo, índice y sugerencia de entrecomillado; añadir test con YAML no entrecomillado (falla, sin `desk/tasks/<id>.md`) y entrecomillado (crea). Dependencias: cargador YAML, CLI existente, pydantic y entorno pytest. Validaciones futuras: ejecutar los dos pytest indicados y la suite completa; comparar fallas en worktree limpio de `origin/main`.

## FUTURO

Otro nodo ejecutará la implementación y devolverá evidencia de tests; un humano decidirá la aceptación final y si las fallas preexistentes justifican excepción.
