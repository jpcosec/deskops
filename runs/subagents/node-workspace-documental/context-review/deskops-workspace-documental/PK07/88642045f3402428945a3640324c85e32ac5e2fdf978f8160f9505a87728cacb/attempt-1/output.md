## REFORMULACION
PK07 es un agregado no ejecutable del plan, con repo dueño `deskops`, que agrupa dos extensiones independientes: WS29 (Changes e impacto comprobable) y WS39 (inspección/edición de modelos existente). Su propósito es que ambas se planifiquen y validen como extras separados, sin convertirlas en prerrequisito del lector o manual básico. El resultado del paquete es que WS29 y WS39 cumplan su aceptación y que el manual etiquete cada extensión según evidencia, sin presumir CST/Kimun. Límites: el agregado no ejecuta, no crea tareas ni aristas, no autoriza mutaciones y no añade alcance; sus hijos implementan en `graph_ui`.

## AMBIGUEDADES
1. «Manual etiqueta cada extra según evidencia, no presume CST/Kimun.» No se nombra el manual, su repo/actor ni si esa etiqueta es condición de cierre o validación posterior. Obligaría a inventar qué artefacto manual acredita el paquete y quién lo actualiza.

## DRY-RUN
Al ser agregado, un ejecutor futuro no ejecutaría PK07: comprobaría sus hijos. WS29 y WS39 no tienen arista entre sí; no hay orden secuencial, solo convergencia en la validación del paquete. WS29 tomaría WS15 (errores/modo degradado) y WS24 (conocimiento, grafo y vecindad) y produciría la vista Changes con mutación real en store temporal, impacto entrante/saliente a 1 hop y errores enlazados a `sldb stores check`, `deskops doctor` o `deskops drift check`; no reparación automática. WS39 tomaría WS12 (contrato de operaciones), WS13 (lector/contexto) y WS48 (admisión de escritura) y produciría el punto de entrada Schema/clase desde documento activo, inspección/mutación UF09 en store temporal y acta humana P08; no habilitaría promover sin API/autoridad. No hay transferencia de artefactos entre WS29 y WS39. La validación conjunta revisaría ambas aceptaciones, sus evidencias y el etiquetado del manual, sin ejecutar pruebas ahora.

## FUTURO
WS15, WS24, WS12, WS13 y WS48 deben producir sus salidas; una persona P08 firma el acta de WS39. La implementación y cualquier mutación quedan fuera de este nodo.
