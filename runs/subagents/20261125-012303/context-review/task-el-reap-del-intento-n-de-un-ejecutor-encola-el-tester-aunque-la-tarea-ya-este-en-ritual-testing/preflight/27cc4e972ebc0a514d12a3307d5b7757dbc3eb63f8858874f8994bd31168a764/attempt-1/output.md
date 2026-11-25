## REFORMULACION
Encargo: corregir `deskops/dispatch.py`, en la fase de reap, para que tras integrar el commit de un intento de ejecutor (cualquier número de intento) se encole `dispatch-tester` para esa tarea si no existe ya un tester vivo ni una entrada pendiente. Resultado esperado: cambio en el reap más tests en `tests/test_dispatch.py` que cubran el intento 2 y la no duplicación. Límites: solo el reap de dispatch y sus tests; queda fuera la máquina de estados de rituales. Repo: el que contiene `deskops/dispatch.py` (raíz no declarada explícitamente).

## AMBIGUEDADES
1. «si no hay un tester vivo ni pendiente»: no define cómo detectar "vivo" (estado, heartbeat, proceso) ni "pendiente" (entrada de cola, nombre exacto). Obligaría a inventar los criterios y las APIs de consulta.
2. «tras integrar commits de un ejecutor» / «sea el intento que sea»: no fija el punto exacto del reap ni si aplica también cuando la integración falla o no hay commit. Obligaría a inventar la condición de disparo.
3. «encolar dispatch-tester»: no especifica la función/API de encolado ni el payload o prioridad. Obligaría a inventar la interfaz concreta.
4. «con uno ya pendiente no se duplica»: no aclara el ámbito de deduplicación (por tarea, por intento, por cola) ni el comportamiento si hay tester vivo pero su intento es anterior. Obligaría a inventar la semántica.
5. Rutas relativas `deskops/dispatch.py` y `tests/test_dispatch.py`: no declaran la raíz del repo. Obligaría a asumirla.

## DRY-RUN
Lecturas: `deskops/dispatch.py` (flujo de reap e integración), `tests/test_dispatch.py` y utilidades de cola/estado usadas por dispatch. Cambios previstos: añadir en reap, tras integrar, una comprobación de tester pendiente/vivo por tarea y encolar `dispatch-tester` si no existe; añadir dos tests (tarea en `ritual-testing` con intento 2 reapeado deja un pendiente; con pendiente previo no duplica). Dependencias: APIs existentes de cola, estado de tareas y helpers de test. Validaciones futuras: `pytest -q tests/test_dispatch.py`. Todo hipotético, sin ejecutar.

## FUTURO
Un nodo ejecutor implementará el cambio y ejecutará los tests; un humano o nodo revisor validará que el caso del intento 2 queda cubierto y que no hay duplicación, y decidirá el cierre de la tarea.
