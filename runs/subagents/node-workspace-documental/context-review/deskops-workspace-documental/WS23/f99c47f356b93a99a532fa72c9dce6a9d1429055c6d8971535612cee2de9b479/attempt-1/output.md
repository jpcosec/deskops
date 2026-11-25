REFORMULACION  
WS23 es un encargo de implementación en `graph_ui` para renderizar RitualDoc/StepDoc/lifecycle como procedimiento sobre referencias reales. Propósito: que un procedimiento abra sus documentos y soporte, con pasos y fuentes navegables y transiciones solo representadas. Resultado: renderer en `frontends/mindmap/views/workspace/procedure/` y pruebas. Límites: no auto-marcar pasos por leerlos; mostrar progreso/estado solo si WS02/WS09/WS11 identifican campo/API real de deskops, si no los pasos authored son inertes; la vista no escribe estado; las transiciones muestran origen/destino/condición declarados sin controles de avance ni mutaciones; prueba de no peticiones de escritura. Depende de WS13 y WS09 y requiere G_UI_READ; pruebas con corpus WS40 o store temporal real.

AMBIGUEDADES  
Ninguna. El input define resultado, aceptación, repo, límites y dependencias; los detalles de archivos, textos y casos quedan al TaskDoc de promoción, y la falta de contrato/dato se rige por las reglas comunes.

DRY-RUN  
Lecturas: `dag.yaml` de WS23, WS13 —agregado que termina con sus hijos— y WS09; brief, alcance y decisiones; contrato WS11/G_UI_READ; inventario de WS09; corpus WS40 o store temporal. Cambios previstos: implementar la vista de procedimiento en el `output_scope` y sus tests; no tocar estado. Dependencias: WS13 y WS09 cumplidos; recibo `per_delta` de G_UI_READ para WS23. Validaciones futuras: abrir documentos/soporte, pasos/fuentes navegables, no auto-marcado, progreso solo con campo/API real o pasos inertes, transiciones sin controles y sin peticiones de escritura.

FUTURO  
WS09 aporta el inventario de renderizaciones; WS11 el contrato de navegación; WS40 el corpus; el receptor designado P01 emite el acta de G_UI_READ por delta. WS30 podrá consumir WS23 en la validación manual. Nada de esto ejecuta ni autoriza escritura.
