## REFORMULACION

**Propósito:** eliminar de README y docs las menciones obsoletas a `spec/artifacts`, `spec/fields` y `SpecRegistry`, borrados en CC30.

**Resultado:** reescribir esas menciones para que remitan a atributos de clase de `deskops/models` y a `deskops/doc_access.py`; el grep de validación debe quedar vacío y debe pasar `test_operator_manual.py`.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`.

**Límites:** entran `README.md`, `docs/knowledge-graph/desk-source-graph-vocabulary.md`, `docs/diagrams/process/current-agent-workflow-and-automation.md` y su `.mmd`, más cualquier otro archivo que muestre el grep. No se reescriben los diagramas ni se migran a specir. El `.mmd` se edita junto con su `.md` y el commit indica que no tiene spec fuente porque spec2viz se archiva (`80d32903`). Es una tarea ejecutable `task.docs`, no un agregado.

## AMBIGUEDADES

1. «cualquier otro que muestre el grep» frente a un grep limitado a `README.md docs/`: obliga a inventar si el alcance incluye archivos del repo fuera de `README.md` y `docs/`.
2. «Esos archivos remiten a los atributos de clase de los modelos (deskops/models) y a deskops/doc_access.py»: no asigna reemplazo por mención; obliga a inventar qué destino exacto corresponde a cada línea.
3. «los tests de docs» frente a la validación concreta `test_operator_manual.py`: obliga a inventar si existen otros tests de docs que deban ejecutarse.
4. «el commit lo dice»: no fija texto ni ubicación; obliga a inventar la redacción exacta de esa afirmación.

## DRY-RUN

Lecturas previstas: el TaskDoc, los cuatro archivos citados, la salida del grep, `deskops/models`, `deskops/doc_access.py` y `tests/test_operator_manual.py`. Cambios previstos: sustituir cada mención obsoleta por la referencia correspondiente. Dependencias: repo disponible, `grep`, entorno `TMPDIR=/dev/shm`, `.venv` y pytest. Validaciones futuras: ejecutar el grep indicado y `pytest -q tests/test_operator_manual.py`. Sin ejecutar nada.

## FUTURO

El ejecutor futuro produce el diff, el commit y la evidencia de grep/pytest. Un revisor humano aprueba el cambio y decide si aparecen coincidencias fuera de `README.md`/`docs/`. La decisión sobre spec2viz o una eventual migración a specir queda fuera de este nodo.
