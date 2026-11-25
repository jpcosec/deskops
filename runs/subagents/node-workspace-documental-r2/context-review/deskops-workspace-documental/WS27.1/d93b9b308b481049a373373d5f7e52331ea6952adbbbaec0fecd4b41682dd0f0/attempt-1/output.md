## REFORMULACION
Encargo de planificación de WS27.1: implementar en `graph_ui` una vista de diff Git e historial **read-only** junto a la TaskDoc. Resultado: mostrar diff real e historial acotados a la tarea y repo, usando commits resolubles de `TaskDoc.references` y rutas de `TaskDoc.files`; sin commits, diff working tree→HEAD limitado a esas rutas. Debe haber una sección por repo alcanzado, con root explícito resuelto mediante WS11. Límites: no escribir, revertir ni adivinar rutas; ruta sin repo resoluble queda no disponible; no mostrar hallazgos de integridad del store (WS29); la asociación a intento llega en WS35. Salida prevista en `frontends/mindmap/views/workspace/diff/`, rutas de lectura de WS11 y `tests/`.

## AMBIGUEDADES
ninguna

## DRY-RUN
Lecturas hipotéticas: definición del nodo, contrato WS11, contrato WS12, modelo TaskDoc de deskops, registro/alias existente y tests de graph_ui. Cambios previstos: crear la vista de diff/historial y sus pruebas dentro del `output_scope`; no ejecutar Git mutante. Dependencias: WS13 aporta el lector integrado; WS12, el contrato de operaciones; WS11, resolución de repo/rutas; `G_UI_READ` se recibe por delta. Validaciones futuras: TaskDoc con y sin commits; diff real; working tree→HEAD cuando falten commits; commits ordenados y limitados a `TaskDoc.files`; varias secciones si hay varios repos; ruta irresoluble marcada no disponible; ausencia de escritura/revert; ausencia de hallazgos de integridad. La promoción fijará archivos, textos y casos detallados.

## FUTURO
WS11 produce el contrato de navegación/rutas; WS12, el contrato de operaciones; WS13, el lector integrado. WS35 añadirá la asociación a intento; WS29, integridad del store. El receptor humano P01 decide la recepción `G_UI_READ` del delta concreto. El TaskDoc de promoción fija archivos, pruebas y textos. WS27 cierra cuando cumplen WS27.1 y WS27.2.
