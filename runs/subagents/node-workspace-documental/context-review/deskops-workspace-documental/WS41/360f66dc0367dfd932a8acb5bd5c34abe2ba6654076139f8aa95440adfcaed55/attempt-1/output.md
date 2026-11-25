REFORMULACION
WS41 es un nodo de implementación, no un agregado, en `graph_ui`. Propósito: habilitar lectura segura entre desks resolviendo aliases/roots explícitamente autorizados por el contrato WS11 y usando APIs públicas de stores. Resultado: cada request conserva su proyecto/store sin cambiar `SLDB_STORE` global; se puede leer el segundo desk del corpus WS40, seguir enlaces authored entre desks y volver por la historia, sin mutaciones cruzadas. Repo dueño: `graph_ui`; salidas en `frontends/mindmap/source/`, `views/workspace/` y `tests/`. Límites: solo aliases/roots autorizados; rechazar roots arbitrarios, paths escapados y store ausente con error visible; no copiar contenido para afirmar federación; no mutar entre desks. Aceptación: UF08 sobre dos stores WS40, con identidad/origen visibles.

AMBIGUEDADES
Ninguna.

DRY-RUN
Un ejecutor futuro leería el contrato WS11 (resolución repo/store, aliases/roots, identidad/origen, enlaces/historia), el manifiesto y corpus WS40 (dos desks, enlaces authored y store del segundo desk), la integración WS13 (historia/foco) y el código/APIs públicas de `graph_ui`/stores. Cambios previstos: capa de resolución por request que fije store/proyecto sin tocar el global; rutas de lectura y errores visibles para alias no autorizado, path escapado y store ausente; conexión de vistas de workspace y pruebas. Dependencias: WS11, WS13, WS40 y recibo G_UI_READ del delta WS41. Validaciones futuras: pruebas con stores temporales/WS40 para abrir el segundo desk, seguir enlaces entre desks, volver por historia y rechazar accesos; UF08 manual posterior vía WS16. Sin ejecutar nada.

FUTURO
WS11 produce el contrato de navegación, autorización de aliases/roots y APIs citadas. WS13 entrega el lector integrado con historia/foco. WS40 produce el corpus, manifiesto y segundo desk. P01/receptor emite el acta G_UI_READ del delta concreto; el estado global pendiente no exige aceptación conjunta. WS16 realiza la validación humana de UF08. La aceptación de recepción y producto corresponde al humano designado.
