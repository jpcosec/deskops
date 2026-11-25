## REFORMULACION

Encargo: corregir en `deskops/dispatch.py` el reap de ramas `deskops/<agente>` para que nunca borre una rama con commits alcanzables desde ella y no desde `main`. Debe calcularlos con `git rev-list <main>..<rama>` en el momento del reap, integrarlos con cherry-pick y, si el cálculo da 0 pero la punta no está en `main`, abortar sin borrar, saliendo con error que nombre rama y punta. Resultado: reproducción en test del caso del commit `run:` en `main` entre creación de rama y commit del ejecutor, arreglo, tests y CHANGELOG. Repo: deskops. Límites: solo reap y cálculo de commits, `tests/test_dispatch.py` y CHANGELOG; fuera el resto.

## AMBIGUEDADES

1. «git rev-list <main>..<rama>»: no define si `<main>` es la rama local, `origin/main` o el SHA remoto; obligaría a inventar la referencia exacta y su resolución.
2. «sale con error nombrando la rama y la punta»: no fija código de salida, formato ni idioma del mensaje; obligaría a inventar contrato de error.
3. «tests/test_dispatch.py con -n 4, en es_ES y en_US»: no indica cómo se parametriza el locale; obligaría a inventar el mecanismo.
4. «el cálculo de commits a integrar del reap parece no contemplarlo»: «parece» deja abierta la causa; obligaría a decidir si el fallo es el rango, el orden de merge o la detección de ancestría.
5. «Guardar la salida como reproducción en el run dir»: no especifica ruta ni nombre; obligaría a inventar ubicación.
6. «CHANGELOG»: no fija versión, sección ni formato de entrada; obligaría a inventarlo.

## DRY-RUN

Lecturas: TaskDoc, `deskops/dispatch.py` (reap y cálculo), `tests/test_dispatch.py`, CHANGELOG y estado git/worktrees. Cambios previstos: test que crea rama, hace commit `run:` en `main`, commitea en rama y ejecuta reap; corrección del rango y guarda de no borrado; entradas de test y CHANGELOG. Dependencias: pytest, git, worktree del ejecutor, locale. Validaciones futuras: el test de reproducción debe fallar antes y pasar después; ejecutar `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py` en `es_ES` y `en_US`.

## FUTURO

El nodo ejecutor crea el worktree, aplica cambios y commitea con trailer `Task-Id`; el tester valida ambos locales. Un humano o nodo de revisión decide la redacción final del CHANGELOG y la aceptación del contrato de error.
