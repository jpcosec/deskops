## REFORMULACION

WS48 es un nodo de implementación en `graph_ui` cuyo propósito es producir un punto único de admisión para toda escritura de la UI en modo manual exclusivo, antes de invocar cualquier canal. El resultado esperado es un módulo común más pruebas que cubran `POST /api/desk/advance`: rechazo en servidor antes de `advance_task` si falta afirmación vigente, hay evidencia contraria o falla la consulta, con estado y mensaje del botón. Repo: `graph_ui`; `output_scope`: `frontends/mindmap/` y `tests/`. Límites: no crea identidad, autenticación, lock, CAS universal ni operación nueva de lifecycle; no habilita uso real de mutaciones, que queda sujeto a gates.

## AMBIGUEDADES

1. «consultas públicas existentes para la evidencia contraria» y «la herramienta de evidencia ausente o con error»: no se nombran las consultas ni la herramienta. El ejecutor tendría que inventar cuáles son y qué resultado cuenta como evidencia contraria; no se declara que WS12 §5.9 produzca ese inventario.

2. «rechazo en el servidor antes de advance_task» frente a `output_scope: frontends/mindmap/ (módulo común de admisión de escritura; archivo exacto en el TaskDoc); tests/`: no se declara dónde vive el handler de `POST /api/desk/advance`. Si está fuera de ese scope, el ejecutor debe inventar si puede modificarlo o si excede el alcance.

3. «toda ruta de escritura de la UI, existente o nueva, consulta antes de invocar su canal» frente a una aceptación que solo prueba `POST /api/desk/advance` y los consumidores listados: no queda claro si deben migrarse ahora otras rutas existentes no enumeradas; obligaría a inventar el universo de rutas.

## DRY-RUN

Lecturas hipotéticas: contrato WS12 y sus secciones 5/5.9; ruta `POST /api/desk/advance` y `views/workflow/deskops/deskops-view.js`; consultas públicas de evidencia; pruebas existentes; configuración de ejemplo sin valores reales. Cambios previstos: módulo de admisión en `frontends/mindmap/` (archivo en TaskDoc), integración en la ruta y el botón, pruebas en `tests/` con store temporal. Dependencias: WS12 produce el contrato; `G_UI_WRITE` y `G_WRITE_CONTRACT` se evalúan por delta. Validaciones futuras: sin afirmación, rechazo servidor antes de `advance_task` y botón deshabilitado; con evidencia contraria o error, lectura/handoff con causa y buffer conservado; con admisión, conservar `revision`, gates y rechazos.

## FUTURO

WS12 produce el contrato y las condiciones de §5/5.9; el receptor P01 emite el acta de `G_UI_WRITE` del delta; WS12 produce `G_WRITE_CONTRACT`. Los consumidores listados usan el módulo sin reimplementarlo. La habilitación real de mutaciones y el acta humana dependen de WS16/`G_HUMAN_READ` y de la recepción por delta.
