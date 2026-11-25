# REFORMULACION

Encargo: corregir que, tras `deskops edit task <id> goal`, `desk/tasks/Board.md` conserva el goal viejo. Propósito: reproducir el fallo en un desk real y arreglarlo. Resultado esperado: la línea de la tarea en Task Details del Board muestra el valor nuevo, o existe un verbo deskops que refresque el Board; más test de regresión. Superficie: `deskops/services/tasks.py`, `deskops/models/board.py` (composición `task_summaries`), `deskops edit`. Límites: no editar `Board.md` a mano ni reimplementar la vista del tablero (es de sldb, CC34). Validación: pytest del test nuevo y `tests/test_cli.py`; commit con rutas y `Task-Id`; reproducción en `runs/subagents/20261119-repro-board-goal/repro.md`.

# AMBIGUEDADES

1. «Reproducir en un desk real» — no se indica ruta, workspace ni instancia; obligaría a inventar cuál es el desk real.
2. «o hay un verbo de deskops que refresca el Board» — dos criterios de aceptación alternativos; obligaría a elegir uno sin autoridad.
3. «deskops/models/board.py:16-21» y «alrededor de las líneas 118 y 219» — referencias imprecisas; obligaría a fijar líneas exactas por inspección.
4. «p1: test que falla antes en tests/» — no nombra fichero de test; obligaría a inventar su nombre/ruta.
5. «status lo cambian advance y closeout; si ya refrescan el Board» — no aclara si status/title entran en el alcance o solo se comprueban; obligaría a decidir alcance.
6. «La vista del tablero es de sldb (CC34)» — no indica si el repo/código sldb está disponible ni cómo validar el re-render; obligaría a asumir disponibilidad.
7. `summary` vacío, `references` y `depends_on` vacíos pese a citar inbox y `repro.md`; obligaría a inventar trazabilidad.

# DRY-RUN

Lecturas: `deskops/models/board.py` (16-21), `deskops/services/tasks.py` (~118, ~219), `deskops` CLI edit, `tests/test_cli.py`, `runs/subagents/20261119-repro-board-goal/repro.md`. Cambios previstos: nuevo test en `tests/` con desk temporal en `tmp_path` (add con goal viejo, edit a nuevo, leer Board); en `services/tasks.py`, re-guardar el Board tras `edit task` sobre campos de `task_summaries` por la vía de `add task`; CHANGELOG; commit. Dependencias: render de sldb, desk de prueba, líneas exactas. Validaciones futuras: los dos pytest listados en Validation.

# FUTURO

Decisión humana/integrador: elegir entre corregir el refresco del Board o añadir verbo explícito; confirmar alcance de title/status; aportar reproducción del integrador; verificar líneas reales del código.
