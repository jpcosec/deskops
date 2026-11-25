REFORMULACION
WS32.1 es un delivery ejecutable —no agregado— de `deskops`: materializar la identidad de intento y el registro local intent/no confirmado de Scion, separando intento de slug y de estado Hub. Resultado: cambios y pruebas en `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/` que crean dos intentos con IDs distintos antes de dispatch y los persisten mediante operaciones reales del store temporal. Límites: sin segundo pipeline; sin inventar almacenamiento, que fija WS12; `models/run.py` con registro/validación SLDB; RunDoc trackeado por API/CLI SLDB, no Markdown ad hoc; sin dispatch/reply de red, evento Hub simulado ni afirmación de fallo/éxito Hub.

AMBIGUEDADES
Ninguna. El contrato/ubicación del registro queda en WS12 y el inventario en WS05; WS32.2 y WS34/37 son futuros declarados, no huecos de este encargo.

DRY-RUN
Lecturas: contrato WS12, inventario WS05, candidato drawer `external_references.scion`, `models/run.py`, `runtime/scion.py`, `services/closure.py` y pruebas existentes. Cambios previstos: identidad/registro local y pruebas dentro del `output_scope`. Dependencias: WS05 y WS12; G_CLOSEOUT satisfecho; G_WRITE_CONTRACT per_delta; G_SCION unverified. Validaciones futuras: dos IDs distintos; registro intent/no confirmado en store temporal real; ninguna etiqueta Hub sin evidencia; modelo registrado/validado por SLDB; RunDoc por API/CLI. Si falta contrato de WS12, se registra hueco y no se sustituye.

FUTURO
WS12 produce contrato/ubicación del registro y su recibo G_WRITE_CONTRACT; WS05, inventario de identidad/API; WS32.2 convierte el registro en manifiesto canónico e idempotente; WS34/37 prueban dispatch real y correlación bajo G_EXEC; WS44/G_SCION verifica API pública. La autorización de ejecución/red es decisión humana externa (G_EXEC), no de este nodo.
