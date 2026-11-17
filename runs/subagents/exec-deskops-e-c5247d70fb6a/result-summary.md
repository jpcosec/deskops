# Resultado del ejecutor deskops-e-c5247d70fb6a (intento 1)

- run_id: run-deskops-e-c5247d70fb6a
- task: task-se-retiran-del-drawer-los-planes-workspace-documental-gates-por-tipo-deskops-ui-y-deskops-como-confi
- session: scion://agent/deskops-e-c5247d70fb6a (agente claude); session_sha256: no disponible desde la sesión
- Estado: **BLOQUEADO**. El código, los tests, las docs y los git rm están hechos y en verde. Lo que falla es el done_when «graph missing no crece»: pasa de 35 a 50 entradas, y dejarlo en 35 obliga a editar TaskDocs de `desk/tasks/` que este encargo no me deja tocar.

## Qué cambié

| Archivo | ¿Está en files? | Por qué |
|---|---|---|
| `tests/fixtures/plans/gates-por-tipo/dag.yaml` (nuevo) | lo nombra el scope («fixture nuevo en tests/fixtures/plans/») | copia recortada del plan real: cabecera, gates sin G_CONSUMER (su produced_by GC05 ya no está), external_references, ROOT (children: [PC01]), PC01, y GC01, GC02 y GC03 sin cambios. Lleva un comentario con el origen. |
| `tests/fixtures/plans/gates-por-tipo/brief.md` (nuevo) | igual | copia literal; `test_third_good_attempt...` lo reescribe. alcance.md, decisiones.md y context-review-guide.md no hacen falta: el servicio lee los cuatro base solo si existen. |
| `tests/test_review_command.py` | sí | `PLAN_SRC` apunta al fixture. La ruta de destino dentro del desk temporal (`desk/drawer/plans/gates-por-tipo`) y los ids esperados no cambian. |
| `tests/test_review_doc.py` | sí | sin cambios: precisión (2), los literales son valores de validación. |
| `deskops/cli/registry.py` | sí | 3 ejemplos de ayuda: `desk/drawer/plans/mi-plan N01` y `desk/drawer/plans/mi-plan` (precisión 3). |
| `tests/fixtures/golden/help/deskops_review.txt`, `deskops_review_node.txt`, `deskops_review_status.txt` | no (los nombra el scope y la precisión 4) | se actualizó la misma línea que en registry.py; test_output_goldens y test_cli_help_examples los comprueban. |
| `docs/operator-manual.md` | sí | línea 1137 → `mi-plan N01`. |
| `docs/deskops-ui.md` | sí | línea 209 con el texto exacto de la precisión (5). La fila de la línea 230, «plan `gates-por-tipo`, sldb GO07», queda: nombra el plan sin ruta. |
| `desk/drawer/plans/{workspace-documental,gates-por-tipo,deskops-ui,deskops-como-config}/` | dag.yaml de gates-por-tipo sí; el resto lo nombra el scope | `git rm -r` (en el índice, sin commit). Quedaba `workspace-documental/__pycache__/` ignorado y sin seguimiento: lo borré junto con los directorios vacíos. `desk/drawer/plans/` ya no existe. |
| `desk/drawer/tasks/workspace-documental/` | lo nombra el scope | `git rm -r` (en el índice). |

## Validación (detalle en validation.log)

- Antes de borrar, con el fixture y el plan real presente: `tests/test_review_command.py`: 29 passed, rc=0.
- Después de borrar (rc=0 en los cuatro): test_review_command.py 29 passed; test_review_doc.py 22 passed y 1 xfailed; test_output_goldens.py 7 passed; test_cli_help_examples.py 13 passed.
- `deskops graph missing --root .`: **35 → 50** (graph-before.txt, graph.txt). Las 15 entradas nuevas son todas `missing_declared_target` desde TaskDocs que declaran rutas de los planes borrados en sus references o files:
  - task-cc51-… → deskops-como-config/dag.yaml y decisiones.md (2)
  - task-cc52-… → deskops-como-config/dag.yaml (1)
  - task-cc53-… → deskops-como-config/dag.yaml (1)
  - task-jp-confirma-o-revierte-do4-… → deskops-como-config/decisiones.md (3)
  - task-jp-decide-si-el-plan-workspace-documental-… → deskops-ui/decisiones.md y workspace-documental/cierre.md (2)
  - task-jp-fija-n-la-meta-de-lineas-… → deskops-como-config/dag.yaml y decisiones.md (3)
  - task-los-rituales-context-review-y-phase-… (GC08) → gates-por-tipo/dag.yaml (2)
  - esta misma tarea → gates-por-tipo/dag.yaml en su `files` (1)
- No corrí la suite completa ni `stores build --check`: quedan para el integrador.

## Bloqueo

El done_when y la precisión (6) piden que graph missing no crezca. Con el scope y las reglas del encargo, eso no se puede cumplir:
- Las 15 entradas nuevas están en 8 TaskDocs de `desk/tasks/`. El encargo prohíbe tocar `desk/` salvo los git rm, y el scope deja fuera la tarea de GC08.
- `tests/test_graph_missing_existing_files.py` y su excepción de CHANGELOG cubren solo los targets que existen como archivo. Una ruta borrada vuelve a contar como missing, como debe ser.

Opciones para el coordinador (las decide él, no yo):
1. Quitar o cambiar esas references y files en los 8 TaskDocs con `deskops edit task …`, en esta tarea o en una previa. Por ejemplo, apuntarlas al recibo de review node de `desk/reviews/` o al commit que borra el plan. La entrada de esta tarea desaparece al cerrarla, o editando su `files`.
2. Aceptar el aumento como esperado y corregir el done_when.

Todo lo hecho se puede revertir: `git restore --staged --worktree desk/drawer` devuelve los planes, y los cambios de código son independientes del borrado.

## Riesgos y notas

- Los cuatro archivos de la Validation pasan. No corrí la suite completa, así que no hay fallas que comparar con origin/main: queda para el integrador.
- Fuera de `files` siguen citando los planes borrados, como texto histórico y no como rutas que se lean: CHANGELOG.md:44, un comentario en tests/test_task_lifecycle_validator.py:74, la nota de desk/inbox (IR13), recibos en desk/reviews y runs/. Los literales de tests/test_review_doc.py se quedan como están por la precisión (2). El texto del fixture (frozen_note, external_references) también nombra rutas del drawer: son datos del fixture.
- Los cambios en `.sldb/` y en `runs/` que ya estaban sucios no son míos y no los toqué.
