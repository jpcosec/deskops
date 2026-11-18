## REFORMULACION

Nodo ejecutable `task.code` (no agregado). Propósito: corregir el despacho automático de deskops tras su primera corrida real. Resultado: `dispatch.reap` localiza y borra agentes aunque el TaskDoc ya no exista; el prompt del ejecutor exige commit con rutas nombradas y trailer `Task-Id`; el prompt del tester limita la ejecución a los tests de los archivos tocados y deja informe con veredicto. Repo: deskops (cwd), con rutas `deskops/dispatch.py`, `deskops/runtime/scion.py`, `tests/`, `docs/operator-manual.md`, `CHANGELOG`. Límites: no cambiar la cola ni integrate; mantener el resto de `reap` (criterio de terminado, stop, delete, rc 4, errores por agente).

## AMBIGUEDADES

1. “Los tests a correr son los archivos tests/*.py de ese commit, más tests/test_<módulo>.py cuando exista para cada módulo de código tocado; de a uno, con TMPDIR=/tmp”. “De a uno” no define si es un archivo por proceso, un test por proceso, ni el orden/comando exacto; obligaría a inventar la invocación.
2. “Si un stop o un delete de scion falla, imprime '<nombre> <rol> error:<código>' y sigue con el siguiente agente; ese caso también da rc distinto de 0”. No fija el código concreto; obligaría a inventarlo.
3. “El resto de reap no cambia: mismo criterio de terminado (phase, activity, result-summary.md)”. No detalla valores ni combinaciones; sin leer el código, obligaría a inventar la condición exacta.
4. “commit de código con rutas nombradas” frente a “docs/operator-manual.md ... y CHANGELOG”: no aclara si esos archivos entran en el mismo commit del ejecutor; obligaría a decidir alcance del commit.

## DRY-RUN

Lecturas hipotéticas: TaskDoc, `dispatch.py` (`reap`), `runtime/scion.py`, generación de `prompt.md` por rol, `tests/test_dispatch.py`, fixtures de scion simulado, manual y CHANGELOG. Cambios previstos: test fallido de reap sin TaskDoc; sustituir etiqueta por `_scion_task_label(task_id)`; textos de prompt executor/tester; tests de prompts; documentación y CHANGELOG. Dependencias: API/CLI simulada de scion, helpers de tests, cola e integrate fuera de alcance. Validaciones futuras: `TMPDIR=/dev/shm python -m pytest -q tests/test_dispatch.py`; suite completa por integrate.

## FUTURO

El implementador ejecutará p1–p4 y entregará commit con `Task-Id`. Integrate correrá la suite completa en el host. Un humano o nodo de revisión decidirá aceptación de docs/CHANGELOG y del alcance exacto del commit.
