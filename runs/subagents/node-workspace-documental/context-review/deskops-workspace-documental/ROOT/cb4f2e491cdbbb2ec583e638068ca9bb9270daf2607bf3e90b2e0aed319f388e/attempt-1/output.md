## REFORMULACION
ROOT es un agregado de planificación, no un nodo ejecutable: ordena el paquete «Workspace documental de Deskops» sobre Mindmap/SLDB/Deskops. Su propósito es cubrir lector temprano, autoría/operación manual, manual publicado, extensiones independientes y ramal Scion opcional. El resultado esperado es un paquete planificado e integrado por sus hijos, con identidad/origen compartidos, APIs públicas, guardas/canales, manual trazado a versión y sin dependencias opcionales sobre el núcleo. Repo dueño: `deskops`. Límites: no implementa UI, no autoriza tareas ni añade aristas, no acepta producto/API/actas, y no convierte extras o Scion en prerrequisitos del núcleo.

## AMBIGUEDADES
ninguna

## DRY-RUN
Hipotético, sin ejecutar:
1. **PK01** consume brief/alcance/decisiones y produce auditorías WS02–WS04, inventario WS05 y matriz WS06; entrega base factual y deltas verificables.
2. **PK02** consume WS06 y decisiones registradas; produce WS07–WS12: UFs, convención manual, catálogo de vistas, identidad/navegación y whitelist por delta.
3. **PK03** consume WS11/WS08; produce lector WS13–WS15, Taller WS40 y lectura multidesk WS41; WS16 integra acta humana.
4. **PK04** consume WS11/WS40/WS13/WS09; produce índices WS17, Board WS22, procedimientos WS23 y conocimiento WS24; WS18 queda opcional.
5. **PK05** consume WS12/WS17/WS22/WS24; produce campos WS19, API fuente WS20, precondición WS45, fuente/render WS21, intake WS25, tareas WS26, evidencia WS27, handoff WS28 y conocimiento WS42; WS30 integra pruebas humanas.
6. **PK06** consume acta WS30 y entradas WS17; produce publicación WS43 y manual WS31.
7. **PK07**, independiente, consume WS15/24 para WS29 y WS12 para WS39; no bloquea lector/manual.
8. **PK08**, ramal independiente, consume WS05; WS44 aporta G_SCION; WS32–WS36 producen intentos, mensajes, dispatch autorizado, trazas y UI; WS37 valida y WS38 publica.

Validación conjunta: actas humanas WS16/WS30, publicación WS43/31, pruebas propias de WS29/39 y acta WS37/WS38 para Scion; comprobar trazabilidad, canales y ausencia de dependencias opcionales sobre el núcleo.

## FUTURO
Humano/product owner decide actas WS16/WS30/WS37 y aceptación de producto. WS12/WS20/WS45/WS44 producen contratos, G_SOURCE, G_PAYLOAD_PRECONDITION y G_SCION; WS43 publica entradas reales.
