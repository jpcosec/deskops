## REFORMULACION
Nodo ejecutable, no agregado. Propósito: evitar que un closeout publique en `.sldb/store.yaml` un RunDoc cuyo `run.md` aún no está versionado, lo que rompe `sldb stores build` en clones limpios. Resultado: todo `deskops closeout commit` incluye los `run.md` registrados por el store, existentes en disco y ausentes del índice y de HEAD. Repo: `deskops`. Límites: solo `deskops/services/closure.py` y `tests/test_closeout.py`; fuera el runtime template, otros archivos del run dir y la CI de `graph_ui`.

## AMBIGUEDADES
1. «Todo commit que hace deskops closeout commit (en cualquier modo)»: no define qué modos abarca. ¿Incluye `--no-run`, `supersede` y `retire`, o solo `--run-dir`? Obliga a inventar alcance y cobertura de tests.
2. «listar los path de RunDoc de .sldb/store.yaml»: no se entrega el esquema del store ni el nombre del campo de ruta. Obliga a inventar cómo leer los registros y resolver rutas relativas.
3. «git clone del sandbox + sldb stores build da rc 0»: la sección Validation solo ordena ejecutar pytest. Obliga a inventar si el test invoca el CLI real `sldb`, cómo lo instala y si es dependencia del entorno.

## DRY-RUN
Leería `deskops/services/closure.py` para ubicar el armado de rutas y el `git add` de `.sldb`; `tests/test_closeout.py` para seguir el patrón de sandbox; y el formato de `.sldb/store.yaml` disponible en fixtures o código. Cambios previstos: un helper que extraiga rutas `run.md` del store, filtre las existentes en disco y ausentes del índice y de HEAD, y las sume a las rutas del commit en los modos acordados. Test en `tmp_path`: dos RunDoc registrados, uno de la tarea y otro de otra corrida con `run.md` sin commitear; tras closeout, ese archivo debe estar en HEAD. Dependencias: git, PyYAML y, si se prueba el clon, el CLI `sldb`. Validación futura: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py`. Sin ejecutar.

## FUTURO
Un nodo ejecutor posterior producirá el diff y el commit descriptivo. La CI o un nodo de validación ejecutará pytest y, si corresponde, el clon limpio con `sldb stores build`. Un humano decidirá el alcance de «cualquier modo» y si `sldb stores build` se prueba dentro del test o fuera.
