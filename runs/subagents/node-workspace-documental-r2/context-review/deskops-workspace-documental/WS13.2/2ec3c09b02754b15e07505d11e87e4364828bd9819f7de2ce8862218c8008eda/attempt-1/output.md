REFORMULACION

WS13.2 es un nodo `implementation` de `graph_ui`, no un agregado. Su encargo es construir un explorador que muestre documentos reales del store y Markdown no modelado del desk, obteniendo el árbol mediante la API del store y el sistema de archivos, conforme al contrato WS11. Debe permitir abrir ambos tipos de documento sin conocer su ID ni usar índices nuevos; las altas deben aparecer tras refresco explícito del catálogo, sin reiniciar servidor ni cambiar código. Límites: trabaja en `frontends/mindmap/views/workspace/explorer/`, usa rutas de lectura de WS11, puede reutilizar catálogo/filtro existente para modelados y deja a WS11 la API/seguridad de no modelados. Incluye `tests/` y requiere `G_UI_READ` por delta.

AMBIGUEDADES

Ninguna.

DRY-RUN

Lecturas: contrato WS11, recibo `G_UI_READ` del delta concreto, aceptación de WS13.1, catálogo/filtro existente y estructura actual del explorador.

Cambios previstos: implementar el árbol de modelados desde la API del store y el de no modelados desde el desk; conectar apertura/selección con el lector existente; añadir refresco explícito del catálogo; pruebas en `tests/`.

Dependencias: WS11 para navegación, API y seguridad; WS13.1 como prerrequisito; `G_UI_READ` pendiente, evaluado por delta.

Validaciones futuras: usar un store temporal real; añadir un documento modelado y un Markdown no modelado; refrescar el catálogo; comprobar que aparecen y se abren sin conocer ID, sin reiniciar servidor ni modificar código; verificar que no se introducen índices nuevos; registrar evidencia y recibo del delta.

FUTURO

WS11 produce el contrato de navegación y la API/seguridad para no modelados. El receptor P01 emite el recibo `G_UI_READ` del delta. WS13 cierra como agregado cuando cumplen sus hijos. La promoción fijará archivos, escenarios de prueba y textos de pantalla en el TaskDoc.
