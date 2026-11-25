## REFORMULACION

PK08 es un agregado de planificación del ramal Scion opcional. Propósito: agrupar la delegación Scion posterior con intentos, trazas e intervención verificables, sin ejecución propia. Resultado: paquete cuyos hijos producen identidad/manifiesto/cierre, mensajes/decisiones, dispatch/reply autorizados, trazabilidad, UI, validación humana y capítulo de manual. Repo dueño: deskops; WS35–WS37 pertenecen a graph_ui. Límites: no duplicar pipeline Scion; ningún permiso de núcleo habilita dispatch; sin G_SCION el ramal queda bloqueado; la agrupación no autoriza tareas ni añade aristas.

## AMBIGUEDADES

1. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada». No define qué artefacto o comprobación constituye esa «integración indicada»; obligaría a inventar si basta el acta de WS37 o se exige otro registro conjunto.
2. «Sin acceso real ramal bloqueado». No dice quién declara el bloqueo ni si afecta a todos los hijos o solo a los que dependen de G_SCION; obligaría a inventar el alcance operativo del bloqueo.

## DRY-RUN

Hipotético, sin ejecutar. WS44 parte de WS05 y WS07: inventario y autorización read-only; produce `auditoria/scion-probe.md` y satisface G_SCION. WS32 (WS32.1→WS32.2), tras WS05/WS12 y G_SCION, produce identidad de intento, registro y manifiesto/RunDoc/cierre idempotentes; los entrega a WS33. WS33.1 vincula mensajes/resultados con dedup; WS33.2 registra decisión humana; ambos alimentan WS34 y WS35. WS34.1→WS34.2, con G_EXEC, producen adaptador dispatch/reply y clasificación de timeout; lo entregan a WS36. WS35, tras WS33/WS27, produce vista de ejecución y evidencia; WS36 integra intervención humana sobre WS34/WS35. WS37 recibe WS36 y WS30, ejecuta el recorrido real y emite acta. WS38 recibe WS37 y WS31, publica capítulo y átomos vinculados.

Validación conjunta: acta WS37, capítulo WS38 y recibos G_SCION/G_EXEC; comprobar correlación intento→dispatch/reply, dedup, idempotencia, completed≠aprobado y ausencia de dispatch sin G_EXEC.

## FUTURO

El solicitante/designee designa operador y acceso Scion; el mismo actor autoriza G_EXEC. WS37 produce aceptación humana y WS31 habilita el manual básico que WS38 enlaza.
