## REFORMULACION

Propósito: corregir que `deskops view task --format json` entregue `holds: true` en un gate (`task_activates -> ritual-testing`) que a la vez trae un finding de nivel error de `rules/rule-activation-task-code`, de modo que `holds` sea `false` cuando la regla de activación del gate produce un finding de error. Resultado: reproducción registrada, causa localizada, cambio en el cálculo de `holds`/findings de `show_task` y `view`, y un test que falla antes y pasa después en `tests/test_view.py`. Repo/superficie: `deskops/cli/commands/view.py` (`_gates`, `show_task`) y `tests/test_view.py`; si la causa está en sldb, se rutea con mensaje y queda un test `xfail strict`. Límites: fuera la UI de graph_ui y el texto de los findings; el nodo es una tarea ejecutable (`task.debug`), no un agregado.

## AMBIGUEDADES

1. "se manda deskops message send --to sldb con la reproduccion minima": no se define destinatario válido, formato ni contenido del mensaje; obligaría a inventar el contrato de mensajería.
2. "hacer que coincidan" frente a "dejar que holds sea false cuando la regla de activacion del gate da un finding de nivel error": no queda claro si solo se ajusta `holds` o también qué findings se muestran; obligaría a elegir una dirección.
3. "rules/rule-activation-task-code" y "task_activates -> ritual-testing": no están en los archivos provistos; obligaría a inventar dónde vive esa regla y qué códigos cuentan como error.
4. "una tarea task.code sin recibos de preflight": no se define qué recibo ni cómo construir el caso; el TaskDoc usa `task_type: task.debug`.
5. "deskops review record <tarea> --kind reproduction": sin esquema de argumentos ni evidencia esperada.

## DRY-RUN

Lecturas: `show_task` y `_gates` en `view.py`, evaluación de regla en sldb, `lifecycle.transitions_from`, `tests/test_view.py` y `tests/view_desk.py`; desk sandbox en `tmp_path` según átomo de sandbox. Cambios previstos: derivar `holds` de la presencia de findings de nivel error en la regla de activación y añadir test comparativo en `tests/test_view.py`. Dependencias: `DeskopsOperations.show_task`, `run_view`/`project`, fixture `view_desk`. Validación futura: `pytest -q tests/test_view.py` con el comando dado. Nada ejecutado.

## FUTURO

Decide un humano si la causa se rutea a sldb y con qué texto; otro nodo ejecuta el commit descriptivo y el cierre; el revisor acepta la vía `xfail strict` o exige corrección local.
