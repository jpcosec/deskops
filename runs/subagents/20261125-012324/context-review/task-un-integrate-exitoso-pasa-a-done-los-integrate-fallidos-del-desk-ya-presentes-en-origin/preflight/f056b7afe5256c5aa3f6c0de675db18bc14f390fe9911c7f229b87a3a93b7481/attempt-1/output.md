## REFORMULACION

Encargo ejecutable `task.code`: al finalizar correctamente `deskops integrate`, recorrer `runs/queue/failed` del desk y mover a `done` cada trabajo de integración cuyo tip ya sea ancestro de `origin`, dejando una línea de log con el motivo. Repo: `deskops`; superficie: `deskops/integrate.py` (paso final) y `tests/test_integrate.py`. Límites: solo ese paso final y su test; fuera fases, encolado y otros tipos de trabajo. Validación indicada: `TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_integrate.py -k failed`.

## AMBIGUEDADES

1. Criterio de pertenencia: “cuyo tip ya es ancestro de origin” frente a “si su tarea o tip ya esta en origin (merge-base --is-ancestor)”. Obliga a inventar si se comprueba el commit tip, la tarea, o ambos, y cómo se obtiene el tip desde la tarea.
2. Ubicación y patrón: “recorre runs/queue/failed del desk” frente a “listar failed/*-integrate-*”. Obliga a inventar la ruta exacta, si es por desk, y el patrón real de nombres.
3. Registro: “dejando una linea en su log de por que” / “moverlo a done con una linea en el log”. Obliga a inventar archivo, formato, nivel y texto.
4. Condición de activación: “Tras el push exitoso” frente a “Tras un integrate exitoso”. Obliga a inventar si el barrido ocurre cuando no hubo push o cuando no hay cambios.
5. Test: “Correr solo ese test” y `-k failed`. Obliga a inventar el nombre del test nuevo y si `-k failed` selecciona exactamente los casos previstos.

## DRY-RUN

Un ejecutor leería `deskops/integrate.py`, `tests/test_integrate.py` y la estructura de `runs/queue/failed`. Tras el push exitoso, listaría entradas de integración fallidas, resolvería su tip y comprobaría `git merge-base --is-ancestor <tip> origin`; si procede, movería la entrada a `done` y escribiría una línea de log; si no, la dejaría en `failed`. Añadiría un test con un fallido ya presente en `origin` y otro ausente. Dependencias: Git, layout de cola, destino `done` y log. Validación futura: ejecutar el pytest indicado. No se ejecuta nada.

## FUTURO

Un humano debe resolver las ambigüedades anteriores. Otro nodo ejecutor implementará el cambio y el test; un nodo de validación correrá la prueba y decidirá si el resultado observable cumple el `Done When`.
