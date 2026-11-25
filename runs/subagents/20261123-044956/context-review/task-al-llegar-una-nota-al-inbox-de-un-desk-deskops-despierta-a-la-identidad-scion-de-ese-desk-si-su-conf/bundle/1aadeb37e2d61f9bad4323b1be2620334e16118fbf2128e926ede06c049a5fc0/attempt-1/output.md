REFORMULACION
Propósito: al llegar una nota al inbox de un desk, deskops debe despertar la identidad scion de ese desk si `identity.wake` lo pide, respetando el gate de memoria. Resultado: campo `identity` en `DeskConfig`; función `wake_identity(root, note_name)`; llamada tras escribir la nota en `message send` sin romper el envío; subcomando `message wake`; tests y goldens. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no arregla `--wake` del fork de scion, no crea RoleDoc, no limita agentes vivos ni lanza scion real en tests. Es un nodo ejecutable `task.code`, no un agregado ni paquete.

AMBIGUEDADES
1. “en un módulo nuevo de deskops”: no fija nombre ni ruta; obligaría a inventar dónde vive `wake_identity`.
2. “llama a wake_identity con la raíz del desk destino” y “se encola con deskops.queue.enqueue”: `enqueue` espera raíz de repo (`root/desk/config.json`), no `desk/`; obligaría a inventar si `root` es repo o `desk`.
3. “se encola con deskops.queue.enqueue”: `enqueue` exige `task_id`/`DESKOPS_TASK_ID` y `transition`; obligaría a inventar qué `task_id` usar (¿nota?, ¿desk?).
4. “sale con código 3 cuando el gate bloquea”: no define código para fallo de ejecución; obligaría a inventar rc distinto de 3/0.

DRY-RUN
Lecturas: TaskDoc, `deskops/config.py`, `deskops/cli/commands/message.py`, `deskops/queue.py`, `tests/test_message_delivery.py`, `tests/test_config.py`, goldens de ayuda. Cambios previstos: modelo `identity` y carga desde `config.local.json`; módulo nuevo con `wake_identity`; llamada tras `_deliver_note` con aviso a stderr y encolado opcional; subcomando `message wake`; tests nuevos y goldens. Dependencias: `DeskConfig.load`, `queue.wait_reason`, `queue.enqueue`, `queue_jobs` declarado, `scion` real aún roto. Validaciones futuras: ejecutar los cinco comandos pytest indicados, incluida la suite completa con `-n 4`.

FUTURO
Otro nodo o un humano debe arreglar `--wake` del fork de scion, crear el RoleDoc de identidad, controlar el límite de agentes desde dispatch, decidir las ambigüedades anteriores y realizar el commit desde el worktree con `Task-Id`.
