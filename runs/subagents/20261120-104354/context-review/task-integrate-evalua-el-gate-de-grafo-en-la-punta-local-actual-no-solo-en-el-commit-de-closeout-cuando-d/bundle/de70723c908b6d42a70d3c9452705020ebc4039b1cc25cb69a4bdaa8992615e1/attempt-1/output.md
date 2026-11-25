REFORMULACION
Nodo ejecutable (`task.code`), no agregado. Propósito: que `integrate` no se bloquee cuando una referencia colgante ya fue corregida por commits de desk posteriores al closeout. Resultado: si entre el commit de closeout y HEAD solo hay commits que tocan `desk/`, `.sldb/` o `runs/`, `integrate` toma HEAD como tip, corre los gates sobre él y lo empuja, informando `tip extendido a <sha>: solo commits de desk`; si hay commits con código, tests o docs, mantiene el closeout. Repo: deskops (`deskops/integrate.py`, `tests/test_integrate.py`, `CHANGELOG`). Límites: no tocar el resto de los gates; esta revisión no ejecuta nada.

AMBIGUEDADES
1. «nada de código, tests ni docs»: no define qué rutas cuentan como cada categoría ni qué hacer con rutas mixtas o ajenas (p. ej. `requirements`, `Makefile`, `.github`). Obliga a inventar la clasificación.
2. «corre los gates sobre ella y la empuja»: no especifica qué gates ni a qué remoto/rama se empuja. Obliga a inventar alcance y destino.
3. Título («el gate de grafo») frente a Goal («corre los gates»): no aclara si el tip extendido aplica solo al gate de grafo o a todos. Obliga a inventar alcance.
4. «git diff --name-only <closeout>..HEAD»: no cubre merges ni el caso de que closeout no sea ancestro de HEAD. Obliga a inventar fallback.
5. «Si hay commits con código posteriores»: no aclara si «código» incluye tests y docs. Obliga a inventar criterio.
6. «un commit de desk posterior que la arregla»: no dice si el arreglo borra la referencia o añade el documento. Obliga a inventar el fixture.
7. «Lo dice en su salida ('tip extendido a <sha>: solo commits de desk')»: no fija stream, formato exacto ni idioma. Obliga a inventar contrato de salida.

DRY-RUN
Un ejecutor futuro leería `integrate.py` (find_tip/cálculo del tip), `tests/test_integrate.py`, `CHANGELOG` y el historial git. Cambiaría el cálculo del tip con un helper que compruebe `git diff --name-only <closeout>..HEAD` contra el conjunto permitido; añadiría dos tests (closeout con referencia colgante y commit desk que la corrige; commit posterior en `src/` que mantiene closeout); actualizaría CHANGELOG. Dependencias: git, repo accesible, closeout resoluble. Validación futura: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py`. Sin ejecución.

FUTURO
Otro nodo implementa y ejecuta los tests; un humano aprueba el alcance de gates y la política de empuje; CI valida el conjunto. No son ambigüedades del input.
