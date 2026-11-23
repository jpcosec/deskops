---
sldb:
  by: agent
  at: '2026-11-23T08:23:53Z'
  authority: generated
  via: save_document_payload
id: task-al-llegar-una-nota-al-inbox-de-un-desk-deskops-despierta-a-la-identidad-scion-de-ese-desk-si-su-conf
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- desk/inbox/20261122-234436-suggestion-hook-que-despierta-a-la-identidad-scion-del-desk-cuando-llega-una-nota-al-inbox.md
depends_on: []
pills: []
files:
- deskops/config.py
- deskops/cli/commands/message.py
- deskops/queue.py
- tests/test_message_delivery.py
- tests/test_config.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Al llegar una nota al inbox de un desk, deskops despierta a la identidad scion de ese desk si su config lo pide (identity.wake), respetando el gate de memoria

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261122-234436 (scion-coordination, encargo de JP para el workflow scion + deskops): JP pidió "uno por desk, pero en scion y se activa por hook en deskops"; la identidad queda parada por defecto y se despierta cuando le llega trabajo. Hoy nada avisa: deskops message send (MessageCLI._deliver_note en deskops/cli/commands/message.py) solo escribe la nota, y los hooks de deskops/lifecycle_hooks.py corren solo al avanzar una transición. Es la pieza de activación de task-governance-agente-interno-por-desk-en-scion-activado-por-hooks-de-deskops (el paraguas, todavía borrador); esta tarea no la duplica: hace solo el disparo por nota.

## Goal

_Describe the concrete result this task must produce._

(1) DeskConfig (deskops/config.py) gana un campo opcional identity con: scion_project (str), agent (str), wake (bool, por defecto false) y command (lista de argv opcional con los marcadores {agent}, {project} y {note}; por defecto ["scion", "message", "--wake", "@{agent}", "--project", "{project}", "nota nueva: {note}"]). Se espera que viva en el config.local.json del desk (es de la máquina), que DeskConfig.load ya mezcla sobre config.json. (2) Una función wake_identity(root, note_name) en un módulo nuevo de deskops: si identity falta o wake es false no hace nada; si deskops.queue.wait_reason(config) da un motivo, no despierta y devuelve "bloqueado: <motivo>"; si no, corre el argv sin shell (stdin DEVNULL, timeout 60 s) y devuelve "despertado" o "fallo: <rc>". (3) Después de escribir la nota en el desk destino, deskops message send llama a wake_identity con la raíz del desk destino. Un fallo o un bloqueo nunca hace fallar el send: se imprime un aviso en stderr. Si quedó bloqueado y el desk destino declara en queue_jobs el tipo wake-identity, se encola con deskops.queue.enqueue para el siguiente ciclo de la cola. (4) Un subcomando deskops message wake --root <desk> [--note <id>] corre wake_identity a mano y sale con código 3 cuando el gate bloquea (para que la cola lo reintente con retry_exit_codes [3]).

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/config.py, deskops/cli/commands/message.py, el módulo nuevo, sus goldens de ayuda, tests/test_message_delivery.py y tests/test_config.py. No entra: arreglar --wake en el fork de scion (nota 20261122-233912 del desk de scion; hoy --wake falla, así que el uso real espera ese arreglo, pero la implementación y los tests no), el límite de 5 agentes vivos (lo controla el despacho), crear el RoleDoc de identidad (tarea aparte), lanzar scion de verdad en los tests.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_message_delivery.py con un command falso ["sh", "-c", "echo \"$0 $1\" >> <archivo>", "{agent}", "{note}"] en el config.local.json de un desk temporal: test_send_wakes_the_target_identity (el archivo recibe el agente y el nombre de la nota), test_send_does_not_wake_when_wake_is_false, test_send_with_memory_gate_blocked_enqueues_wake_identity (wait_reason parcheado; el send termina con rc 0 y queda un trabajo wake-identity pendiente), test_wake_command_exits_3_when_blocked. p2: test en tests/test_config.py: DeskConfig.load toma identity del config.local.json. p3: implementar. p4: goldens de ayuda. p5: suite con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_delivery.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_config.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los cinco tests nuevos pasan; deskops message send en un desk sin identity se comporta igual que hoy (los tests existentes de tests/test_message_delivery.py y tests/test_message_cli.py siguen verdes sin cambios).
