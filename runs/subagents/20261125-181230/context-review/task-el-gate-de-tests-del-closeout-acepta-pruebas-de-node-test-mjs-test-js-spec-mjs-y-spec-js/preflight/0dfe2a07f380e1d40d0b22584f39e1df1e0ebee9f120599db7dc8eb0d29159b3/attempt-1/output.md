## REFORMULACION

Propósito: que el gate de tests del closeout acepte pruebas Node escritas como `node --test`. Resultado: extender `_is_test_suffix` en `deskops/services/closeout_gates.py` para aceptar `.test.mjs`, `.test.js`, `.spec.mjs` y `.spec.js`, manteniendo las reglas de ubicación bajo `tests/` o declarado en `files`; actualizar el docstring de `reference_points_to_test` y añadir cobertura en su test existente. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo ese gate y su test; fuera el resto de gates; no incluir `Task-Id` en el commit de código. Cierre: una referencia a `tests/x.test.mjs` cuenta como evidencia y un `.mjs` común no; pasa `TMPDIR=/mnt/ssd/tmp/sldb1 PYTHONPATH=. pytest -q -k reference_points_to_test tests`.

## AMBIGUEDADES

1. “buscar con grep reference_points_to_test en tests/”: no indica el archivo exacto ni qué hacer si hay cero o varias coincidencias; obligaría a inventar cuál es “el test existente”.
2. “Test: agregar casos en el test existente del gate de tests ... para un .test.mjs bajo tests/ que cuenta y un .mjs que no es test que no cuenta”: solo explicita dos casos; no aclara si deben cubrirse los cuatro sufijos nuevos; obligaría a inventar la cobertura mínima.
3. “con las mismas reglas de ubicación (bajo tests/ o declarado en files)”: no define cómo se comprueba “declarado en files” ni si aplica igual a cada sufijo; obligaría a inventar el criterio de ubicación.
4. “No poner Task-Id en el commit de codigo”: no fija formato alternativo del mensaje; obligaría a inventar la convención exacta.

## DRY-RUN

Lecturas previstas: el TaskDoc; `deskops/services/closeout_gates.py`, en particular `reference_points_to_test` y `_is_test_suffix`; grep de `reference_points_to_test` en `tests/`; convenciones del test existente. Cambios previstos: ampliar la detección de sufijos y el docstring; añadir casos al test del gate para un `.test.mjs` bajo `tests/` que cuenta y un `.mjs` no-test que no cuenta. Dependencias: entorno pytest con `PYTHONPATH=.` y `TMPDIR` indicado. Validaciones futuras: ejecutar el comando de validación y comprobar los cuatro sufijos y las reglas de ubicación. Sin ejecutar nada.

## FUTURO

Un nodo ejecutor posterior producirá el parche y la salida de pytest; un humano revisará y aprobará el cierre y el mensaje de commit sin `Task-Id`.
