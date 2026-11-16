# Veredicto del tester deskops-t-64f1e63a41b3

Tarea: task-deskops-atoms-citations-queda-declarado-como-comando-que-modifica-en-el-test-del-registro-de-comando

## Comprobaciones
1. `git diff -- tests/test_command_registry.py`: una sola línea añadida, `("atoms", "citations"),` en MUTATING_COMMANDS, en el bloque de subcomandos de atoms. Nada más en ese archivo.
2. `deskops/cli/registry.py:1439-1472`: la entrada `path=("atoms", "citations")` declara `mutates=True` (no tocado por esta entrega).
3. El comando escribe de verdad: `deskops/services/atoms.py` `atom_citations(write=True)` -> `_write_citations`, que en `desk_transaction` crea el RelationTypeDoc `cited_by` y RelationDoc por cita vía `doc_access.create_doc` (y retira los obsoletos).
4. `pytest -q tests/test_command_registry.py` (working tree): 3 passed.
5. `pytest -q tests/test_atom_citations.py`: 5 passed (sin cambios en ese test).
6. Copia de HEAD de test_command_registry.py en /dev/shm: `test_mutating_commands_are_declared_explicitly` FALLA con "Extra items in the left set: ('atoms', 'citations')" — el cambio es el que corrige la falla. (El fallo de goldens en la copia es artefacto de ubicación: ruta relativa a `__file__`.)
7. Done When: ambos tests pasan y el diff de la entrega solo toca tests/test_command_registry.py (los demás cambios sucios son de otra tarea, closeout verify --run-dir, según el brief).

Evidencia: validation.log en este directorio. No se editó código, no se commiteó; /dev/shm limpiado.

VEREDICTO: APROBADO
