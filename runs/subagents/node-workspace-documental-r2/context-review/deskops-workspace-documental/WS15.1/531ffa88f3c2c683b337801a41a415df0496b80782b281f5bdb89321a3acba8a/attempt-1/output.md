REFORMULACION
El encargo de WS15.1 es un nodo de implementación en graph_ui: mostrar en el panel afectado los errores de lectura —referencia rota, documento ausente, modelo no importable y backend caído— sin borrar historial ni fingir vacío; tratar la falta de permiso o capacidad de edición como límite read-only visible, no como fallo de lectura; y declarar el fallo CDN como límite actual sin prometer offline. El resultado esperado es reutilizar el lector Markdown de WS13.1, tipificar en shell/api.js errores HTTP/red/JSON conservando error.body y compatibilidad con consumidores, y cubrir con pruebas la distinción entre error de API y red sin respuesta, el reintento con recuperación de pestañas/foco/historia y la no carga por CDN. Repo dueño: graph_ui. Límites: no implementar otro lector ni guardado; rutas de lectura según contrato WS11; empaquetado offline fuera. G_UI_READ queda pendiente por delta.

AMBIGUEDADES
Ninguna.

DRY-RUN
Lecturas: contrato WS11 de errores/red, implementación de WS13.1 y WS13.3, shell/api.js actual y tests existentes. Cambios previstos: componentes en views/workspace/errors/; ajuste de api.js para conservar estado HTTP y error.body y tipificar HTTP/red/JSON; pruebas de referencia rota, documento ausente, modelo no importable, backend caído, permiso read-only, CDN sin carga y reintento. Dependencias: WS13 cumplido —incluye WS13.1/13.3—, contrato WS11 y G_UI_READ como recibo de aceptación del delta concreto. Validaciones futuras: ejecutar tests; comprobar que no se borra historial ni se simula vacío; verificar recuperación tras restaurar backend y que CDN solo diagnostica; no añadir guardado ni offline. No ejecuto nada.

FUTURO
WS11 debe entregar el contrato de errores; WS13/WS13.1 el lector y foco/historia; TaskDoc fijará archivos, textos y escenarios; el receptor humano de G_UI_READ aceptará el delta concreto. WS15 cerrará cuando también cumpla WS15.2.
