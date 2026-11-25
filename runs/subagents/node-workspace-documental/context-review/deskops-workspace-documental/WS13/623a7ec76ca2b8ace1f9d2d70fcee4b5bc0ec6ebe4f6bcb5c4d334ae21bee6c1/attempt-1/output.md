REFORMULACION
El encargo de WS13 es integrar en graph_ui un lector de workspace con historia y foco sobre la base a1b2b22. Resultado: documento/fuente solo lectura, panel de contexto, enlaces, selección por documento/nodo, explorador de documentos modelados y no modelados, dos documentos lado a lado y pestañas/historia. Repo dueño: graph_ui. Límites: mantener Code local y rutas del host, no exigir índices nuevos, reutilizar shell/registry.js y no crear otro workspace. Es un agregado no ejecutable: no produce cambios propios y cierra cuando WS13.1, WS13.2 y WS13.3 cumplen su aceptación; G_UI_READ es por delta.

AMBIGUEDADES
ninguna.

DRY-RUN
Un ejecutor futuro del agregado no escribiría código: leería WS13, los contratos de WS13.1–WS13.3, WS11 y los recibos G_UI_READ. Orden real: WS11 habilita a WS13.1; WS13.1 habilita a WS13.2 y WS13.3. WS13.2 y WS13.3 son hermanos sin arista: no se transfieren entregables, pero deben integrarse sobre el mismo lector. WS13.1 aporta lectura de documento/fuente, contexto, enlaces y foco compartido por representaciones. WS13.2 aporta el explorador que abre documentos modelados y no modelados sin ID ni índices nuevos. WS13.3 aporta pestañas, divisiones, documento activo, historia y disposición local, conservando el foco por documento. Validación conjunta: aceptación de los tres hijos y recibo del delta concreto de cada uno; el agregado no añade una prueba distinta. Sin cambios previstos en archivos por WS13.

FUTURO
WS11 entrega contrato de navegación y mapa de recepción; P01/receptor de graph_ui emite actas G_UI_READ por delta; la promoción fija TaskDoc, archivos y pruebas; WS14 y siguientes consumen WS13 ya cerrado.
