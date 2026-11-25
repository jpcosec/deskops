REFORMULACION
WS28 es un nodo de implementación en graph_ui, no un agregado. Su encargo es integrar en la vista de revisión la verificación de cierre de Deskops: verificar con `deskops closeout verify` por el canal del contrato WS12, diagnosticar faltantes y ofrecer handoff explícito con evidencia, a `deskops closeout commit` por CLI en modo manual o al coordinador activo. Resultado: UF05 con cierre externo confirmado y estado refrescado desde deskops. Límites: no commit/close por HTTP, no terminal embebido genérico, mutaciones de UI sujetas a G_HUMAN_READ y recibos G_UI_WRITE/G_WRITE_CONTRACT por delta; no sustituye el canal WS12.

AMBIGUEDADES
1. «UF05 termina cuando `deskops show task` y el commit de closeout confirman el cierre externo». UF05 no se define en las fuentes suministradas ni se nombra un nodo que produzca user-flows. Obliga a inventar qué recorrido y estado final constituyen UF05.
2. «o al coordinador si está activo (P03)». No se fija cómo se determina «activo» ni si coincide con la admisión denegada de WS48. P03 solo dice «con otro coordinador escribiendo»; obliga a inventar la señal operativa y el destinatario exacto del handoff.

DRY-RUN
Un ejecutor futuro leería el contrato WS12 (canal, errores, operaciones), las salidas de WS27.1/WS27.2, el módulo de admisión de WS48, la evidencia G_CLOSEOUT y, si existe, UF05. Cambios previstos: vista `frontends/mindmap/views/workspace/review/`, endpoints de verificación/handoff y tests en graph_ui. Dependencias: WS27 (agregado; termina cuando terminan sus hijos), WS12 y WS48. Validaciones futuras: pruebas con store temporal, recorrido manual WS30, acta G_HUMAN_READ de WS16 y recibos per-delta G_UI_WRITE/G_WRITE_CONTRACT. No se ejecuta nada.

FUTURO
WS12 publica el contrato de operaciones; WS48, la admisión de escritura; WS16 produce el acta de lectura; P01 emite el recibo por delta; WS30 valida UF05.
