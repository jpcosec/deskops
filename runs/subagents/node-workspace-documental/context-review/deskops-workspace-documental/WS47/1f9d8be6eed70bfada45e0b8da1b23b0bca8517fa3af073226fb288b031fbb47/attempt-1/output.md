## REFORMULACION
WS47 es un nodo de implementación en `sldb` que debe producir la guarda de conservación de contenido no declarado (HO-07 de WS12, 6.7), distinta de la precondición de WS45 y de la protección de campos de UI. Resultado: inventario con ruta, símbolo y commit de `refuse_structural_noise`, `refuse_undeclared_frontmatter` y la guarda de `deskops edit` (`_write_doc`), más pruebas focalizadas en el canal de edición por campos que termina en `save_document_payload`. Límites: no amplía WS45, no cambia la creación, no resuelve el gap de prevalidación del inbox de sldb, no usa workaround Deskops, y no habilita edición con contenido no declarado hasta que las pruebas pasen.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería el contrato WS12, el código de `save_document_payload`, las funciones de ruido/frontmatter no declarado, `create_document`, `track_document_file`, la guarda `_write_doc` de deskops y pruebas existentes. Cambios previstos: un inventario verificable y, solo tras el recibo `G_SLDB_WRITE` de este delta, la guarda en `src/sldb/api/documents/` o `src/sldb/cli/serve/` y pruebas en `tests/`. Dependencias: WS12 y los gates `G_SLDB_WRITE` y `G_WRITE_CONTRACT`, pendientes e intencionales. Validaciones futuras: rechazo observable sin cambios cuando un update con `expected` vigente perdería contenido no declarado; aplicación de un update seguro, incluido documento limpio; 409 con `expected` obsoleto; creación sin cambios; declaración explícita de pérdidas detectadas, no detectadas y casos deshabilitados, sin merge ni restauración. No se ejecuta nada.

## FUTURO
WS12 debe publicar el contrato y el canal elegido; el receptor humano P01 produce el acta `G_SLDB_WRITE` por delta; WS12 verifica `G_WRITE_CONTRACT` por efecto. WS19.1, WS19.2 y WS26.1 consumirán la guarda solo cuando pase. La coordinación con el gap de prevalidación del inbox de sldb corresponde a su dueño, no a este nodo.
