## REFORMULACION
Nodo ejecutable `task.code`: corregir la expectativa de `tests/test_command_registry.py` para que `MUTATING_COMMANDS` incluya `("atoms", "citations")`, alineándola con `deskops/cli/registry.py`, que ya declara `mutates=True`. Resultado: pasan las validaciones indicadas y el diff solo toca ese test. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no modificar `deskops/cli/registry.py`, el comportamiento del comando ni otros tests.

## AMBIGUEDADES
1. “Sale: … cualquier otro test” frente a la validación de `tests/test_atom_citations.py`: obliga a decidir si ese test solo se ejecuta o también puede requerir cambios si falla.
2. El átomo ligado exige “tests pass and the completed change is recorded in a descriptive git commit”, pero “Done When” solo pide tests y que “git diff solo toca tests/test_command_registry.py”; obliga a decidir si este nodo debe commitear o si el commit corresponde al cierre.

## DRY-RUN
Lecturas: `tests/test_command_registry.py`, `deskops/cli/registry.py`, el TaskDoc, ambos átomos y, si hace falta, `tests/test_atom_citations.py`. Cambio previsto: agregar la tupla `("atoms", "citations")` al conjunto `MUTATING_COMMANDS`, sin tocar el registro. Dependencias: que la entrada del registro exista con `mutates=True` y que el golden/registro ya contenga el comando. Validaciones futuras: ejecutar los dos `pytest` indicados con `TMPDIR=/dev/shm` y comprobar el diff limitado a `tests/test_command_registry.py`. No se ejecuta nada.

## FUTURO
Un nodo ejecutor aplicará el cambio y correrá las validaciones. El cierre —y, si se confirma la lectura del átomo, el commit descriptivo— corresponde a otro nodo o a una decisión humana.
