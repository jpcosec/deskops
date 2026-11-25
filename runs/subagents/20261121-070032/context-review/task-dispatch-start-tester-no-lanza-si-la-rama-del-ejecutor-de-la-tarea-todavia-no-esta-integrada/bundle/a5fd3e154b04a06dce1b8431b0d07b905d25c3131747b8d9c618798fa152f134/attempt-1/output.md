## REFORMULACION
Nodo ejecutable (`task.code`), no agregado. Propósito: impedir que el tester se lance antes de que la rama del ejecutor esté integrada, evitando validar `main` sin el cambio. Resultado: `dispatch start` para rol tester detecta una rama `deskops/<ejecutor>` asociada a la tarea (vía `scion_child_identity`, intentos 1 y 2) con commits fuera de la rama principal; entonces sale con `EXIT_BUSY` (3) e imprime `en espera: la rama deskops/<ejecutor> de la tarea no está integrada`. Sin esa rama, lanza. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops` según cwd; el input no lo nombra. Límites: solo `deskops/dispatch.py` (start, rol tester), `tests/test_dispatch.py` y `CHANGELOG`; no modifica el reap, la integración Git ni la cola.

## AMBIGUEDADES
1. “por scion_child_identity, intentos 1 y 2”: no define formato, fuente ni cómo mapear identidad→tarea→rama. Obligaría a inventar el esquema de identidad y si el intento 3 queda excluido.
2. “rama principal”: no nombra `main`, `master` ni remoto. Obligaría a inventar la ref exacta.
3. “la rama deskops/<ejecutor> … con commits que no están en la rama principal” y “Cuando el reap la integra y la borra”: no aclara múltiples ramas, ramas obsoletas ni qué significa “integrada”. Obligaría a inventar la política de detección.
4. “sale con EXIT_BUSY (3…)” e imprime el mensaje: no indica si el mensaje va a stdout/stderr, ni si `EXIT_BUSY` ya existe. Obligaría a inventar contrato de salida.
5. “commit con 'git commit -- <rutas>' y trailer Task-Id”: no fija formato ni valor del trailer. Obligaría a inventar la convención.

## DRY-RUN
Lecturas: TaskDoc, `deskops/dispatch.py`, `tests/test_dispatch.py`, `CHANGELOG` y utilidades de identidad/Git existentes. Cambios previstos: test nuevo que simula rama con commit fuera de principal y espera salida 3/mensaje; test sin rama que espera lanzamiento; implementación de la comprobación antes del lanzamiento; entrada de CHANGELOG; commit indicado. Dependencias: resolución de identidad, ref principal, acceso Git, constante de salida y semántica de reintento de cola. Validación futura: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`. Sin ejecutar nada.

## FUTURO
El reap integra y borra la rama; la cola interpreta `EXIT_BUSY` y reintenta; un humano decide la convención exacta de commit/trailer y aprueba el cierre tras la validación.
