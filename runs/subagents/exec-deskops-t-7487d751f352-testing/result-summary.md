PASA

# Resultado del tester

- task_id: task-atomos-pills-y-tareas-guardan-el-donde-como-punteros-a-un-documento-del-store-a-una-categoria-o-a-un
- role: tester
- run_id: exec-deskops-t-7487d751f352 (run-deskops-t-7487d751f352)
- commit evaluado: `9bcec7d88c1291c0e1e2311046f910e4d5c9b1ce` (`fix: pointers en AtomAdrDoc, golden de vistas y sample de átomo`)
- HEAD del árbol: `26c2f2bab` (`run: deskops-t-7487d751f352`, solo metadatos del run). El código y los tests son los de `9bcec7d88`.
- El commit no lleva trailer `Task-Id`, como pedía el intento 3.
- Entorno: `/dev/shm/tester-venv/bin/python` (3.12.16), con `PYTHONPATH=/workspace/deskops:/workspace/sldb/src`; `TMPDIR=/tmp` y `--basetemp=/tmp/pytest-deskops-t-7487d751f352*` en todo lo corrido. El `.venv` de `/workspace` está roto en este contenedor (su `python` apunta a `/usr/bin/python3` 3.11 sin pytest; su `pytest` tiene shebang a `/home/robocop/...`).

## Veredicto

PASA. El commit del intento 3 corrige exactamente lo que habían señalado los dos testers anteriores y no introduce regresiones medibles:

- `deskops/models/adr.py`: `__template__` de `AtomAdrDoc` incluye `pointers`, así que `deskops add atom --atom-type atom.adr --pointers ...` guarda y `deskops show` muestra los punteros.
- `tests/fixtures/golden/output/view_drawer.json`: el único cambio es la línea `pointers: []` en el markdown de la tarea del drawer; `test_view_goldens.py` pasa sin `--update-golden`.
- `tests/fixtures/model_contract_hashes.json`: solo cambia el hash de `AtomAdrDoc` (los demás no se tocan).
- `tests/test_atom_materialization.py`: el sample incluye `pointers: []` y el roundtrip pasa.
- `tests/test_where_pointers.py`: nuevo caso `test_adr_atom_stores_pointers`, que crea un `atom.adr`, guarda las tres clases de puntero y las comprueba con `show`.

## Tests ejecutados (de a uno, `TMPDIR=/tmp`)

| Test | Resultado |
|---|---|
| `tests/test_where_pointers.py` | **20 passed** (38.79 s) |
| `tests/test_atom_materialization.py` | **2 passed** (0.69 s) |
| `tests/test_model_contract_snapshot.py` | **2 passed** (0.68 s) |
| `tests/test_view_goldens.py` | **1 passed** (36.51 s) |
| `tests/test_adr_artifact.py` | **14 passed** (57.81 s) |
| `tests/test_output_goldens.py` | **7 passed** (455.30 s) |

No se corrió la suite completa (la corre integrate en el host). No existe `tests/test_adr.py`; para el módulo tocado `deskops/models/adr.py` el test relevante es `tests/test_adr_artifact.py`, que pasó.

## Done When comprobado a mano (desk temporal)

Un desk nuevo, con un átomo, una pill y una tarea creados con las tres clases de puntero
(`doc:TaskDoc:otra`, `tag:area:ui:graph`, `code:src/a.py::foo~2`):

- `deskops show task task-tarea-p` imprime la sección `Pointers:` con las tres líneas.
- `deskops show atom atom-atomo-p` y `deskops show pill pill-pill-p` imprimen `pointers: doc:TaskDoc:otra, tag:area:ui:graph, code:src/a.py::foo~2`.
- El frontmatter de los tres documentos guarda la lista YAML de punteros.
- `deskops edit task task-tarea-p pointers "['doc:nada']"` → rc=1 y `Invalid doc pointer 'doc:nada': expected doc:<Model>:<id>.`
- `deskops doctor --root <desk temporal>` → rc=0, "Desk is healthy. No issues found."
- Lectura de un documento viejo del workspace (`deskops show atom atom-001-self-described-store-layout --root .`) → rc=0, `pointers:` vacío.

Las formas `tag:area:ui:graph` y `code:src/a.py::foo~2` / `code:src/a.py::Clase.metodo~2` están cubiertas por `test_tag_value_with_colon_and_code_tilde_suffix` (parametrizado) y por el smoke anterior.

## Nota de entorno (no imputable al commit)

Con el Python 3.13.18 de `/workspace/sldb/.venv`, `tests/test_output_goldens.py::test_help_goldens` falla en `help/deskops_add_atom.txt` por el wrapping de argparse de 3.12 vs 3.13 en la opción `--conversation-ref, --conv` (`_unwrap_usage` solo normaliza opciones cortas). Reproduje la misma falla en un worktree aislado del padre `19077b6d3` (antes del commit evaluado) y el mismo test pasa completo con 3.12.16. Por eso lo trato como deriva del intérprete, no del cambio.

## Observaciones no bloqueantes

- El docstring de `deskops/models/adr.py` sigue diciendo "the common pointers field does not exist yet on `AtomDoc`; the day it does, `references` is what moves there". Ya es falso: `pointers` existe y esta misma tarea lo añadió a la plantilla. Conviene actualizarlo en una tarea de documentación, no bloquea el Goal.
- El árbol compartido llega con cambios previos sin commitear en `.sldb/` y en `desk/tasks/` (y archivos `ReviewDoc` sin seguimiento generados por runs en paralelo); no forman parte de `9bcec7d88` y no los imputo a este intento. El worktree temporal usado para la comprobación del padre en `/tmp` ya se eliminó.
