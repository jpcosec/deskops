REFORMULACION
Nodo ejecutable `task.debug` en el repo deskops. Propósito: corregir `dispatch reap` para que no borre ramas `deskops/<agente>` con commits no alcanzables desde main y los integre con cherry-pick. Resultado: cálculo `git rev-list main..rama` al reap, guarda que aborta con error si hay 0 commits pero la punta no está en main, test de regresión del commit `run:` en main, tests en dos locales y CHANGELOG. Límites: solo `deskops/dispatch.py`, `tests/test_dispatch.py` y `CHANGELOG`; fuera el resto.

AMBIGUEDADES
1. "como _commit_run_store" / "hacer en main el commit 'run:'": no define cómo invocar ni construir ese commit en el test; obligaría a inventar helper, firma y repo temporal.
2. "los trae todos con cherry-pick": no indica orden ni resolución de conflictos; obligaría a inventar política de conflicto/abort.
3. "sale con error nombrando la rama y la punta": no fija mensaje, código de salida ni canal; obligaría a inventar el contrato observable.
4. "en es_ES y en_US": no indica cómo ejecutar ambos locales y el comando de validación no los parametriza; obligaría a inventar variables de entorno o duplicación.
5. "Guardar la salida como reproducción en el run dir": no da ruta ni nombre; obligaría a inventar ubicación y formato.
6. "el worktree que dispatch te da": no aparece el comando o procedimiento para obtenerlo; obligaría a inventar el flujo operativo.

DRY-RUN
Lecturas: task doc, `deskops/dispatch.py` (reap y cálculo), `tests/test_dispatch.py`, `CHANGELOG` y helper de commit `run:`. Cambios previstos: test de reproducción; cálculo con `rev-list main..rama`; cherry-pick de todos; guarda de no borrado; tests de locale; CHANGELOG; commit con `Task-Id`. Dependencias: repo git con main, creación de rama/worktree, pytest y locales. Validaciones futuras: ejecutar `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`, comprobar reproducción antes/después y que la rama con commits pendientes no se borra. Sin ejecutar.

FUTURO
Otro nodo o ejecutor deberá obtener worktree y run dir, ejecutar reproducción y validación; un humano decidirá si acepta el mensaje/exit code y la política de conflictos.
