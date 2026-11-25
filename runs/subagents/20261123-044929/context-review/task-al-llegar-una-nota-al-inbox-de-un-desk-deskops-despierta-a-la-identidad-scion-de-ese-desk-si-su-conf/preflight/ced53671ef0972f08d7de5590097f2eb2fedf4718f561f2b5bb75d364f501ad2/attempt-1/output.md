## REFORMULACION

Encargo ejecutable (`task.code`) en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`: al escribir una nota en el inbox de un desk, `deskops` debe despertar la identidad scion de ese desk si su config (`identity.wake`) lo pide, respetando el gate de memoria. Resultado esperado: campo `identity` en `DeskConfig` (`scion_project`, `agent`, `wake`, `command` con marcadores), función `wake_identity(root, note_name)`, llamada desde `message send` sin romper el envío (aviso por stderr y encolado opcional `wake-identity`), subcomando `message wake` con rc 3 al bloquear, más tests y goldens de ayuda. Límites: no arreglar `--wake` del fork scion, no gestionar el límite de 5 agentes, no crear el RoleDoc, no lanzar scion real en tests.

## AMBIGUEDADES

1. «en un módulo nuevo de deskops»: no indica nombre ni ruta; obliga a inventar el módulo.
2. «sus goldens de ayuda»: no identifica qué goldens ni dónde viven; obliga a inventar archivos y formato.
3. «si el desk destino declara en queue_jobs el tipo wake-identity»: no describe el esquema de `queue_jobs`; obliga a inventar cómo se declara.
4. «command (lista de argv opcional con los marcadores {agent}, {project} y {note}…)»: no dice cómo se sustituyen ni si `{note}` es id o ruta; obliga a inventar la sustitución.
5. «deskops.queue.wait_reason(config) da un motivo»: no define firma ni qué cuenta como motivo; obliga a inferir el contrato.
6. «retry_exit_codes [3]»: no aclara si debe configurarse o solo asumirse; obliga a decidir.

## DRY-RUN

Un ejecutor leería `deskops/config.py`, `deskops/cli/commands/message.py`, `deskops/queue.py`, `tests/test_message_delivery.py`, `tests/test_config.py` y los goldens de ayuda. Cambios previstos: añadir el modelo `identity` y su carga desde `config.local.json`; crear el módulo de despertar con gate, timeout 60 s, stdin DEVNULL y sin shell; integrar la llamada tras escribir la nota y añadir `message wake`; escribir cinco tests y actualizar goldens. Dependencias: `DeskConfig.load`, `queue.wait_reason`, `queue.enqueue` y el sistema de goldens. Validaciones futuras: las cinco invocaciones pytest listadas, incluida la suite completa con `-n 4`.

## FUTURO

Quedan fuera y dependen de otros: el arreglo de `--wake` en el fork scion (nota 20261122-233912), la creación del RoleDoc de identidad (tarea aparte), el worktree que entrega dispatch y la decisión humana sobre la tarea paraguas. El límite de agentes vivos lo controla el despacho, no este nodo.
