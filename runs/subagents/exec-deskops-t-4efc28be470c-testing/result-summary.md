FALLA

# Resultado del tester

Tarea: task-la-skill-el-ritual-drawer-triage-y-la-ayuda-de-promote-dicen-que-una-nota-del-inbox-que-es-trabajo-s
Run: run-deskops-t-4efc28be470c
Commit evaluado: 812f6115aba165fee9c4050c2dcb179da57cbf0d ("docs: inbox notes that are work become tasks with references, not drawer promotions", trailer Task-Id correcto).

## Veredicto

El commit cumple el Goal para las superficies que tocó y los tests pasan, pero **no cumple el Done When**:
el grep de validación no muestra solo advertencias. Quedan menciones que siguen mandando notas del
inbox al drawer, sin advertencia, en `docs/faq.md` y `docs/deskops-ui.md`.

## Evidencia del fallo de aceptación

En un árbol limpio del commit (`git archive 812f6115` en `/tmp/deskops-test-812f`):

```text
$ grep -rn 'inbox-to-drawer' .claude docs desk/rituals
.claude/skills/...                -> advertencias (correctas)
docs/operator-manual.md:444       -> advertencia (correcta)
docs/operator-manual.md:448,468   -> ejemplos runnable de la mecánica (permitidos por "se conservan los ejemplos que sigan siendo correctos")
docs/operator-manual.md:1505      -> advertencia (correcta)
docs/deskops-ui.md:237            -> "Inbox: Pasar a drawer | promote inbox-to-drawer-task" (sin advertencia)
docs/faq.md:53                    -> "deskops promote — move inbox notes into loose drawer candidates" (sin advertencia)
docs/faq.md:116,121               -> recomiendan "Promote inbox notes" (sin advertencia)
```

El Implementation Path pedía `grep -rn 'inbox-to-drawer' .claude docs ...` y reescribir cada mención
(salvo ejemplos que sigan siendo correctos). Las menciones de `docs/faq.md` describen promote como el
camino para notas del inbox y no son meros ejemplos de mecánica. `docs/deskops-ui.md` mantiene la
acción "Inbox: Pasar a drawer". El Done When dice literalmente: "El grep solo muestra advertencias".

## Lo que sí está bien

- `desk/rituals/ritual-drawer-triage.md` tiene el paso 1 exacto pedido ("Capture repo-local deferred
  work directly in desk/drawer/tasks/. Inbox notes that are work become tasks with references to the
  note and then message ack; they do not go to the drawer."). El cambio está en el árbol del commit
  porque fue arrastrado por 624f5882, no en el diff propio de 812f6115.
- `.claude/skills/deskops-workflow/SKILL.md`, `references/vocabulary.md` y `references/deskops-cli.md`
  describen el camino add task + references + message ack y advierten que promote borra la nota.
- El help de `deskops promote inbox-to-drawer-task` en `deskops/cli/registry.py` advierte que borra la
  nota de origen y que no es el camino para notas que son trabajo.
- `docs/operator-manual.md` añade la advertencia y conserva ejemplos runnable de la mecánica.

## Tests ejecutados (de a uno, sobre el árbol limpio del commit)

Python del contenedor: el `.venv` del checkout apunta a Python 3.12, ausente aquí; usé
`/dev/shm/t311/bin/python` (3.11) con `PYTHONPATH=/tmp/deskops-test-812f:/mnt/ssd/proyectos/SLDB_1/sldb/src`.

```text
TMPDIR=/tmp .../python -m pytest -q tests/test_skill_cli_drift.py       -> 2 passed
TMPDIR=/tmp .../python -m pytest -q tests/test_output_goldens.py       -> 7 passed (392.97 s)
TMPDIR=/tmp .../python -m pytest -q tests/test_operator_manual.py      -> 1 passed (199.39 s)
TMPDIR=/tmp .../python -m pytest -q tests/test_command_registry.py     -> 3 passed
TMPDIR=/tmp .../python -m pytest -q tests/test_registry_robustness.py  -> 8 passed (30.84 s)
```

No se corrió la suite completa (la corre integrate en el host). El commit no añade archivos
`tests/*.py`; añadí los tests de los módulos de código tocados (`deskops/cli/registry.py`).

## Acción sugerida para el ejecutor

Reescribir las menciones restantes de `docs/faq.md` (y decidir/actualizar la fila de
`docs/deskops-ui.md`) con el mismo texto canónico, o que el coordinador acote expresamente el
Done When a las superficies del Goal. Mientras el criterio siga diciendo "el grep solo muestra
advertencias", la tarea no puede cerrarse.

## Datos del run

- Task id: task-la-skill-el-ritual-drawer-triage-y-la-ayuda-de-promote-dicen-que-una-nota-del-inbox-que-es-trabajo-s
- Role: tester
- Run id: run-deskops-t-4efc28be470c
- Session path / sha256: no registrados por el runtime para este run (el coordinador los completa al recoger).
- Snapshots: board.txt, task.txt, next.txt, graph.txt, git-status.txt en este run_dir. `graph missing` sale 1 por hallazgos preexistentes de otras tareas; no hay hallazgo nuevo atribuible a este commit.
