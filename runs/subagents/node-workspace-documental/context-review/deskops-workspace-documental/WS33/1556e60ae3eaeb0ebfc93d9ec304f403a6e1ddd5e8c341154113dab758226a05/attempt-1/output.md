REFORMULACION
Propósito: agrupar la vinculación documental de mensajes y resultados con su intento —con deduplicación y procedencia— y el registro de una decisión humana explícita asociada al intento y su tarea. Resultado: agregado no ejecutable; se cumple cuando WS33.1 y WS33.2 cumplen su aceptación, y sus dependientes siguen esperando WS33. Repo dueño: deskops. Límites: backend documental independiente del editor UI; no escribe estados de testing/closeout ni toca tablas Scion; exige G_SCION y G_WRITE_CONTRACT.

AMBIGUEDADES
1. «depends_on: - WS32 - WS11 - WS33.1 - WS33.2». WS33 es agregado no ejecutable y ningún hijo declara consumir WS11; el input no dice qué artefacto de navegación/identidad transfiere WS11 ni si su cierre condiciona el agregado. Obligaría a inventar si WS11 es precondición real o arista sobrante.
2. «requires: - G_SCION - G_WRITE_CONTRACT» frente a «Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación». G_WRITE_CONTRACT es per_delta y lista WS33 en scope_nodes, pero no se define efecto/contrato propio de WS33 ni si basta el recibo de WS33.1/WS33.2. Obligaría a inventar qué recibo verificar para WS33.

DRY-RUN
No se ejecuta WS33. Un ejecutor futuro leería dag.yaml, gates y contratos WS32/WS12; ejecutaría WS33.1 y WS33.2. Orden por aristas: WS32 -> WS33.1 -> WS33.2 (WS33.2 depende de WS33.1). WS33.1 transfiere mensajes/resultados vinculados a intento, claves de dedup Hub+proyecto+conversación+mensaje y Hub+proyecto+intento+fuente, y huecos de procedencia. WS33.2 consume ese vínculo para registrar la decisión con actor humano, intento y tarea, mediante la operación de WS12. Validación conjunta: importación repetida sin duplicados ni atribución de conversación completa; decisión con resultado explícito y texto de corrección; completed nunca como aprobado; recibos por delta. Si falta contrato/API, detenerse y registrar hueco.

FUTURO
WS44/operador designado resuelve G_SCION; WS12 produce G_WRITE_CONTRACT por delta; el solicitante P01 acepta deltas; WS34/WS35 consumen las salidas de WS33.
