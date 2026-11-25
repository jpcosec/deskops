## REFORMULACION
WS15 es un **agregado no ejecutable** de `graph_ui`. Propósito: cubrir los errores de lectura y el modo degradado, junto con la orientación cuando un proyecto no tiene desk. Resultado: las salidas de WS15.1 y WS15.2; no produce artefacto propio. Límites: no implementa otro lector ni guardado, no promete offline, no inicializa desks por GET ni muta el proyecto, y conserva pestañas/foco/historia. Depende de WS13 y de sus hijos; requiere G_UI_READ, con recibos por delta.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro no ejecutaría WS15 como tarea: comprobaría que WS15.1 y WS15.2 cumplen su aceptación. Lecturas: `dag.yaml`, esta guía, contratos/resultados de WS13, WS11 y salidas/pruebas de ambos hijos. Cambios previstos: ninguno propio del agregado; solo integración y verificación. Dependencias: WS13 como base común; G_UI_READ por delta concreto, aún pendiente de forma intencional.

WS15.1 aporta panel de errores, distinción backend/CDN, recuperación tras restaurar backend y tipificación HTTP/red/JSON en `api.js`. WS15.2 aporta orientación sin desk, ruta absoluta, comando `deskops init <ruta>` y refresco tras init externo. Entre hermanos no hay arista ni transferencia secuencial: ambos consumen WS13 y se integran en el workspace. La validación conjunta exige ambas aceptaciones; no añade una prueba extra del agregado. Hacia WS16/WS29 se transfiere el conjunto integrado de errores/degradación y orientación.

## FUTURO
WS11 define los errores de API y estados de red, incluido CDN. El receptor humano P01 emite los recibos G_UI_READ por delta. WS16 realiza la validación humana de lectura, descubrimiento y UF10; WS29 consume WS15 para Changes. WS40 aporta corpus/manifiesto donde corresponda.
