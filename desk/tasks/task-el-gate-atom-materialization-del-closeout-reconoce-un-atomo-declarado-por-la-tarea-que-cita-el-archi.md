---
sldb:
  by: agent
  at: '2026-11-25T02:51:01Z'
  authority: generated
  via: save_document_payload
id: task-el-gate-atom-materialization-del-closeout-reconoce-un-atomo-declarado-por-la-tarea-que-cita-el-archi
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files:
- deskops/services/closure.py
- tests/test_closeout_atom_cites_file.py
- docs/operator-manual.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-gate-atom-materialization-del-closeout-acepta-un-atomo-declarado-por-la-tarea-que-cita-el-archivo
---

# El gate atom|materialization del closeout reconoce un atomo declarado por la tarea que cita el archivo cambiado, de cualquier tipo

## Rationale

_Explain why this task exists or the business driver behind it._

Piloto UI-122 de MEPU (nota PARA DESKOPS 20261124-222637 punto 11): una tarea de UI (.ts/.tsx/.css, build en src/frontend/v2/) queda bloqueada en closeout aunque declara en atoms un atomo cuyo provenance y respuesta citan esos archivos; el grafo solo tiene nodos de archivos Python de desk/ y deskops/.

## Goal

_Describe the concrete result this task must produce._

closeout verify acepta como enlace de un archivo cambiado un atomo declarado en atoms o references cuya provenance o texto cite la ruta (o su directorio); el mensaje del hallazgo dice que forma de enlace se acepta.

## Scope

_State what is in scope and what is out of scope._

deskops/services/closure.py (gate atom_or_materialization_link y _link_documents), tests/test_closeout_atom_cites_file.py y la fila atom/materialization de la tabla de evidencia en docs/operator-manual.md. Fuera: el grafo declarado y los demas gates.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Atomos declarados: los ids del campo atoms y las references que apuntan a un atomo (reference_points_to_atom: id atom-..., atom:atom-..., o ruta desk/atoms/...md); se resuelven a su archivo bajo desk/atoms (rglob <id>.md) y se lee el texto completo (frontmatter con provenance mas cuerpo). Un id sin archivo local se ignora. 2. Para cada ruta de files sin evidencia de grafo ni materialization, la ruta normalizada relativa a la raiz (sin barra final) cuenta como citada si aparece como token completo: no precedida por letra, digito, '.', '/' o '-', ni seguida por letra, digito, '-' o '.<letra>' (OcsPanel.tsx.bak no cita OcsPanel.tsx); o si aparece asi un directorio que la contiene con al menos dos partes (frontend/src/screens/ocs/ cubre frontend/src/screens/ocs/ocs.css; 'src' solo no cubre nada). Distingue mayusculas; cualquier extension de archivo vale. 3. La evidencia es 'atom-cites:<atomo> -> <ruta>' y _link_documents la cuenta como atomo para el recibo evidence-atom. 4. El mensaje del hallazgo missing_changed_file_link agrega, literal en ingles como el resto: 'Accepted links: an atom declared in the task's atoms or references whose provenance or text cites this path (or a directory containing it), a graph edge from the file to an atom, or a materialization whose target_identity is the file; a routed follow-up is a task:<id>, issue:<id> or desk/tasks|desk/drawer .md path in references.' 5. Tests: atomo declarado que cita .tsx/.css/directorio enlaza todo; atomo citado por ruta en references tambien; directorio citado cubre archivos; atomo no declarado o que cita solo prefijos parecidos no enlaza y el mensaje nombra las formas aceptadas.

## Validation

_List the checks required before this task can close._

- pytest tests/test_closeout_atom_cites_file.py

## Done When

_Name the observable condition that makes the task complete._

pytest tests/test_closeout_atom_cites_file.py y tests/test_closeout*.py pasan, y closeout verify de una tarea de UI con un atomo declarado que cita sus archivos da atom|materialization.
