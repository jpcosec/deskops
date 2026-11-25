## REFORMULACION

**Propósito:** corregir el paso de push de integrate para que no empuje el sha de código cuando ya es ancestro de `origin/main`, evitando el rechazo non-fast-forward descrito.

**Resultado:** integrate detecta tras el fetch, con `git merge-base --is-ancestor <sha> origin/<branch>`, que el código ya está en origin; informa `código ya en origin: <sha>`, omite ese push y continúa con suite, checks y push de la punta. Si no es ancestro, mantiene el comportamiento actual.

**Repo:** deskops (`/mnt/ssd/proyectos/SLDB_1/deskops`). Es una tarea ejecutable, no un agregado.

**Límites:** solo el paso de push de `deskops/integrate.py`, su test y CHANGELOG. Fuera: el resto de integrate.

## AMBIGUEDADES

1. `"deskops/integrate.py"`: desde el CWD podría corresponder a `integrate.py`; obliga a inventar si la ruta es relativa a la raíz del repo o al directorio padre.
2. `"origin/main"` frente a `"origin/<branch>"`: no queda fijado si la rama es siempre `main` o configurable; obliga a inventar el origen de `<branch>`.
3. `"CHANGELOG"`: no se indica ruta ni formato; obliga a inventar dónde y cómo registrar el cambio.
4. `"commit con rutas nombradas y Task-Id"`: no se define el formato exacto del mensaje; obliga a inventar la plantilla.

## DRY-RUN

**Lecturas:** TaskDoc, `deskops/integrate.py`, `tests/test_integrate.py`, CHANGELOG.

**Cambios previstos:** p1, test que falla antes con un repo cuyo `origin/main` ya contiene el sha de código y donde integrate debe terminar ok empujando solo la punta; p2, implementar el skip tras el fetch con `git merge-base --is-ancestor`; p3, CHANGELOG y commit con rutas y Task-Id.

**Dependencias:** git, pytest y fixture de repositorio con remoto.

**Validaciones futuras:** `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py`; después, suite completa ejecutada por integrate. Sin ejecutar nada.

## FUTURO

El nodo/flujo integrate ejecutará la suite completa. Un humano revisará y aceptará el commit y el cierre de la tarea.
