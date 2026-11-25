## REFORMULACION
Encargo ejecutable (`task.code`): borrar en el repo `/mnt/ssd/proyectos/SLDB_1/deskops` el detector legacy de `related_atoms` y los alias `scaffold_desk` y `ensure_lifecycle_graph`, sin consumidores. Resultado: desaparecen `LEGACY_FIELDS`, `LEGACY_FIELD_VIOLATION` y la frase del docstring en `atom_references.py`; imports y bloque legacy en `graph/checks.py`; las asignaciones alias en `workspace.py` y `lifecycle.py`; y los tests legacy de `test_atom_reference_convention.py`. Límites: solo esos cinco archivos y tests que importen alias; no tocar `UIs/graph_ui/runs/`; `test_graph_checks.py` y `test_cli.py` solo se ejecutan; se conserva `test_fenced_yaml_examples_are_not_scanned`; verificar consumidores antes.

## AMBIGUEDADES
1. “la frase del docstring que presenta related_atoms como alias legacy”: no se cita literalmente. Obliga a decidir si se borra solo la oración sobre `related_atoms` o también la mención a `source_atoms`.
2. “el bloque que los usa (alrededor de 188-196)”: el rango es aproximado. Obliga a fijar exactamente qué líneas de `_atom_reference_findings` se eliminan, aunque el criterio funcional —quitar el tratamiento de `LEGACY_FIELDS`— acota el cambio.

## DRY-RUN
Lecturas: los cinco archivos nombrados; greps de consumidores en `/mnt/ssd/proyectos/SLDB_1` excluyendo `runs/` y `.git`. Cambios previstos: eliminar constantes, imports, rama legacy, alias y test legacy; ajustar docstring. Dependencias: ninguna producción fuera de esos archivos; tests afectados. Validaciones futuras: grep vacío, pytest de `test_atom_reference_convention.py`, `test_graph_checks.py`, `test_cli.py`, suite completa con `-n 4`; fallas nuevas comparadas contra worktree limpio de `origin/main`. No se ejecuta nada.

## FUTURO
Otro nodo ejecutor aplicará el diff y producirá informe de pruebas; un humano resolverá las ambigüedades 1 y 2 y aceptará la lista de fallas preexistentes; el cierre exige commit descriptivo.
