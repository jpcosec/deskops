REFORMULACION
WS36 es un nodo de implementación en `graph_ui`. Su propósito es integrar la delegación e intervención humanas en la vista de ejecución, invocando solo el adaptador público WS34 para dispatch/reply y registrando decisiones con WS33.2. El resultado esperado es una UI y pruebas que vinculen la respuesta al intento, confirmen la operación, muestren actor humano y evidencia enlazada de WS33.1/WS33.2, y presenten como error la ausencia de API o permisos. Límites: no autoaprobar ni simular; no implementar el adaptador; la ruta fina hacia WS34 queda sujeta al contrato WS12; alcance en `frontends/mindmap/views/workspace/execution/` y `tests/`. Depende de WS34, WS35 y los gates G_EXEC, G_SCION, G_UI_WRITE y G_WRITE_CONTRACT.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: nodo y aristas de `dag.yaml`; contrato WS12; API/confirmación de WS34; modelo de decisiones/evidencia WS33.1/WS33.2; vista WS35; recibos de gates. Cambios previstos: capa fina de invocación en `execution/` que solo llame a WS34; registro de decisión vía WS33.2; presentación de actor/evidencia y errores; tests. Dependencias: WS34 disponible, WS35 visible, WS33.1/WS33.2 con evidencia, contrato WS12 y gates. Validaciones futuras: tests de respuesta ligada al intento y operación confirmada; revisión con actor humano y evidencia enlazada; error visible por falta de API/permiso; ausencia de autoaprobación o simulación. Sin ejecutar.

FUTURO
WS34 entrega el adaptador; WS35 la trazabilidad; WS33.1/WS33.2 la evidencia y decisiones; WS12 fija el contrato; WS37 valida con agente real. Humanos, WS44 y los gates resuelven G_EXEC, G_SCION, G_UI_WRITE y G_WRITE_CONTRACT.
