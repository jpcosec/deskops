## REFORMULACION

Nodo ejecutable, no agregado ni paquete. Propósito: corregir el test del registro de comandos para que reconozca `deskops atoms citations` como comando mutante. Resultado esperado: `('atoms', 'citations')` incluido en `MUTATING_COMMANDS` de `tests/test_command_registry.py`, manteniendo en `deskops/cli/registry.py` la entrada con `mutates=True`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo se modifica `tests/test_command_registry.py`; `registry.py`, el comportamiento del comando y otros tests quedan fuera de alcance.

## AMBIGUEDADES

ninguna

## DRY-RUN

Un ejecutor futuro leería `tests/test_command_registry.py` para localizar `MUTATING_COMMANDS` y el bloque de subcomandos de `atoms`, y leería `deskops/cli/registry.py` para confirmar que `path=('atoms', 'citations')` declara `mutates=True`. Después ejecutaría el test focalizado para verificar que la única falla es la tupla ausente. El cambio previsto sería añadir `('atoms', 'citations')` al conjunto, sin tocar otras entradas ni archivos. Dependencias: directorio de trabajo indicado, entorno `../.venv`, `TMPDIR=/dev/shm` y pytest disponible. Validaciones futuras: ejecutar `pytest -q tests/test_command_registry.py` y `pytest -q tests/test_atom_citations.py`, y comprobar mediante `git diff` que solo cambió `tests/test_command_registry.py`. No se ejecuta nada en esta revisión.

## FUTURO

El nodo ejecutor aplicará el cambio y reportará las pruebas y el diff. Otro nodo o un humano decidirá la aceptación final, el cierre y, si corresponde, el commit; también corresponderá a CI o al revisor confirmar que no hay regresiones fuera de las validaciones indicadas.
