## REFORMULACION

Propósito: evitar que ejecutores paralelos compartan árbol de trabajo e índice, aislando cada uno en un git worktree y una rama propia, y reintegrando su commit al cierre. Resultado: `dispatch start` crea por ejecutor una rama `deskops/<agente>` desde la punta local, en `<repo>/.worktrees/<agente>` ignorado por git; el agente trabaja y commitea ahí; el tester prueba ese worktree; `integrate`/`closeout` trae el commit a la rama principal mediante cherry-pick o rebase+fast-forward y borra worktree y rama. Repo de trabajo: deskops (`dispatch.py`, `integrate.py`, tests, `docs/operator-manual.md`, CHANGELOG); el incidente en sldb es motivación. Límites: fuera scion; dentro plantilla/prompt, tests y docs. No es un agregado ni un paquete no ejecutable: es una tarea `task.code` única.

## AMBIGUEDADES

1. «una rama 'deskops/<agente>'»: no define formato de `<agente>` ni si el prefijo aplica a repos distintos de deskops; obligaría a inventar normalización y colisiones.
2. «desde la punta local del repo» y «cherry-pick sobre main local»: no fija rama base ni qué pasa si HEAD no es main; obligaría a inventar la fuente.
3. «<repo>/.worktrees/<agente>»: no dice cómo se resuelve `<repo>` con varios repos ni cómo se ignora (`.gitignore` vs `info/exclude`); obligaría a inventar mecanismo.
4. «el template de scion o el prompt» dentro, pero «Fuera: scion»: contradicción de límite; obligaría a elegir superficie.
5. «p1: diseño en el informe»: no identifica informe, formato ni ubicación; obligaría a inventar el entregable.
6. «Al cierre, integrate (o closeout)» frente a «reap borra el worktree» y «borra el worktree y la rama»: responsabilidades y casos de fallo sin asignar.
7. «commit con rutas nombradas y Task-Id»: no define convención de mensaje ni formato de Task-Id.

## DRY-RUN

Lecturas: TaskDoc, `dispatch.py` (start/reap), `integrate.py`, `tests/test_dispatch.py`, `tests/test_integrate.py`, docs/CHANGELOG y configuración de prompt/scion. Cambios previstos: diseño p1; tests p2 de dos worktrees/ramas separadas, aislamiento, reap e integración selectiva; implementación p3; docs/CHANGELOG p4; commit con rutas y Task-Id. Dependencias: dispatch paralelo existente, integrate con cherry-pick local y montaje del workspace en contenedor. Validaciones futuras: el comando pytest indicado y la suite completa por integrate. Nada ejecutado.

## FUTURO

Un humano aprueba el diseño p1 y fija convenciones ausentes. Otro nodo (`integrate`/`closeout`) corre la suite completa y materializa cherry-pick/rebase+ff y limpieza. El tester valida el worktree.
