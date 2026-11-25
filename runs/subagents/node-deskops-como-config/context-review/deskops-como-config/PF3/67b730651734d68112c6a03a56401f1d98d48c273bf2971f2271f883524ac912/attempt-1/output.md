## REFORMULACION
PF3 es un nodo agregado, no ejecutable, del plan `deskops-como-config`; repo dueño: deskops. Propósito: que las lecturas de UI y las escrituras de deskops pasen por sldb. Resultado: vistas como `ViewDoc` servidas por `sldb serve` y toda escritura por la transacción de sldb. Límites: no cambia el formato del desk ni la gramática del CLI; no escribe en sldb; no suple reglas con Python; no toca P4; cada superficie borra su código viejo en el mismo paso. No se promueve: termina cuando terminan sus hijos CC34 y CC35.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
No se ejecuta nada. Al ser agregado, se cumple por sus hijos. CC34 captura primero los goldens JSON de `view board|task|drawer|inbox`, crea las `ViewDoc` semilla, sustituye `desk_view.py` por `sldb.api.run_view` y adapta graph_ui a `GET /views` con ETag; transfiere el contrato de vistas y la ausencia de `DeskView`. CC35, también agregado, se cumple por CC35a-d: transacción, selectores, referencias entrantes y tags/reemplazo; transfiere escrituras sin `doc_io.DocTransaction` ni selectores propios. Validación conjunta: grep vacío de `desk_view|DeskView` y `doc_io|DocTransaction`; `deskops view board` JSON igual al golden capturado, salvo `revision`; `GET /views/board` de `sldb serve` con el mismo payload; graph_ui sirve board leyendo de sldb y un ETag viejo da 409; tests reescritos, `doctor` en los 6 desks y suite integrada por el supervisor.

## FUTURO
CC33 produce recibos de evidencia y reglas de cierre; CC36, plantillas y scaffold. sldb debe satisfacer `G_GD25`/`G_GD21` para CC34 y `G_GD22`-`G_GD24`/`G_GD27` para CC35; H1-H3 quedan pendientes por DO7. El supervisor fija worktree, corre la suite integrada y decide la promoción; el TaskDoc fijará nombres exactos de archivos y tests.
