## REFORMULACION
WS14 es un nodo de implementación en `graph_ui` para integrar búsqueda navegable del workspace. El resultado esperado es una UI que busque mediante `sldb find` o la ruta de `sldb serve`, sin parser propio, abra resultados con identidad y ruta de origen, conserve consulta y foco al volver, y distinga tres estados: sin resultados, error de backend y degradación parcial declarada. Límites: usar solo texto, campos y semántica de la API real; respetar auditoría WS03 y contrato WS11; no cargar el grafo completo en cada tecla. Salidas previstas en `frontends/mindmap/source/`, `views/workspace/` y `tests/`.

## AMBIGUEDADES
ninguna

## DRY-RUN
Lecturas previstas: contrato WS11, `auditoria/infraestructura.md` de WS03, salidas de WS13, API disponible de `sldb` y pruebas existentes. Cambios previstos: implementar búsqueda y navegación en `graph_ui`; mapear resultados a documento/ruta; conservar consulta y foco con teclado; modelar los tres estados; añadir prueba de peticiones que demuestre que teclear no dispara carga completa del grafo. Dependencias: WS13 completo como agregado, WS11/WS03 como prerrequisitos transitivos y recibo `G_UI_READ` por delta. Validaciones futuras: recorrido de teclado buscar-abrir-volver; casos sin resultados, error y degradado; inspección de peticiones; uso de store temporal o corpus WS40; el TaskDoc de promoción fijará mecanismo, archivos y textos.

## FUTURO
WS11 publica el contrato de navegación/búsqueda; WS03 entrega la auditoría de infraestructura; WS13 entrega lector, historia y foco; el humano P01 emite el recibo `G_UI_READ` del delta WS14; el TaskDoc de promoción fija archivos, textos y escenarios; WS16 validará lectura/descubrimiento con humano y medirá tiempos.
