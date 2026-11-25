## REFORMULACION
Propósito: agrupar en `graph_ui` la integración de autoría explícita desde candidato, evidencia declarada, dependencias y contexto/pill binding, más enrutamiento en Board y capa lista, sin confundir Board route con ejecución. Resultado: agregado no ejecutable; se cumple cuando WS26.1 y WS26.2 cumplen su aceptación, y sus salidas son las de ambos. Repo dueño: `graph_ui`. Límites: no implementa por sí mismo, no crea API/modelo, no autoriza promoción sin contrato WS12, no habilita mutaciones UI antes de G_HUMAN_READ; commits, permisos y closeout según WS12 y gates.

## AMBIGUEDADES
ninguna.

## DRY-RUN
No hay ejecución del agregado. Un ejecutor futuro leería WS26, `dag.yaml`, la guía y las aceptaciones de WS26.1/WS26.2; no cambiaría archivos por WS26. WS26.1 prepara el candidato: recorrido rastreado con `expected`, WS47, WS48 y G_PAYLOAD_PRECONDITION; recorrido no rastreado con propuesta, handoff y refresco, sin crear tarea activa. Transfiere a WS26.2 el candidato preparado, evidencia, dependencias y pills. WS26.2, tras autorización humana, crea/enruta la tarea en Board y muestra capa lista, invocando solo operación admitida por WS12; si falta, handoff. Dependencias: WS12, WS22, WS48; gates por delta. Validación conjunta: aceptación de ambos hijos, recibos G_UI_WRITE/G_WRITE_CONTRACT por delta, G_HUMAN_READ antes de mutaciones UI y WS30 después.

## FUTURO
WS12 fija el contrato por delta (sección 4.4, W01, HO-12, commits previos); WS47/WS48 aportan guardado/admisión; WS22, representación Board; WS45, precondición; P01 emite actas G_UI_WRITE; WS16 produce G_HUMAN_READ; WS30 valida el recorrido humano. La promoción real o cierre ocurre por canal autorizado o handoff, no aquí.
