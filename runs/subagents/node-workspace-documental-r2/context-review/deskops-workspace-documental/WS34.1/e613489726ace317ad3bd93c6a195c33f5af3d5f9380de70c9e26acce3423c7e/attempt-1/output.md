REFORMULACION  
WS34.1 encarga, en el repo `deskops`, implementar un adaptador público restringido para dispatch de Scion: confirmación como respuesta de la API Scion, identidad de intento, timeout/errores y autoridad del coordinador según WS12. Resultado: `runtime/`, la superficie CLI/API que fije WS12 y `tests/`. Límites: no shell arbitrario, no duplicar transporte, no elegir umbral propio de timeout; sin la política de WS12 se detiene y registra el hueco. Aceptación: con G_EXEC/G_SCION, un agente real demuestra un dispatch aceptado y otro rechazado o vencido por timeout, correlacionado con el id de intento local WS32.1 y registros WS32.2; `confirmed` solo con respuesta observada del Hub.

AMBIGUEDADES  
ninguna

DRY-RUN  
Lecturas: nodo, guía, brief, alcance, decisiones, contrato WS12, salidas WS33/WS32.1/WS32.2, probe WS44/G_SCION y autorización G_EXEC. Cambios previstos: adaptador en `runtime/` y superficie CLI/API definida por WS12, sin nuevo transporte ni shell; pruebas en `tests/`. Dependencias: WS12 debe fijar política/umbral de timeout y superficie; WS33/WS32.1/2 deben aportar correlación; G_EXEC, G_SCION y G_WRITE_CONTRACT deben pasar. Si falta contrato, dato o permiso: detener y registrar hueco, sin inventar umbral ni sustituto. Validaciones futuras: ejecutar agente real, observar dispatch aceptado y rechazado/timeout, comprobar correlación, confirmar solo con respuesta Hub y verificar timeout contra WS12/G_WRITE_CONTRACT. Sin ejecutar.

FUTURO  
WS12 produce política de timeout, clasificación y API/superficie; WS32.1 genera id de intento; WS32.2 registros; WS33 integra referencias; WS44/G_SCION produce probe; humano resuelve G_EXEC; G_WRITE_CONTRACT verifica por delta; WS34.2 añade reply; WS34 cierra cuando ambos hijos cumplen. No son ambigüedades de WS34.1.
