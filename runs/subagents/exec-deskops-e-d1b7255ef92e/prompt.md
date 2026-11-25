Task: task-deskops-add-adr-crea-un-registro-de-decision-con-estado-contexto-decision-consecuencias-y-a-cual-ree
Title: atom.adr: un ADR es un átomo con estado, contexto, consecuencias y a cuál reemplaza; se crea con deskops add atom --atom-type atom.adr y se lista filtrando los vigentes
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: closed [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .
  blocked by: error: [rules/rule-activation-task-code] TaskCodeDoc:task-deskops-add-adr-crea-un-registro-de-decision-con-estado-contexto-decision-consecuencias-y-a-cual-ree: Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight") (seen: {}) (witness: ReviewDoc:review-task-deskops-add-adr-crea-un-registro-de-decision-con-estado-contexto-decision-consecuencias-y-a-cual-ree-bundle-1 {"anchor_state":"changed"})

---
sldb:
  by: agent
  at: '2026-11-25T18:23:28Z'
  authority: generated
  via: save_document_payload
id: task-deskops-add-adr-crea-un-registro-de-decision-con-estado-contexto-decision-consecuencias-y-a-cual-ree
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# atom.adr: un ADR es un átomo con estado, contexto, consecuencias y a cuál reemplaza; se crea con deskops add atom --atom-type atom.adr y se lista filtrando los vigentes

## Rationale

_Explain why this task exists or the business driver behind it._

Pedido de JP (2026-11-25): "es en extremo importante empezar a entrar a documentar ADRs en deskops". Ese día se revirtió dos veces la misma decisión sobre la interfaz de specIR, y JP daba pron por retirado cuando el único registro (un ADR en Markdown dentro de sldb, de septiembre) decía otra cosa y nadie lo encontró. Hoy una decisión queda repartida entre un átomo, un task.decision, un review dispose y documentos sueltos en docs/ de cada repo, y nada lista las decisiones vigentes ni cuál reemplazó a cuál.

## Goal

_Describe the concrete result this task must produce._

Que una decisión de arquitectura sea un subtipo de átomo, atom.adr, modelado igual que los tipos de tarea: una subclase AtomAdrDoc de AtomDoc que solo agrega campos, con sus compuertas como RuleDoc y su relación de reemplazo como arista. JP (2026-11-25): 'inventalo, creo que atom.adr sería un buen modelo'.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/models/ (AtomAdrDoc y un registro ATOM_TYPE_MODELS como TASK_TYPE_MODELS), deskops add atom con --atom-type, el filtro por tipo y estado al listar átomos, el tipo de relación supersedes, las reglas sembradas en deskops/data/rules/, la materialización del ADR a Markdown y el manual del operador. Fuera: cambiar AtomDoc (su contrato y su hash no se tocan: el subtipo solo agrega), una interfaz, migrar decisiones anteriores a las cinco del 2026-11-25, federar ADR entre desks.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer primero deskops/models/task_types.py (un tipo es un modelo, no un string; un subtipo solo agrega; las compuertas son RuleDoc sembradas con sujeto model <= Tipo) y deskops/models/atom.py. Diseño de partida: AtomAdrDoc(AtomDoc) con five_wh_one_plus fijo en what y answer como el enunciado de la decisión; agrega status (proposed, accepted, superseded, rejected), decided_on, decided_by, y las secciones context, consequences, alternatives (opcional) y not_verified (opcional). Id adr-<slug>; tags por defecto system:deskops y topic:adr; los repos afectados van como tags repo:<nombre>. El reemplazo es una arista supersedes de ADR a ADR (RelationTypeDoc), no un campo: crearla pone el anterior en superseded, y una RuleDoc exige que ningún ADR accepted tenga una arista supersedes entrante de otro accepted. Otra RuleDoc exige recibo de owner para pasar a accepted, igual que la activación de task.decision. Un task.decision cierra citando un atom.adr con la evidencia atom que ya existe; no se crea un tipo de evidencia nuevo. El Markdown en docs/ es una materialización del átomo (deskops materialize), no un archivo escrito a mano. Si al leer aparece que task.decision, los átomos de decisión o review dispose ya cubren contexto, alternativas y reemplazo con un cambio menor, se extiende eso y se deja escrito por qué.

Aclaraciones de la revisión: la opción 'todos' es --all. Los cinco ADR a sembrar: /mnt/ssd/proyectos/SLDB_1/sldb/docs/architecture/{mechanism-in-sldb-content-in-specir,pron-is-archived,one-command-taxonomy-served-by-fastmcp,surface-is-an-editor-contract}.md y /mnt/ssd/proyectos/SLDB_1/IR/docs/decisiones/paridad-por-capacidades.md (se leen por ruta absoluta; el AtomAdrDoc vive en el desk de deskops). Recibo de owner: el mismo mecanismo que task.decision (deskops review record --kind owner y dispose accepted, solo JP); no se inventa otro. Repos afectados: los declara quien crea el ADR con --repo (repetible), que se guardan como tags repo:<nombre>; para los cinco sembrados, los repos que el ADR nombra en su texto. Reemplazo parcial (pron-is-archived sobre la sección de pron de sldb-absorbs-kgdb): arista supersedes al ADR entero con un atributo opcional section; el ADR reemplazado parcialmente sigue accepted. Vigente = accepted y sin supersedes total entrante; list sin --all muestra solo esos. Campos opcionales (alternatives, not_verified) se materializan como sección solo si están. 'Cambio menor' = agregar campos opcionales sin romper documentos existentes; si se extiende algo existente en vez de crear AtomAdrDoc, el porqué va en el commit y en result-summary. No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_adr_artifact.py
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

deskops add atom --atom-type atom.adr crea el registro y rechaza un status fuera de la lista. Pasar un ADR a accepted sin recibo de owner lo rechaza la regla. Declarar que un ADR reemplaza a otro deja al anterior en superseded y la regla de consistencia pasa. Listar átomos de tipo atom.adr muestra por defecto solo los accepted y con una opción todos. Un task.decision cierra citando un atom.adr. Materializar un ADR produce un Markdown con Status, Date, Decision Maker, Supersedes, Context, Decision y Consequences. El hash del contrato de AtomDoc no cambia. Quedan cargados los cinco ADR del 2026-11-25 (cuatro de sldb/docs/architecture/ y IR/docs/decisiones/paridad-por-capacidades.md), con pron-is-archived reemplazando la sección de pron del ADR sldb-absorbs-kgdb. El manual del operador describe el flujo.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-deskops-add-adr-crea-un-registro-de-decision-con-estado-contexto-decision-consecuencias-y-a-cual-ree"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-d1b7255ef92e"

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-d1b7255ef92e`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-d1b7255ef92e

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
