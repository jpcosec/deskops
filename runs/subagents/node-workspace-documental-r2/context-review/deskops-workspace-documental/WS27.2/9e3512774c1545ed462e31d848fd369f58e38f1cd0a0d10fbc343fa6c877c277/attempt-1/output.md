REFORMULACION
WS27.2 es un encargo de implementación en graph_ui: añadir, junto a la TaskDoc, una vista de evidencia que muestre declarada, encontrada y verificada, y permita abrir su soporte. Resultado: vista en `frontends/mindmap/views/workspace/evidence/` con rutas de lectura del contrato WS11 y tests. Límites: no crear modelo de comentarios; no inferir tipos por extensión en renderer; verificación = resultado del gate/tipo y de `deskops closeout verify`, no prueba independiente; reporte ausente o fallo se muestra como no verificable con error; fuera de Markdown dentro del workspace solo se muestra ruta y no soportado. Depende de WS13, WS12 y G_UI_READ por delta.

AMBIGUEDADES
1. «declarada/encontrada/gates/summary se muestran según reporte real». La aceptación solo define declarada, encontrada, verificada y abrir soporte; no define qué son «gates/summary», de qué reporte salen, cómo se muestran ni cómo se aceptan. Obligaría al ejecutor a inventar su fuente, presentación y prueba, o a decidir que sobran en el scope.

DRY-RUN
Leería el contrato WS12 (correspondencia tipo→evidencia, artefactos soporte y salida pública de closeout verify) y las rutas de lectura WS11; revisaría el lector integrado WS13 y el registro de vistas. Localizaría los campos de TaskDoc citados (`closeout_evidence`, `references/files`) y la salida de `deskops closeout verify`. Implementaría la vista y tests en el output_scope. Dependencias: WS13 aporta lector/foco/historia; WS12, el contrato; G_UI_READ, recibo por delta. Validaciones futuras: estados distintos, evidencia ausente, apertura de Markdown dentro del workspace, ruta declarada fuera/no soportada y error por reporte ausente o comando fallido. Sin ejecutar nada.

FUTURO
WS12 produce el mapeo y la salida pública de closeout verify; WS13 entrega el lector integrado; el receptor humano P01 emite el acta G_UI_READ del delta concreto; la promoción fija archivos, pruebas y textos de pantalla en el TaskDoc.
