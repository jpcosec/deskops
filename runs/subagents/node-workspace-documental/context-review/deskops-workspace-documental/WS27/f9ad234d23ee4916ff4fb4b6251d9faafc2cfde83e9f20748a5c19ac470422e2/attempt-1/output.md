## REFORMULACION
WS27 es un **agregado no ejecutable** de `graph_ui` cuya finalidad es integrar la revisión de cambios y evidencia junto a la TaskDoc. Su resultado no es una ejecución propia, sino la suma de: (a) diff Git e historial read-only por repo y tarea, y (b) evidencia declarada, encontrada y verificada. Repo dueño: `graph_ui`. Límites: no escribe ni revierte; el diff se acota a `TaskDoc.references`/`TaskDoc.files` y a repos resolubles por WS11; la evidencia no crea modelo de comentarios ni infiere tipos por extensión; abrir soporte fuera de Markdown del workspace se declara no soportado. Depende de WS13 y WS12, y termina cuando terminan WS27.1 y WS27.2; sus dependientes siguen colgando de WS27.

## AMBIGUEDADES
ninguna

## DRY-RUN
No hay dry-run ejecutable para WS27: es agregado y no se ejecuta. Hipotéticamente, un ejecutor futuro recorrería sus hijos:

- **WS27.1**: leería el contrato WS11 de rutas/aliases, WS12, y los campos `TaskDoc.references`/`TaskDoc.files`; produciría vista de diff e historial read-only por repo/tarea, con repo raíz explícito y “no disponible” si la ruta no resuelve. Cambios previstos en `views/workspace/diff/` y tests. No escribiría ni revertiría.
- **WS27.2**: leería `closeout_evidence`, references/files y salida de `deskops closeout verify`; mostraría declarada/encontrada/verificada como estados distintos y abriría soporte Markdown en el lector WS13 o declararía no soportado. Cambios en `views/workspace/evidence/` y tests.

Dependencias: WS13 y WS12 como prerrequisitos; WS27 espera la aceptación conjunta de ambos hijos. Validaciones futuras: aceptación de WS27.1 y WS27.2, pruebas de sus vistas y recibos `G_UI_READ` por delta de los hijos; el agregado no añade efecto propio.

## FUTURO
WS27.1 y WS27.2 producen las vistas y pruebas; el receptor P01 emite los recibos `G_UI_READ` por delta. WS28 y WS35 consumen el agregado cuando esté completo. WS29 aporta hallazgos de integridad del store, fuera de este nodo.
