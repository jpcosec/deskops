## REFORMULACION
**Propósito:** WS32 es un agregado de planificación no ejecutable que unifica la identidad de intento y el cierre Scion, refinando el candidato de drawer de `external_references.scion` sin abrir un segundo pipeline. **Resultado:** que sus hijos validen identidad/registro/idempotencia locales y dejen consistentes intento, dispatch intent/confirmed, manifiesto, RunDoc y cierre. **Repo dueño:** deskops. **Límites:** solo operaciones locales sobre store temporal; sin dispatch/reply de red, sin eventos Hub fingidos ni tablas internas; los estados Hub reales quedan para WS34/37 bajo G_EXEC. No es ticket del Board. Depende de WS05, WS12 y de sus hijos WS32.1/WS32.2; requiere G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.

## AMBIGUEDADES
Ninguna. El nodo es agregado y su aceptación remite a la de sus hijos; las ubicaciones exactas, campos y pruebas quedan delegadas a la promoción/TaskDoc, y los gates pendientes son intencionales.

## DRY-RUN
Agregado no ejecutable: se recorre por hijos siguiendo aristas reales.
1. **WS05 y WS12** son prerrequisitos comunes de ambos hijos: WS05 inventaría identidad/API Scion; WS12 fija el contrato/ubicación del registro por intento y la precondición de escritura. No se ejecutan aquí.
2. **WS32.1** materializa, según ese contrato, la separación intento/slug y los hechos `intent` y `confirmed`; entrega a WS32.2 un id de intento estable y el registro local intent/no confirmado, sin afirmar resultado Hub. Toca `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y tests.
3. **WS32.2** consume ese id y hace idempotentes manifiesto, RunDoc y closeout sobre el mismo intento, con hash de sesión y evidencia concordantes; si falta artefacto/contrato de hash, registra hueco con productor WS12/WS05.
4. **Validación conjunta:** ambas aceptaciones hijas deben cumplirse; WS32 termina cuando terminan sus hijos y sus dependientes siguen apuntando al ID WS32. Gates: G_CLOSEOUT satisfecho; G_SCION no verificado y G_WRITE_CONTRACT per_delta pendiente, sin que ello autorice inventar API, hash o respuesta Hub.

## FUTURO
WS44 produce el probe real de G_SCION; WS34/37 demuestran dispatch/confirmación Hub y correlación bajo G_EXEC; WS12 emite su contrato/recibo por delta; un humano registra la recepción del delta. WS33 y siguientes consumen WS32. Ninguna aprobación de implementación se infiere.
