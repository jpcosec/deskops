## REFORMULACION

Encargo ejecutable (TaskDoc `task.code`) en el repo `deskops`. Propósito: que las transiciones del lifecycle declaren post-hooks deterministas y que el ejecutor pida `deskops advance task` al terminar, en lugar de que el coordinador lo haga a mano. Resultado: (1) `attributes.hooks` leído en `lifecycle.py` y ejecutado por `advance_task` tras persistir, con env `DESKOPS_*`, timeout y log; (2) fallo o timeout revierte status/current_node/history y devuelve error con hook, código y log; (3) hooks preservados por `desk update --apply` y no marcados por doctor; (4) `next`/`show task` los muestran; (5) templates de ejecutor y coordinador ajustados; (6) atom y manual actualizados. Límites: sin runner/cola de hooks pesados, sin rol especialista, sin cambios en sldb, sin hooks en closeout, sin declarar hooks concretos en ningún desk.

## AMBIGUEDADES

1. «Cada hook tiene un tope de tiempo»: no fija valor ni configuración; obligaría a inventar el default y su clave.
2. «se guarda en un log por tarea y transicion bajo el directorio de runs del desk»: no define ruta ni nombre; obligaría a inventar el layout.
3. «la tarea vuelve al estado exacto que tenia antes de la transicion (status, current_node e history)»: no aclara si se revierten archivos escritos por hooks; obligaría a inventar el alcance de la atomicidad.
4. «`attributes.hooks` es la unica parte que pertenece al desk»: no especifica merge (lista completa, por `name`, orden); obligaría a inventar la semántica de conservación.
5. «muestran los hooks de la transicion que sigue»: presupone una única transición siguiente; obligaría a inventar qué mostrar si hay varias candidatas.
6. «un hallazgo ... que nombra el hook, su codigo de salida y la ruta del log»: en timeout no hay código; obligaría a inventar qué valor imprimir.

## DRY-RUN

Lecturas: `lifecycle.py` (construcción desde `edge.metadata["attributes"]`), `services/tasks.py::advance_task`, `doctor_findings.py`, camino de `desk update --apply`, `workflow/next_actions.py`, `runtime/scion.py`, tests y manual citados. Cambios previstos: campo hooks en Transition; ejecución secuencial con timeout, env y log en `advance_task`, con reversión ante fallo; merge de hooks en reescritura de semilla y exclusión en doctor; salida en `next`/`show`; textos de ambos templates; atom y manual. Dependencias: persistencia de estado/history, resolución del directorio de runs, subprocess con timeout, escritor de logs, comparación de semillas. Validaciones futuras: los cuatro pytest indicados, suite completa y `deskops graph missing --root .`. Nada ejecutado.

## FUTURO

Decisiones humanas: valor de timeout, layout de logs, semántica de merge y presentación ante múltiples transiciones. Otro nodo/humano ejecutará el commit y cierre conforme a los atoms; el ejecutor solo deja evidencia y pide `advance`.
