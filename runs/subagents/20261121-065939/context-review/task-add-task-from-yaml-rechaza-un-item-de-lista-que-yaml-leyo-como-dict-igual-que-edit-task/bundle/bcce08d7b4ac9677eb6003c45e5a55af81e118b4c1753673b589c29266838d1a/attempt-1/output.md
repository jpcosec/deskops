## REFORMULACION
Propósito: corregir `deskops add task --from-yaml` y el payload JSON inline para que rechacen ítems no-string en campos de lista de strings del TaskDoc (`validation`, `depends_on`, `inherits_from`, `atoms`, `evidence`, `references`), en lugar de guardar el `repr` de un dict. Resultado: el comando falla con código distinto de 0, el mensaje nombra campo e índice y sugiere entrecomillar el ítem, y no se crea la tarea; los ítems string no cambian. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no convertir silenciosamente el dict a string ni cambiar `edit task`; incluye `parse_input.py`/punto de conversión a TaskDoc y un test nuevo. Es una tarea ejecutable `task.code`, no un agregado.

## AMBIGUEDADES
1. “un campo de lista de strings del TaskDoc (validation, depends_on, inherits_from, atoms, evidence, references)”: no se adjunta el esquema que confirme que esa es la lista exacta y completa; obligaría a inventar campos o tipos.
2. “el payload JSON inline”: no se define opción, formato de invocación ni si comparte la misma validación; obligaría a inventar la interfaz.
3. “el mensaje nombra el campo, el indice y sugiere entrecomillar el item”: no hay texto ni formato exacto; obligaría a inventar la redacción.
4. “parse_input.py (...) o el punto de add task donde el payload se convierte a TaskDoc”: no hay criterio para elegir el punto canónico; obligaría a inventar la ubicación.
5. “con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra”: el input solo contiene TaskDoc e instrucción; obligaría a inventar rituales, pills, átomos y archivos.

## DRY-RUN
Lecturas: TaskDoc; `deskops/cli/parse_input.py` (`_load_yaml_mapping`, línea ~70, y `_ensure_mapping_payload`); ruta de `add task` a TaskDoc; esquema/pydantic; `tests/test_cli.py` y `tests/test_add_task_from_drawer.py`; fixtures YAML. Cambios previstos: validar antes de crear que cada ítem de los campos lista sea `str`; emitir error no-cero con campo, índice y sugerencia; añadir test negativo y positivo, comprobando ausencia de `desk/tasks/<id>.md`. Dependencias: repo, `../.venv`, pytest y pydantic. Validaciones futuras: ejecutar los tres comandos pytest indicados, incluida la suite completa, y comparar fallas en un worktree limpio de `origin/main`.

## FUTURO
Un nodo ejecutor implementará el cambio y correrá las validaciones; un humano o revisor decidirá la redacción final del mensaje y aceptará fallas preexistentes; otro nodo revisará el diff. Aquí no se ejecuta nada.
