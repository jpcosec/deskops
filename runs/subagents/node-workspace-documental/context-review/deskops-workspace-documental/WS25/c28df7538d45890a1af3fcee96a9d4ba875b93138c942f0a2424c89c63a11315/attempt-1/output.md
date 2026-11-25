REFORMULACION
Propósito: WS25 es un agregado de implementación en `graph_ui` que integra en la UI lectura de inbox con ack/respuesta local y captura en drawer o protoátomo, usando solo operaciones autorizadas por el contrato WS12; ack no es aprobación. Resultado: salidas de WS25.1 y WS25.2, no una ejecución propia. Repo dueño: `graph_ui`. Límites: no se ejecuta; termina cuando ambos hijos cumplen su aceptación; no hay envío interdesk, tarea implícita ni cron de triage; no se inventan API, modelo o canal; G_HUMAN_READ habilita uso de mutaciones en UI, sin bloquear desarrollo/pruebas aisladas de API con contratos/gates técnicos.

AMBIGUEDADES
Ninguna. El resultado y la aceptación remiten a hijos concretos; WS12, WS46 y WS48 tienen productor/dueño; los gates pendientes son intencionales y `per_delta`.

DRY-RUN
Sin ejecutar. Un ejecutor futuro no ejecutaría WS25: leería `dag.yaml`, el contrato WS12, evidencia de WS46/WS48 y recibos de gates. Verificaría que WS25.1 —tras WS12 y WS48— entrega vista de inbox, ack persistente y respuesta solo si WS12 la define; y que WS25.2 —tras WS12, WS46 y WS48— entrega captura con destino explícito, origen tipado ruta/mensaje, colisión controlada y persistencia tras recarga. Los hermanos no se transfieren nada entre sí: comparten contrato y host; la integración conjunta se valida porque ambas superficies usan las mismas operaciones autorizadas, no confunden ack con aprobación y no crean tarea implícita. Cambios previstos: solo en rutas de hijos dentro de `graph_ui`; el agregado no cambia código. Validaciones futuras: aceptación de cada hijo, persistencia tras recarga, UF02, permisos del contrato, no sobrescritura silenciosa, ausencia de tarea/cron y recibos aplicables de G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

FUTURO
WS12 produce contrato/whitelist y resuelve adapter/huecos; WS46 prueba la capacidad de captura con origen; WS48 aporta su dependencia; WS16 produce G_HUMAN_READ; el receptor P01 emite actas `per_delta` de G_UI_WRITE/G_WRITE_CONTRACT; WS30 valida manualmente. Nada de eso lo decide este nodo.
