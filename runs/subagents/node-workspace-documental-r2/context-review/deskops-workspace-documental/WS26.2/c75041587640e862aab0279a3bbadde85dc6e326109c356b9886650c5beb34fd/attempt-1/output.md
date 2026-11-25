REFORMULACION  
Encargo de WS26.2: en `graph_ui`, enrutar explícitamente una tarea en el Board y representar la capa lista por dependencias/no solapamiento. Resultado: `deskops show board` muestra la tarea, la UI la distingue de una en ejecución y la capa lista queda separada de ejecución, dependencias pendientes y archivos solapados. Límites: la creación+enrutado es operación conjunta W01 de WS12, nunca parcial ni efecto oculto de WS26.1; no implementar promoción nueva, solo invocar la operación completa admitida o dejar handoff/pendiente; no usar heurística optimista con glob/no-resolución dudosa. Repo: `graph_ui`; salidas en `frontends/mindmap/views/workspace/routing/`, endpoints autorizados por WS12 y `tests/`.

AMBIGUEDADES  
1. «Enrutar un TaskDoc ya existente no tiene operación pública con precondición (HO-12).» Obliga a inventar qué hace el ejecutor con ese caso: bloquear, ofrecer handoff, mostrar no disponible o usar otra vía; no se fija resultado ni aceptación específica.  
2. «revisión supervisor antes de marcar lista» Obliga a inventar quién es el supervisor, qué evidencia deja y cómo se comprueba; sin actor ni registro, la aceptación no es comprobable.

DRY-RUN  
Lecturas: contrato WS12 (W01, promoción, commits previos, rutas/`files`, ritual), vistas Board WS22, preparación de candidato WS26.1, admisión WS48, Board/lifecycle/ritual de deskops y `files` de TaskDocs. Cambios previstos: ruta de enrutamiento en `routing/`, vista de capa lista, llamada a W01 solo si existe, estados handoff/pendiente y pruebas. Dependencias: WS12, WS22, WS26.1, WS48; gates G_HUMAN_READ para uso de mutaciones UI, G_UI_WRITE/G_WRITE_CONTRACT por delta; G_CLOSEOUT ya satisfecho. Validaciones futuras: `deskops show board`, distinción respecto a ejecución, separación de capa lista, reglas de igualdad/contención/glob, handoff sin promoción terminada, pruebas con store temporal.

FUTURO  
WS12 debe fijar W01, commits previos, normalización/expansión y huecos; WS22 aporta representación Board; WS26.1 prepara candidato; WS48 admite escritura; P01 emite acta por delta y G_HUMAN_READ se resuelve con acta humana.
