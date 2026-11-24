---
sldb:
  by: agent
  at: '2026-11-24T02:17:47Z'
  authority: generated
  via: save_document_payload
id: task-deskops-trae-un-roledoc-desk-identity-instalable-en-cualquier-desk-y-runtime-template-lo-materializa
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-234447-suggestion-roledoc-de-identidad-de-desk-desk-identity-y-su-traduccion-a-agente-scion.md
depends_on:
- task-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-el-alias-de-modelo-sale
pills: []
files:
- pyproject.toml
- deskops/cli/commands/desk.py
- deskops/cli/commands/core.py
- deskops/runtime/scion.py
- deskops/cli/commands/runtime.py
- deskops/cli/registry.py
- tests/test_desk_sync.py
- tests/test_scion_runtime.py
- tests/fixtures/golden/help/deskops_runtime_template.txt
- tests/fixtures/golden/scaffold/init.json
- tests/fixtures/golden/scaffold/update.json
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops trae un RoleDoc desk-identity instalable en cualquier desk y runtime template lo materializa como agente scion persistente (--mode identity)

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261122-234447 (scion-coordination, workflow scion + deskops de JP): no hay RoleDoc para la identidad de un desk. deskops tiene deskops-executor, deskops-supervisor y deskops-tester en desk/roles; sldb no tiene desk/roles. El piloto wf-desks arma el prompt pegando reglas de /mnt/ssd/proyectos/wf-desks/bin/desk-prompt.sh delante de desk/roles/deskops-supervisor.md, fuera de deskops. Texto base vigente, autorizado por Governance: /srv/wt/labchile_chatbots/.encargo-triaje-inbox.txt. Relacionadas, no se duplican: task-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-el-alias-de-modelo-sale (tools del RoleDoc a claude, dependencia) y task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale (image, resources y volumes en --config).

## Goal

_Describe the concrete result this task must produce._

(1) deskops empaqueta como dato (junto a las plantillas de deskops/data/templates) un RoleDoc desk-identity: name desk-identity, kind claude, tools read, grep, find, ls, bash, y un cuerpo con estas reglas: triar el inbox propio (ack con motivo, tarea + ack, o dejar abierto lo que pide decisión de JP y decirlo); reenviar lo ajeno por deskops message send --to <dueño>; registrar un acuerdo cerrado en un hilo como atom con la referencia del hilo, una sola vez; mandar lo sin dueño a su destino; no implementar código, no despachar, no tocar la cola, no hacer push; desk/ y .sldb/ solo con los CLI; todo comando con --root <raíz del desk>. (2) deskops desk update --apply (y el modo en seco lo lista) instala ese RoleDoc en desk/roles de un desk que no lo tiene, con deskops add role por debajo; no pisa uno existente. (3) deskops runtime template acepta --mode identity: escribe un agents.md de identidad persistente que nombra la raíz del desk y el proyecto scion, sin worktree por agente (workspace relativo en un proyecto de carpeta sin git, el único modo que admite reincarnate) y sin las instrucciones de ejecutor/tester/coordinador.

## Scope

_State what is in scope and what is out of scope._

Entra: el RoleDoc empaquetado como payload YAML (archivo desk-identity.yaml en una carpeta roles nueva del paquete, hermana de la carpeta templates de deskops/data; NO dentro de data/templates, porque lo que esta ahi lo siembra seed_desk como semilla gestionada y lo restauraria) y su entrada en [tool.setuptools.package-data] de pyproject.toml (un patron para los YAML de esa carpeta roles); la instalacion en deskops/cli/commands/desk.py (desk update) y en deskops init (deskops/cli/commands/core.py, InitCLI, para que un desk recien creado siga "Desk is up to date"); --mode identity en deskops/runtime/scion.py y en la declaracion de runtime template de deskops/cli/registry.py (choices de --mode); goldens de ayuda (tests/fixtures/golden/help/deskops_runtime_template.txt) y de scaffold (tests/fixtures/golden/scaffold/init.json y update.json, que ganan el RoleDoc role-desk-identity.md en la carpeta roles del desk); tests/test_scion_runtime.py y tests/test_desk_sync.py. No entra: crear el agente en scion, el hook que lo despierta (tarea aparte), cambios en el repo scion, el mapa de propiedad, la traduccion de tools a claude (dependencia).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test en tests/test_desk_sync.py: test_desk_update_installs_desk_identity_role (en un desk sin el rol, desk update en seco lista "Missing role: desk-identity" y sale 1 como con cualquier divergencia; con --apply queda el archivo role-desk-identity.md en la carpeta roles del desk, deskops show role desk-identity lo lee; una segunda corrida dice "Desk is up to date."; un role-desk-identity.md existente en la carpeta roles del desk, aunque tenga otro cuerpo, no se pisa). p2: test en tests/test_scion_runtime.py: test_runtime_template_identity_mode (con el rol instalado en el desk temporal, el agents.md nombra la raiz del desk y el proyecto scion, no contiene "worktree" ni "deskops dispatch"; --mode foo sigue fallando: argparse lista las cinco opciones y el ValueError de scion.py, hoy "mode must be executor, coordinator, tester or specialist, got '<x>'" en deskops/runtime/scion.py linea 384, pasa a "mode must be executor, coordinator, tester, specialist or identity, got '<x>'"). p3: implementar. Instalacion: una funcion compartida (en deskops/cli/commands/desk.py) que, si en la carpeta roles del desk ningun RoleDoc tiene name desk-identity ni id role-desk-identity y no existe el archivo role-desk-identity.md (cualquiera de las tres cuenta como existente), crea el rol con la misma ruta que deskops add role --from-yaml (parse_artifact_input + DeskopsOperations.create_artifact("artifact.role", payload)), sin lanzar un subproceso del CLI; asi queda el archivo role-desk-identity.md con id role-desk-identity, trackeado en el store; desk update la llama en --apply y en seco solo la lista; InitCLI la llama despues de seed_desk. Payload: name desk-identity, kind claude, tools [read, grep, find, ls, bash], description de una linea, y body en espanol con estas secciones y comandos literales: Triaje del inbox propio (cada nota abierta termina en una salida: deskops message ack <id> --reason "<motivo>" --root <raiz del desk> si es informativa, duplicada, resuelta u obsoleta; deskops add task ... que cite la nota y despues el ack; o queda abierta si pide una decision de JP (elegir entre alternativas, aprobar algo irreversible o externo, fijar duenos, fechas o prioridades, o lo dice explicitamente), y se dice en la respuesta con la pregunta concreta); Reenvio (lo que es de otro desk va con deskops message send --to <desk dueno> --root <raiz del desk> y despues el ack; el dueno es el repo del registro del desk (deskops list repositories --root <raiz del desk>) cuyo nombre, ruta o descripcion cubre el asunto; lo que no tiene dueno claro va con deskops message send --to unowned --root <raiz del desk> si el desk declara unowned_target (lo agrega otra tarea); si no, queda abierto y se dice); Acuerdos (un acuerdo cerrado, es decir que el hilo dice explicitamente que quedo acordado, se registra una sola vez con deskops add atom --root <raiz del desk>, con la referencia del hilo ("<hilo>/<id de mensaje>" o "<hilo>") en --provenance "conv:<referencia>", mirando antes deskops list atoms --root <raiz del desk>); Limites (no implementar codigo, no despachar, no tocar la cola, no hacer push; desk/ y .sldb/ solo con los CLI deskops y sldb; todo comando con --root <raiz del desk>). Modo identity: rama nueva en la seleccion de agents.md de scion.py (hoy lineas 495-504) con una funcion _render_identity_agents_md que usa _example_roots (linea 508) para nombrar desk_root y project, dice que el agente es persistente, trabaja en su carpeta (workspace relativo de un proyecto de carpeta sin git, el unico modo que admite reincarnate) y no menciona worktree, deskops dispatch ni instrucciones de ejecutor, tester o coordinador. p4: goldens: TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py --update-golden y tests/test_scaffold_golden.py --update-golden, revisando que el diff solo agregue la opcion identity y el rol. p5: suite con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_desk_sync.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos pasan; deskops init deja un desk con el RoleDoc role-desk-identity.md en su carpeta roles y desk update dice Desk is up to date; y, en un desk temporal con el rol instalado, deskops runtime template desk-identity --mode identity --root <desk temporal> escribe el template sin error.
