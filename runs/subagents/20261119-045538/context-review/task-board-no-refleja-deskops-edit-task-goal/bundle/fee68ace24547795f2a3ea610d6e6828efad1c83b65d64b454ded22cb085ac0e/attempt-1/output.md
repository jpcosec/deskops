## REFORMULACION

Encargo: corregir en el repo deskops (cwd `/mnt/ssd/proyectos/SLDB_1/deskops`) el bug por el que `deskops edit task <id> goal` actualiza la tarea pero `desk/tasks/Board.md` conserva el goal viejo. Resultado esperado: un test que falle antes y pase después, verificando que la línea de Task Details del Board muestra el goal nuevo (y análogamente title), más CHANGELOG y commit. Límites: tocar `deskops/services/tasks.py`, `deskops/models/board.py` y `deskops edit`; no editar `Board.md` a mano ni reimplementar la vista del tablero (sldb, CC34). La validación son dos comandos pytest.

## AMBIGUEDADES

1. «Reproducir en un desk real» — no se define qué desk ni ruta; obligaría a inventar el entorno de reproducción.
2. «el test nuevo» — no se nombra archivo ni caso; obligaría a inventar nombre y ubicación.
3. «alrededor de las líneas 118 y 219» — rango impreciso; obligaría a inventar el punto exacto de guardado.
4. «por la misma vía con que add task lo guarda» — no se explicita la función/API; obligaría a inventar el mecanismo de persistencia.
5. «la línea de la tarea en Task Details» — no se fija formato exacto de la línea; obligaría a inventar el criterio de aserción.
6. «status lo cambian advance y closeout» — no se aclara si esos verbos entran en el test o solo se documentan; obligaría a inventar cobertura.

## DRY-RUN

Lecturas: `deskops/services/tasks.py` (flujo add/edit), `deskops/models/board.py:16-21` (composición task_summaries), `deskops edit`, tests existentes, `tests/test_cli.py`, `runs/subagents/20261119-repro-board-goal/repro.md`. Cambios previstos: test de regresión con desk en `tmp_path` (add goal «viejo», edit goal «nuevo», assert Board); re-guardado del Board tras editar campos de la composición; CHANGELOG. Dependencias: helpers de guardado de `services/tasks.py`, render de sldb no modificable. Validaciones futuras: pytest del test nuevo y `tests/test_cli.py`. Sin ejecutar nada.

## FUTURO

Otro nodo (ejecutor) produce el test, el parche y el CHANGELOG. El integrador aporta la reproducción en `runs/subagents/20261119-repro-board-goal/repro.md`. Un humano decide el commit final (rutas y Task-Id) y acepta el cierre.
