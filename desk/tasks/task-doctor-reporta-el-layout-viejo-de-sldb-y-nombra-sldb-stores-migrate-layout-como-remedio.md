---
sldb:
  by: agent
  at: '2026-11-22T06:32:13Z'
  authority: generated
  via: save_document_payload
id: task-doctor-reporta-el-layout-viejo-de-sldb-y-nombra-sldb-stores-migrate-layout-como-remedio
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history:
- task_activates
- 'task_returns_to_execution: Tester deskops-t-6a1436989fc7 FALLA sobre 2373f55d.


  (1) deskops/sldb_layout.py no detecta en .gitignore las variantes .sldb/core/**,
  .sldb/core/*, .sldb/runtime/** ni .sldb/runtime/*. La resolución aceptada pide quitar
  la barra inicial y los sufijos ''/**'', ''/*'' o la barra final, y dar señal si
  queda exactamente .sldb/core o .sldb/runtime. El tester lo reprodujo: con .sldb/core/**
  en el .gitignore, doctor dice healthy.


  (2) init rechaza un directorio sin store que solo hereda una línea vieja en .gitignore.
  El chequeo de init va en deskops/bootstrap.py (init_local_store, antes de _init_store
  y de cualquier escritura), y solo si la carpeta de store del repo ya existe.


  (3) Se acepta la ubicación deskops/sldb_layout.py. El mensaje tiene que ser el resuelto:
  "old .sldb layout (SEÑALES): run sldb stores migrate-layout --store RUTA", donde
  RUTA es la ruta absoluta de la carpeta de store del repo.


  Intento 2:

  - arreglar 1, 2 y 3, con tests para las cuatro variantes del .gitignore y para init
  en un repo sin store (sale 0 e inicializa);

  - correr tests/test_doctor_sldb_layout.py, test_doctor_alerts.py y test_gitignore_policy.py;

  - correr la suite completa con -n 4 (pip install pytest-xdist en /tmp/ws-venv);
  si no termina en 30 minutos, entregar con los tests enfocados y anotarlo;

  - commitear desde tu worktree con ''git commit -- <rutas>'' y el trailer Task-Id.'
references:
- desk/inbox/20261119-230958-suggestion-guiar-a-los-repos-que-usan-deskops-a-migrar-el-layout-de-sldb-sldb-stores-migrate-layout.md
depends_on:
- task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# doctor reporta el layout viejo de .sldb y nombra sldb stores migrate-layout como remedio

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de hbc_latina (20261119-230958): desde sldb c420809c (2026-11-04) .sldb/ se versiona entero y el cache vive en .sldb_cache/, pero los repos inicializados antes siguen con el layout viejo (.sldb/runtime/, .sldb/journal, .gitignore que ignora .sldb/core o .sldb/runtime) y nada les avisa; un escaneo local encontro 48 stores asi. La migracion existe y es idempotente: sldb stores migrate-layout --store <repo>/.sldb.

## Goal

_Describe the concrete result this task must produce._

deskops doctor detecta el layout viejo por cualquiera de tres senales (existe .sldb/runtime/, existe .sldb/journal, el .gitignore raiz tiene una linea que ignora .sldb/core o .sldb/runtime) y lo reporta como issue con el remedio exacto sldb stores migrate-layout --store <ruta del repo>/.sldb; mientras quede una senal doctor no imprime Desk is healthy. deskops init sobre un repo con .sldb/ en layout viejo falla con el mismo remedio en el mensaje. El README y la skill .claude/skills/deskops-workflow/SKILL.md documentan el procedimiento por repo: ponerse al dia con la rama de integracion, correr sldb stores migrate-layout, revisar git status (si .sldb/core/ estaba ignorado aparece como nuevo), git add .gitignore .sldb (nunca git add -A), deskops doctor, commit con [skip ci] y push, avisar a las otras sesiones del repo.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/commands/doctor.py (el reporte, alrededor de las lineas 220-231 donde imprime Desk is healthy) o el servicio que arma sus findings, deskops/bootstrap.py (init), README.md, .claude/skills/deskops-workflow/SKILL.md y tests nuevos. No entra: correr la migracion en otros repos ni mandar avisos al ecosistema (lo hace cada coordinador despues), ni cambiar sldb. Depende de la tarea que saca la salida de graph export y self-reflection de .sldb/runtime (si no, el propio desk de deskops daria la senal .sldb/runtime/).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer deskops/cli/commands/doctor.py y como junta issues; leer sldb stores migrate-layout --help. 2) Agregar un chequeo de las tres senales que produce un issue con el remedio. 3) init: antes de inicializar, si .sldb/ existe con una senal, salir con codigo distinto de 0 y el remedio. 4) Docs. 5) Tests con un repo temporal por senal y uno ya migrado sin issue.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_doctor_alerts.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_gitignore_policy.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops doctor --root . (sin issue de layout en el desk de deskops, ya migrado)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; cada falla se corre igual en un worktree limpio de origin/main y solo se acepta si falla igual ahi, listada en la entrega)

## Done When

_Name the observable condition that makes the task complete._

Tests nuevos: cada una de las tres senales produce un issue de doctor con el comando sldb stores migrate-layout --store <ruta>/.sldb y sin Desk is healthy; un repo migrado no da el issue; init sobre layout viejo falla nombrando el remedio. README y skill tienen el procedimiento.
