Task: task-doctor-reporta-el-layout-viejo-de-sldb-y-nombra-sldb-stores-migrate-layout-como-remedio
Title: doctor reporta el layout viejo de .sldb y nombra sldb stores migrate-layout como remedio
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-22T06:19:45Z'
  authority: generated
  via: save_document_payload
id: task-doctor-reporta-el-layout-viejo-de-sldb-y-nombra-sldb-stores-migrate-layout-como-remedio
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
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

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-doctor-reporta-el-layout-viejo-de-sldb-y-nombra-sldb-stores-migrate-layout-como-remedio"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.
