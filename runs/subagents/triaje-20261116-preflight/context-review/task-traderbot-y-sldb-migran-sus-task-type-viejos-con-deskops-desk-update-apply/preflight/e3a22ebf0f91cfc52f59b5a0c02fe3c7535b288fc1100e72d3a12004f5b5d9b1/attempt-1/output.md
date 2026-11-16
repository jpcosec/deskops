## REFORMULACION

Propósito: coordinar que los desks de TraderBot y sldb migren sus `task_type` legacy mediante `deskops desk update --apply`, como espejo externo de la tarea que retira caminos legacy. Resultado: ambos desks confirman la migración y el commit; ninguna tarea usa valores sin prefijo `task.`. Repo: no se escribe en TraderBot ni sldb desde deskops; sldb está en `/mnt/ssd/proyectos/SLDB_1/sldb`; TraderBot no está en robocop2. Límites: solo pedir por inbox y registrar commits; no modificar esos repos. No es agregado/paquete: es una tarea externa de coordinación; sus “hijos” son respuestas de otros desks, no nodos del TaskDoc.

## AMBIGUEDADES

1. “si --to traderbot no resuelve en robocop2, pedirlo a JP para la maquina donde vive TraderBot”: obliga a inventar host, identidad y canal de TraderBot.
2. “En los desks ... `deskops desk update --apply` migro”: obliga a inventar comando exacto, versión y quién lo ejecuta.
3. “pedir la migracion a cada desk por inbox”: no define texto, criterio de aceptación ni plazo; obliga a inventar el mensaje.
4. “Registrar los commits de respuesta”: no indica dónde ni con qué formato; obliga a inventar registro.
5. “grep ... `<desk>/desk/tasks/*.md`”: la ruta de TraderBot es desconocida; obliga a inventar `<desk>`.
6. “sin valores sin prefijo task.”: no enumera valores permitidos ni alcance; obliga a inventar criterio.

## DRY-RUN

Lecturas: TaskDoc, registro `repo-traderbot.md`, ayuda de `deskops message` y rutas de ambos desks. Cambios previstos: ningún cambio local en repos externos; enviar dos mensajes y, tras respuesta, anotar commits en el TaskDoc/historial. Dependencias: enrutamiento de deskops, respuesta de sldb y TraderBot/JP. Validaciones futuras: ejecutar grep en cada desk y confirmar commits.

## FUTURO

JP o el operador aporta ubicación/acceso de TraderBot; los responsables de sldb y TraderBot ejecutan la migración y devuelven commits; un humano o nodo validador comprueba el grep y cierra la tarea. Este nodo no decide esas respuestas.
