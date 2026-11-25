Task: task-docs-auditoria-atomos-y-pills-md-clasifica-cada-atomo-y-cada-pill-de-los-cuatro-desks-con-las-tres-p
Title: docs/auditoria/atomos-y-pills.md clasifica cada átomo y cada pill de los cuatro desks con las tres preguntas de la propuesta
Status: active
Current node: ritual-testing
Task type: task.docs
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-25T20:48:16Z'
  authority: generated
  via: save_document_payload
id: task-docs-auditoria-atomos-y-pills-md-clasifica-cada-atomo-y-cada-pill-de-los-cuatro-desks-con-las-tres-p
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# docs/auditoria/atomos-y-pills.md clasifica cada átomo y cada pill de los cuatro desks con las tres preguntas de la propuesta

## Rationale

_Explain why this task exists or the business driver behind it._

Propuesta deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md (JP, 2026-11-25): "hay muchas pills mal hechas, y muchos átomos también". Hay 647 átomos y 59 pills en los desks de graph_ui, deskops, sldb e IR; 450 átomos responden cómo, qué o dónde, que son los candidatos a estar repitiendo el código o lo que specIR puede extraer. Antes de tipar nada hay que saber cuánto sobra.

## Goal

_Describe the concrete result this task must produce._

Una tabla con un veredicto por documento, para que JP decida qué se retira, qué se mueve y qué se queda.

## Scope

_State what is in scope and what is out of scope._

Dentro: leer los átomos y las pills de los cuatro desks y escribir el informe. Fuera: retirar, mover o editar cualquiera de ellos.

## Implementation Path

_Outline the expected implementation route or affected surface._

Las tres preguntas, en orden: si se puede leer del código o de su docstring; si lo puede extraer specIR; si seguiría valiendo sin el trabajo en curso. Para la primera se abre el código al que el documento se refiere y se cita archivo y línea. No se clasifica por el título.

Aclaraciones de la revisión: Desks: /mnt/ssd/proyectos/SLDB_1/{UIs/graph_ui,deskops,sldb,IR}/desk; átomos = desk/atoms/atom-*.md y pills = las de desk/contexts/ (las que lista 'deskops list pills --root <repo>'); censo con 'deskops list atoms|pills --root <repo>', sin drawer ni retirados; si el número difiere de 647/59, se usa el real y se dice. Las tres preguntas y las definiciones son las de deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md (leerlo primero). specIR = el extractor de /mnt/ssd/proyectos/SLDB_1/IR (specir extract): 'lo extrae' si hoy produce ese hecho, 'lo extraería' si es del tipo que extrae pero falta. Trabajo en curso = tareas no cerradas de los cuatro desks y los planes de drawer. Documento sin código referido: se busca el código por grep del concepto; si no hay, veredicto 'no se sostiene'. Pills: los mismos veredictos aplicados a lo que la pill afirma. Sin clasificar = no se pudo abrir ni encontrar el código o el texto es ambiguo; 'no se sostiene' = el código contradice lo afirmado o ya no existe. Evidencia mínima: archivo:línea. Salida en deskops/docs/auditoria/atomos-y-pills.md; es solo lectura, no se edita ningún átomo ni pill.

## Validation

_List the checks required before this task can close._

- test -f docs/auditoria/atomos-y-pills.md

## Done When

_Name the observable condition that makes the task complete._

Cada átomo y cada pill aparece una vez con uno de estos veredictos y su motivo en una línea: ya está en el código (con archivo y línea), falta en el docstring, lo extrae o lo extraería specIR, es una decisión, es un invariante, es contexto de un trabajo abierto, o no se sostiene. El informe trae los totales por desk y por veredicto, y lista aparte los que no se pudieron clasificar.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-docs-auditoria-atomos-y-pills-md-clasifica-cada-atomo-y-cada-pill-de-los-cuatro-desks-con-las-tres-p"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-3c73ef7253ca"
