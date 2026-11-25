REFORMULACION
WS33.1 es un encargo de implementación en deskops: construir backend documental que vincule mensajes y resultados de Scion a intentos existentes, con referencias Hub/proyecto/conversación/mensaje/intento, deduplicación y procedencia. Resultado: importación repetida idempotente; mensajes sin intento resoluble o con varios quedan sin vínculo y como hueco de procedencia; resultados deduplicados por Hub+proyecto+intento+id de fuente. Límites: depende de WS32 y de G_SCION/G_WRITE_CONTRACT; no toca tablas Scion ni editor UI; si falta contrato/dato/permiso, se detiene y registra hueco. Repo dueño: deskops.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: salidas de WS32 sobre identidad/idempotencia de intento; contrato público de WS12/G_WRITE_CONTRACT; inventario/probe WS05/WS44 y G_SCION; fuente de mensajes/resultados vía contrato público, nunca tablas Scion. Cambios previstos: adaptador en runtime/ según contrato, modelos/reportes de referencias, deduplicación, procedencia y huecos; tests/. Dependencias: WS32 y sus hijos; gates pendientes. Validaciones futuras: importar dos veces el mismo Hub/proyecto/conversación y comprobar cero duplicados de mensajes/resultados; no atribuir conversación completa a un intento; mensajes con varios intentos o sin intento resoluble sin vínculo y con hueco; resultados con id de fuente conservando procedencia; verificar que no se escriben tablas Scion. Sin ejecutar nada.

FUTURO
WS32 fija identidad de intento, registro e idempotencia. WS12 define operación/campos/actor/errores del contrato; WS05/WS44 producen inventario/probe y el operador designado resuelve G_SCION. La promoción fija archivos, TaskDoc y pruebas. El recibo per_delta de G_WRITE_CONTRACT y las actas humanas corresponden a recepción; WS33.2 registrará decisión humana y WS34/37 probarán Hub real bajo G_EXEC.
