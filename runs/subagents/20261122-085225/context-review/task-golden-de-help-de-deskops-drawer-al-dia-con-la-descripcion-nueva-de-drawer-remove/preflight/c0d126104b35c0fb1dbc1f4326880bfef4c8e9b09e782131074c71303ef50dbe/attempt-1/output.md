REFORMULACION
Nodo ejecutable (`task.code`), no agregado. Propósito: poner al día el golden de ayuda del grupo `drawer` con la descripción nueva del subcomando `drawer remove`, desbloqueando los integrates de deskops. Resultado: `tests/fixtures/golden/help/deskops_drawer.txt` coincide con `deskops drawer --help` a `COLUMNS=80`, y existe un commit que solo toca ese archivo, con `Task-Id` en el cuerpo. Repo: deskops, en el worktree que proporcione dispatch. Límites: dentro, solo ese golden; fuera, el código de drawer, cualquier otro golden y la suite completa (la corre integrate).

AMBIGUEDADES
1. «se revierten y se explica por qué»: no indica dónde se registra esa explicación (¿commit, informe, comentario?). Obligaría a inventar el canal y formato.
2. «con COLUMNS=80» frente a «python -m pytest … --update-golden»: no aclara si hay que exportar `COLUMNS=80` manualmente o si el test ya lo fija. Obligaría a inventar el entorno de ejecución.
3. «commit desde el worktree que dispatch te da»: no fija rama base ni política de firma/autoria. Obligaría a inventar condiciones de commit no declaradas.

DRY-RUN
Lecturas: TaskDoc, `tests/test_output_goldens.py`, golden actual `help/deskops_drawer.txt`, `git status` y ayuda real de `deskops drawer`. Cambios previstos: ejecutar pytest con `--update-golden`; revisar qué archivos cambiaron; revertir los goldens ajenos; repetir el test sin actualizar; commitear únicamente el golden objetivo con el trailer. Dependencias: Python/pytest disponibles, worktree asignado por dispatch, mecanismo `--update-golden` operativo. Validaciones futuras: `pytest tests/test_output_goldens.py` en verde y comprobar que el commit solo contiene `deskops_drawer.txt`. Nada se ejecuta aquí.

FUTURO
Dispatch entrega el worktree y el id de tarea. El nodo integrate ejecutará la suite completa. Si `--update-golden` modifica otros goldens, un humano decide si la explicación aportada es suficiente; el integrador solo verifica el resultado conjunto.
