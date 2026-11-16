## REFORMULACION

Encargo ejecutable (task.code) en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`: modificar `deskops/graph/checks.py` (construcción de listas missing/informational; `MISSING_TARGET_KINDS`), la salida de `deskops graph missing` en `deskops/cli/commands/graph.py`, y cubrir con tests en `tests/test_graph_checks.py`. Resultado observable: cuando el origen de un `missing_declared_target` es un TaskDoc abierto (`status` distinto de closed, superseded, cancelled, retired) y el destino es source_file, test_file o doc inexistente, se reporta como informational con código `planned_target`, separado de missing; desde documentos no-tarea sigue siendo missing; la salida cuenta cada tipo. Límites: no tocar `SOURCE_PATH` ni el extractor, no ocultar los `planned_target`.

## AMBIGUEDADES

1. "el destino es un source_file, test_file o doc inexistente" — no define cómo distinguir un archivo planificado de una ruta mal escrita o ya borrada en una tarea abierta (`deskops/specs/loader.py`). Obligaría a inventar un criterio (p.ej. lista blanca, heurística por nombre) no presente en el input.
2. "La salida dice cuantos son de cada tipo" — no fija formato ni etiquetas. Obligaría a inventar el texto/estructura exacta de la salida y su verificación.
3. Línea de validación con forma de dict: `{'cd ... pytest -n 4 -q tests ...': 'cada test que falle se corre ...'}` — el comando y su criterio están fusionados. Obligaría a inventar si el segundo texto es condición, nota o comando aparte.
4. "una tarea cerrada (en history) no aplica porque ya no esta en desk/tasks" — asume el mecanismo sin verificarlo. Obligaría a decidir si se testea o se omite.

## DRY-RUN

Lecturas futuras: `checks.py`, `cli/commands/graph.py`, `tests/test_graph_checks.py`, `tests/test_graph_cli.py` y TaskDocs de `desk/tasks`. Cambios previstos: rama de clasificación por estado del TaskDoc origen; constante/código `planned_target`; conteo por tipo en la salida; dos o tres tests nuevos (tarea draft → informational; átomo → missing). Dependencias: parser de frontmatter y estados vigentes. Validaciones futuras: los tres pytest de Validación y `deskops graph missing --root .`; suite completa `-n 4` con triaje de fallas contra `origin/main` en worktree limpio.

## FUTURO

Un ejecutor implementa y entrega informe de fallas preexistentes; un humano decide el formato de salida y el criterio planificado-vs-error de la ambigüedad 1.
