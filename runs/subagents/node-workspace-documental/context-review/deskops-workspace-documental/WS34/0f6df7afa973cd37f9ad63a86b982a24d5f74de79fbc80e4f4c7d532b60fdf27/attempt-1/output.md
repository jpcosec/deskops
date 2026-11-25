## REFORMULACION
Encargo: exponer en `deskops` un adaptador público restringido para dispatch/reply de Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: salidas de WS34.1 y WS34.2; al ser `aggregate` no ejecutable, no produce artefacto propio. Repo dueño: `deskops`. Límites: depende de WS33 y WS12; requiere G_EXEC, G_SCION y G_WRITE_CONTRACT; no shell arbitrario ni duplicar transporte; no enviar mensajes en planificación; la política de timeout y la autoridad se toman del contrato WS12; si falta, se detiene y registra el hueco.

## AMBIGUEDADES
Ninguna. Las referencias a timeout, autoridad e identidad de intento tienen productor o consumidor nombrado —WS12, WS32.1/WS32.2— y los gates pendientes son intencionales. El carácter agregado no exige definir un resultado propio distinto de las salidas de sus hijos.

## DRY-RUN
Agregado no ejecutable. Lecturas: WS34, WS34.1, WS34.2, aristas WS33/WS12 y gates. Cambios previstos: ninguno en WS34; WS34.1 produciría el adaptador de dispatch y evidencia de aceptado/rechazado/vencido correlacionada al intento local; WS34.2, tras WS34.1, produciría el adaptador de reply vinculado al intento y reportaría timeout como fallo sin confirmación. Dependencias: WS33 y WS12 antes de ambos; WS34.1 antes de WS34.2. Validación conjunta futura: G_EXEC/G_SCION pasan; un agente real demuestra dispatch aceptado y rechazado/vencido y respuesta al intento correcto con timeout; sin shell ni transporte duplicado; si falta la política WS12, se detiene y registra el hueco; WS34 cierra cuando ambos hijos aceptan.

## FUTURO
WS36 consumirá solo el adaptador WS34 y registrará decisiones con WS33.2. WS12 debe producir la sección por delta de timeout/autoridad. WS44 o el operador designado verificará G_SCION; un humano resolverá G_EXEC. G_WRITE_CONTRACT se recibirá por delta, sin aceptación conjunta de otros nodos.
