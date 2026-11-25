## REFORMULACION

Propósito: entregar en `graph_ui` la vista de inbox que lee mensajes del desk, registra ack y, solo si el contrato WS12 define esa operación, responde localmente; sin envío interdesk y sin confundir ack con aprobación. Resultado: UI en `frontends/mindmap/views/workspace/inbox/` sobre endpoints autorizados por WS12, más tests. Repo dueño: `graph_ui`. Límites: no crea tarea implícita ni cron de triage; toda mutación UI pasa por la admisión de WS48 y los permisos de WS12, y su habilitación real espera `G_HUMAN_READ`; el desarrollo y las pruebas aisladas de API pueden avanzar con sus gates técnicos.

## AMBIGUEDADES

Ninguna. La respuesta local queda explícitamente delegada al contrato WS12 con conducta alternativa («si no se declara no disponible»), y el ack usa operaciones de ese mismo contrato; no hay resultado indefinido ni aceptación no comprobable que obligue al ejecutor a inventar.

## DRY-RUN

Hipotético, sin ejecutar. Lecturas: nodo WS25.1 y gates; contrato WS12 (whitelist de operaciones, permisos, revisión, errores); módulo de admisión WS48; vistas y endpoints existentes de inbox; store temporal de prueba. Cambios previstos: componentes de lectura de inbox, acción de ack, acción de respuesta condicionada al contrato, estados de no disponible/error y tests. Dependencias: WS12 y WS48 deben estar cerrados antes de invocar sus canales; WS48 se consulta antes de cada escritura. Validaciones futuras: ack visible tras recarga con el mensaje origen; respuesta solo si el contrato la define, si no «no disponible»; sin tarea ni cron; permisos aplicados; pruebas con store temporal y, para validación humana, corpus WS40.

## FUTURO

WS12 entrega el contrato y `G_WRITE_CONTRACT` por delta; WS48 entrega el punto único de admisión; WS16 produce el acta `G_HUMAN_READ`; el receptor P01 en `graph_ui` emite el acta `G_UI_WRITE` del delta. WS25.2 (captura drawer/protoátomo) es hermano sin arista: no se entregan nada entre sí; WS25 cierra como agregado cuando ambos cumplen. Humanos aceptan el delta y el recorrido de lectura.
