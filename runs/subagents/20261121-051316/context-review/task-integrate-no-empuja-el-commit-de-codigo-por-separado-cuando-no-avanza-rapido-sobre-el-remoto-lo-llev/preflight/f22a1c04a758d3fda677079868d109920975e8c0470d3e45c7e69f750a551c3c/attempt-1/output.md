**REFORMULACION**

Propósito: corregir en `deskops/integrate.py` el push separado del commit de código cuando este no avanza rápido sobre el remoto pero sí queda contenido en el tip. Resultado: en `_steps`, añadir el push `git push origin <code>:<branch>` solo si el commit no está en el remoto y `remote_ref` es ancestro suyo; si no avanza rápido, omitirlo e imprimir `código va con el tip: <code corto>`, dejando que el push del tip lo transporte. Repo: `deskops` (cwd `/mnt/ssd/proyectos/SLDB_1/deskops`). Límites: solo `integrate.py` (`_steps`, entorno de línea 347), `tests/test_integrate.py` y `CHANGELOG`; el resto queda fuera. Nodo ejecutable `task.code`, no agregado.

**AMBIGUEDADES**

1. «remote_ref es ancestro del commit de código»: no se define `remote_ref`. Obligaría a inventar si es `origin/main`, `origin/<branch>` o el valor ya usado por el chequeo de fast-forward.
2. «git merge-base --is-ancestor remote_ref code en la copia da 0»: «la copia» no identifica el repositorio ni el worktree donde ejecutar la comprobación. Obligaría a inventar el contexto de ejecución.
3. «p3: CHANGELOG»: no se indica sección, formato ni contenido de la entrada. Obligaría a inventar la redacción y ubicación.
4. «imprime 'código va con el tip: <code corto>'»: no se especifica canal ni nivel de salida. Obligaría a inventar si va a stdout, stderr o al log del paso.

**DRY-RUN**

Lecturas: TaskDoc, `deskops/integrate.py` alrededor de `_steps`/`code_in_origin`, `tests/test_integrate.py` y el escenario `test_tip_extends_over_a_merge_of_the_remote_branch`, y `CHANGELOG`. Cambios previstos: añadir primero un test que reproduzca el remoto con commit ajeno mergeado tras el closeout; modificar la condición de la lista de pushes; documentar en `CHANGELOG`; commitear desde el worktree indicado con `git commit -- <rutas>` y trailer `Task-Id`. Dependencias: worktree proporcionado por dispatch, fixture de remoto bare y git/pytest disponibles. Validaciones futuras: ejecutar el test nuevo antes y después, y `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py`; comprobar remoto final en el tip y mensaje emitido. Nada de esto se ejecuta aquí.

**FUTURO**

Dispatch debe entregar la ruta del worktree; un humano o el nodo de aceptación decidirá si el cambio y la entrada de `CHANGELOG` son suficientes. La integración remota y el CI quedan fuera de este nodo.
