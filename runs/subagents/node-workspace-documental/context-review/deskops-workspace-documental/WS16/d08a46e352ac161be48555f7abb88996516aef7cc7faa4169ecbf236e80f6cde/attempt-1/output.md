## REFORMULACION
WS16 es un nodo de validación en `graph_ui`: un humano real recorre lectura/descubrimiento (UF01/UF03/UF07/UF08/UF10) sobre el manifiesto y corpus de WS40, sigue `validacion-humana.md` y registra acta en `runs/subagents/workspace-documental-acceptance/lectura/`. Resultado: evidencia para `G_HUMAN_READ`. No implementa correcciones, no crea corpus propio, no muta entre desks y no mide guardados hasta WS30. Límites: no sustituye aprobación humana; un fallo medido mantiene el gate pendiente; no se rebajan umbrales P08.

## AMBIGUEDADES
1. «sigue el protocolo de validacion-humana.md»: no se indica repo, ruta ni productor del protocolo. Obliga al ejecutor a inventar el procedimiento o localizarlo sin contrato.
2. «Humano real realiza recorrido»: no define si debe ser el responsable de producto/solicitante u otra persona. Obliga a inventar el criterio de elegibilidad del aprobador.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml`, el manifiesto de WS40, el protocolo, las salidas de WS14/WS15/WS41 y las UF de WS08. Cambios previstos: `acta.md` y registros de fallo/incidente si aplica; ningún código. Dependencias: humano disponible, corpus WS40, búsqueda WS14, errores/degradado WS15 y segundo desk WS41. Validaciones futuras: recorrido humano, tiempos de apertura/búsqueda/arranque, estados de error, lectura del segundo desk; si algo falla, registrar y dejar `G_HUMAN_READ` pendiente.

## FUTURO
El humano firma o rechaza el acta; el supervisor del repo receptor atribuye fallos; nodos de corrección los resuelven. WS30 medirá guardados y WS17 enriquecerá índices. `G_HUMAN_READ` habilitará uso de UI, no desarrollo/pruebas aisladas de API.
