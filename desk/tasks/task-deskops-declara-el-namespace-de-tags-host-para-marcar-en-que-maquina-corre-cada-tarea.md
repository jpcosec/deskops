---
sldb:
  by: agent
  at: '2026-11-22T16:45:30Z'
  authority: generated
  via: save_document_payload
id: task-deskops-declara-el-namespace-de-tags-host-para-marcar-en-que-maquina-corre-cada-tarea
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
history:
- task_activates
- 'task_returns_to_execution: Tester deskops-t-52556b8a9207 FALLA.


  Bloqueante: la declaración del namespace host quedó en desk/atoms/tag-namespaces.yaml,
  pero el store del desk no se sincronizó. En HEAD, tag_models de store.yaml no incluye
  TaskDoc ni declara el namespace host, y deskops desk update --root . informa la
  divergencia ''Tag namespace declaration: store.yaml differs from desk/atoms/tag-namespaces.yaml''
  y sale 1.


  Además, el commit duplicó en store.yaml una segunda sección ''- model: RelationTypeDoc''
  con las rutas de sldb/relation_types/*.


  Intento 2:

  1. Quitar del store la sección RelationTypeDoc duplicada. Que quede una sola, y
  que la herramienta la regenere: no se edita a mano.

  2. Sincronizar el store con ''deskops desk update --apply --root .'' y commitear
  los archivos del store que toque.

  3. Comprobar que ''deskops desk update --root .'' sale 0 y que ''sldb stores check
  --store'' sobre la carpeta de store del desk no da hallazgos nuevos.

  4. Que el test de la tarea compruebe además que, después de declarar el namespace,
  desk update no informa divergencia.

  5. Correr los tests de la tarea y la suite con -n 4 (pytest-xdist ya está en [dev]).

  6. Commitear desde tu worktree con ''git commit -- <rutas>'' y el trailer Task-Id.'
- task_activates
references:
- desk/inbox/20261116-003533-suggestion-namespace-de-tags-host-para-marcar-en-qu-m-quina-corre-cada-tarea.md
- desk/inbox/20261116-003602-suggestion-namespace-de-tags-host-para-separar-tareas-de-ui-local-y-backend-robocop2.md
- desk/inbox/20261116-004642-suggestion-namespace-de-tags-host-para-rutear-tareas-por-m-quina-host-local-host-robocop2.md
depends_on: []
pills: []
files:
- deskops/atom_tags.py
- docs/workflow-policy-reference.md
- .sldb/store.yaml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops declara el namespace de tags host para marcar en que maquina corre cada tarea

## Rationale

_Explain why this task exists or the business driver behind it._

Dos notas del 2026-11-16 (IR y deskops), del triaje de drawers e inbox: JP pide que cada TaskDoc diga en que maquina corre. Lo que tiene UI o verificacion en navegador va a la maquina local; suites, build --check, benchmarks, migraciones, scion y revisiones van a robocop2. La via es TaskDoc.tags, pero ningun store del ecosistema declara un namespace para la maquina (deskops no declara tag_namespaces en .sldb/store.yaml; sldb e IR solo tienen domain, layer, system y topic).

## Goal

_Describe the concrete result this task must produce._

La declaracion de tag namespaces que deskops sincroniza en cada desk (deskops/atom_tags.py, alrededor de 159-204, que arma TagNamespace(name=..., anchored_by=...)) agrega host como TagNamespace(name='host', hierarchical=False), usando el modelo sldb.api.stores.tag_namespace.TagNamespace tal cual (campos name, hierarchical, folder_axis, anchored_by). tag_models es global en sldb, asi que TaskDoc entra en tag_models y, para que las tareas existentes no den alertas, se declaran tambien workspace, artifact y source (hierarchical=False). meaning, use_when y do_not_use_when de host van en el registro de atom tags que escribe deskops (DEFAULT_ATOM_TAG_NAMESPACES, mismo formato que las demas entradas): meaning 'maquina donde se ejecuta y valida la tarea'; use_when 'tareas con UI o verificacion en navegador -> host:local; backend, suites, migraciones, scion y revisiones -> host:robocop2'; do_not_use_when 'atoms y pills'. Los valores no se restringen (sldb no tiene enumeraciones). docs/workflow-policy-reference.md, en la seccion '### Tasks', suma una linea: 'TaskDoc.tags may carry host:local or host:robocop2: the machine that runs and validates the task (UI and browser checks run locally; backend on robocop2).' Tras deskops desk update --apply en el desk de deskops, una tarea con host:robocop2 no produce alertas de tag en sldb stores check. Criterio de detencion: si con workspace, artifact y source declarados sldb stores check sigue dando alertas de tag en tareas existentes del desk de deskops, se manda deskops message send --to sldb pidiendo namespaces por modelo y la tarea cierra solo con la documentacion.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/atom_tags.py, la semilla de desk que la usa, docs/workflow-policy-reference.md (una linea que explique el tag host) y un test nuevo o ampliado en tests/ (buscar el test actual de tag namespaces con `grep -rln tag_namespaces tests/`). No entra: taggear las tareas existentes (lo hace cada coordinador despues), restringir valores si sldb no soporta enumeraciones (se documentan). Precisiones del preflight 1: en sldb, tag_namespaces es una lista de {name, hierarchical, folder_axis} y tag_models es una lista GLOBAL de modelos (hoy AtomDoc y ProtoAtomDoc en sldb/.sldb/store.yaml): agregar TaskDoc hace que se validen TODOS sus tags, y las tareas ya usan workspace:, artifact: y source:. Por eso la entrada es: host con hierarchical: false y folder_axis: false, y si TaskDoc entra en tag_models se declaran tambien workspace, artifact y source. Si sldb no admite eso sin alertas en tareas existentes, la tarea se detiene, manda deskops message send --to sldb pidiendo namespaces por modelo, y cierra solo con la parte de documentacion. Textos: meaning 'maquina donde se ejecuta y valida la tarea'; use_when 'tareas con UI o verificacion en navegador -> host:local; backend, suites, migraciones, scion y revisiones -> host:robocop2'; do_not_use_when 'atoms y pills'. Los valores no se restringen (sldb no tiene enumeraciones): se documentan. La tarea de prueba es una creada en el desk sandbox del test. docs/workflow-policy-reference.md es el de este repo (deskops). El test va en tests/test_atom_tags.py (ampliado).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer deskops/atom_tags.py completo y sldb docs/architecture/tags.md. 2) Agregar host a la semilla con tag_models que incluya TaskDoc. 3) Test: desk sandbox, desk update --apply, TaskDoc con host:robocop2, `sldb stores check` sin alerta de tag. 4) Aplicar en el desk de deskops y commitear .sldb/store.yaml.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_atom_tags.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_domain_tree.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops desk update --apply --root . && PYTHONPATH=../sldb/src:. ../.venv/bin/python -m sldb stores check --store .sldb (sin alertas de tag por host)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El store de deskops declara host; una tarea con host:robocop2 no da alertas; el test pasa; la doc lo explica.
