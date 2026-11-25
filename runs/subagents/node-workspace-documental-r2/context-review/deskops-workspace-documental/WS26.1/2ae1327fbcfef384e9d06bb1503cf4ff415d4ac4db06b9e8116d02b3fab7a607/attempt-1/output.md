REFORMULACION  
WS26.1 es un nodo de implementación de `graph_ui` que prepara un candidato del drawer (UF04, paso preparar) con dos recorridos separados. El rastreado escribe directamente por `update` con `expected`, guarda de contenido WS47, admisión WS48 y `G_PAYLOAD_PRECONDITION`, solo sobre campos autorables; el no rastreado muestra propuesta, ofrece handoff explícito a `deskops edit task` y refresca, sin escritura HTTP. Resultado: candidato con evidencia, dependencias y pills persistentes/visibles; no crea tarea activa ni ruta Board, no edita `status`/`id`/`current_node`/`history`/`from_drawer` ni inventa API. Repo dueño: `graph_ui`; salida en `authoring/`, endpoints autorizados por WS12 y `tests/`. Depende de WS12, WS22, WS47, WS48 y los gates listados.

AMBIGUEDADES  
1. «El handoff se ofrece solo si una comprobación previa confirma que el selector no resuelve a una tarea activa.» Solo excluye la tarea activa; no dice qué ocurre si el selector resuelve a una tarea existente no activa (cerrada, archivada u otra). Obligaría a inventar si el comando se ofrece igualmente, con riesgo de editar una tarea ajena al candidato. La aceptación solo cubre «una tarea activa y un candidato de selector coincidente (nombre idéntico y prefijo)».

DRY-RUN  
Sin ejecutar: leería el contrato WS12 (sección 4.4, whitelist y precondición), la guarda WS47, la admisión WS48, la representación de Board WS22 y los contratos de gates; localizaría la vista de autoría y el flujo de drawer existentes. Implementaría ambas rutas y pruebas: persistencia tras recarga; 409 sin perder buffer local; propuesta/handoff sin escritura HTTP y lectura posterior; colisión con tarea activa; evidencia vacía pendiente; ausencia de `status`/Board. Validaría con store temporal real o corpus WS40 cuando exista; `G_HUMAN_READ` solo habilitaría uso en UI, no desarrollo/pruebas aisladas.

FUTURO  
WS12 fija sección 4.4, whitelist y representación de la precondición; WS47 aporta la guarda; WS48 la admisión; WS45/`G_PAYLOAD_PRECONDITION` la precondición; WS22 el Board; WS26.2 crea la tarea activa y la ruta. El humano produce el acta de `G_HUMAN_READ` y los recibos `G_UI_WRITE`/`G_WRITE_CONTRACT` por delta.
