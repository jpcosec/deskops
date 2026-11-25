## REFORMULACION
WS05 es un nodo de planificación (`delivery`) de `deskops` que debe producir `auditoria/scion.md`: inventariar la identidad y la API pública de Scion leyendo código/documentación en `deskops` y `../scion`; separar slug/agente/intento/dispatch/mensaje/conversación y permisos; señalar campos internos no públicos y capabilities que requieran API real, WS32 y WS33. Límites: no contacta endpoints vivos, no usa credenciales, no crea agentes, no envía mensajes ni modifica configuración; puede leer configuración sin secretos; no produce G_SCION. Depende solo de WS01.

## AMBIGUEDADES
1. «marca qué capabilities requieren WS32 y WS33»: el input no define WS33 ni enumera sus capabilities; el ejecutor tendría que inventar qué es WS33 y qué capacidades atribuirle.
2. «los campos internos que no figuren en la API pública definida en el scope»: el scope no enumera endpoints/SDK ni campos públicos; solo remite a «endpoints/SDK documentados o exportados». Si esos artefactos no fijan el límite, el ejecutor tendría que inventar el criterio de publicidad o la lista de campos públicos.

## DRY-RUN
Lecturas: WS01 (brief/glosario), `dag.yaml`, `auditoria/scion.md`; código `runtime/templates/RunDoc` en `deskops` y repo `../scion`, más docs/SDK exportados. Cambios previstos: crear/actualizar solo `auditoria/scion.md` con el inventario y las marcas exigidas. Dependencias: WS01; WS44 aportará el probe real; WS12/WS32 consumirán el inventario. Validaciones futuras: que no se usen tablas internas como interfaz, que la separación de identidades y permisos sea completa, que se marquen campos internos y capabilities, y que no haya endpoints vivos, credenciales, mutaciones ni G_SCION.

## FUTURO
WS44 ejecuta el probe read-only y produce la evidencia de G_SCION. WS12 fija el contrato/ubicación del registro por intento; WS32.1/WS32.2 materializan identidad e idempotencia. Si WS33 no aparece definido en el plan, un humano o el nodo dueño del DAG debe aportar su definición antes de promover WS05.
