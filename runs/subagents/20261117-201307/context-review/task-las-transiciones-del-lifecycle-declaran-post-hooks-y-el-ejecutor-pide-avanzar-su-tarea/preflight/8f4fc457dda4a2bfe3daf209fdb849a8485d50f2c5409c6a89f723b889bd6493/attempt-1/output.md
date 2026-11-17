## REFORMULACION

Encargo: en el repo deskops, agregar post-hooks declarados en las transiciones del lifecycle y hacer que el ejecutor pida `deskops advance task` al terminar, sin reimplementar coordinadores. Resultado: `attributes.hooks` en RelationDoc; ejecución tras persistir el avance con `DESKOPS_ROOT`, `DESKOPS_TASK_ID`, `DESKOPS_TRANSITION`, `DESKOPS_FROM_NODE`, `DESKOPS_TO_NODE`; timeout de 300 s sustituible por entrada; log por avance; rollback de status/current_node/history si falla un hook; conservación en `desk update --apply`; doctor sin deriva; `next`/`show task` muestran hooks; templates de ejecutor y coordinador actualizados; atom y manual. Límites: fuera colas/runners, rol especialista, cambios en sldb, hooks en otros comandos y declarar hooks concretos. Es una tarea ejecutable, no un agregado.

## AMBIGUEDADES

1. «una entrada puede traer `timeout` (entero, segundos) que lo reemplaza»: no define qué ocurre con timeout inválido (cero, negativo o no entero); obliga a inventar validación o comportamiento.
2. «deja el hallazgo en su resumen y senala `sciontool status blocked` con ese texto»: no fija el texto ni el formato exacto del template; obliga a inventar su redacción.
3. «imprimiendo un hallazgo de nivel error que nombra el hook, su codigo de salida y la ruta del log»: no especifica formato ni canal exacto; obliga a inventar la presentación.
4. «El texto del coordinador […] deja de avanzar el esa transicion y pasa a verificar que ocurrio»: no concreta qué verificación debe indicar; obliga a inventar la instrucción.

## DRY-RUN

Lecturas: los diez archivos listados y el atom. Cambios previstos: `lifecycle.py` (campo hooks), `services/tasks.py` (ejecución, log, rollback), `next_actions.py` y salida de `show task`, `doctor_findings.py` (ignorar hooks), camino de `desk update --apply` (conservar lista), `runtime/scion.py` (templates), pruebas, manual y atom. Dependencias: construcción de Transition desde `attributes`, `advance_task`, reescritura de semillas y comparación de doctor. Validaciones futuras: los cuatro pytest indicados, suite completa y `deskops graph missing --root .`. Sin ejecutar nada.

## FUTURO

El cierre y commit corresponden a otro nodo de closeout; el ejecutor no cierra ni commitea. Un humano decide si declara hooks concretos en algún desk y si ajusta timeouts. La ejecución real de pruebas y la verificación del resultado conjunto quedan para nodos posteriores.
