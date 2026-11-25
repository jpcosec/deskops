REFORMULACION

WS32.2 es una implementación en `deskops`: hacer idempotentes manifiesto, RunDoc y cierre sobre el id de intento citado por el cierre, nunca por agente o slug. Resultado: registro canónico por intento que materializa RunDoc y registros de closeout, con campos mínimos declarados. Límites: solo persistencia local mediante operaciones reales de store temporal; sin dispatch/reply de red ni evento Hub no observado. Repo dueño: `deskops`; salidas: `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py`, `tests/`. No es agregado.

AMBIGUEDADES

1. «según el candidato de drawer de external_references.scion (campos mínimos: id de intento, identidad de agente, identidad de run si la API la expone, timestamps, hash de sesión, evidencia y commit de cierre)». Obligaría a inventar ruta/commit del candidato, campos adicionales y prevalencia del candidato sobre los mínimos. Si falta, el nodo no nombra productor ni regla de bloqueo; el bloqueo escrito solo cubre artefacto/contrato de hash.

DRY-RUN

Un ejecutor futuro leería WS05 (inventario de identidad/API), WS12 (contrato y campos de sesión/hash), WS32.1 (registro por intento), el candidato citado y el código/tests actuales. Cambiaría `runtime/scion.py`, `models/run.py`, `services/closure.py` y tests. Implementaría operaciones idempotentes sobre un store temporal real, usando el id de intento como clave, materializando manifiesto/RunDoc/closeout y comparando id de intento, hash de sesión y evidencia. No usaría red, dispatch/reply ni eventos Hub. Si faltara artefacto/contrato de hash, se detendría y registraría hueco con WS12/WS05. Validaría que una finalización repetida conserva identidad y evidencia sin crear registros nuevos, y que manifiesto, RunDoc y closeout coinciden. Dependencias: WS05, WS12, WS32.1; gates G_CLOSEOUT, G_SCION, G_WRITE_CONTRACT, sin evaluar aquí su satisfacción.

FUTURO

WS05 aportará el inventario de sesión/identidad; WS12 cerrará el contrato de operaciones, sesión/hash y `G_WRITE_CONTRACT`; WS44 y el operador designado producirán el probe y `G_SCION`; WS34/37 probarán Hub real y correlación bajo `G_EXEC`; un humano o designee autorizará `G_EXEC`. La recepción per-delta queda fuera de este nodo.
