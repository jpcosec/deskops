REFORMULACION

WS15.2 es un nodo atómico de implementación en `graph_ui`. Su encargo es cubrir UF10: ante un proyecto sin desk, la UI muestra orientación, la ruta absoluta del proyecto como destino y el comando `deskops init <ruta>`, sin inicializar nada por GET. Tras un init externo real, refrescar la lectura debe mostrar el desk real. El resultado esperado es la vista/estado de orientación y sus pruebas dentro de `frontends/mindmap/views/workspace/orientation/`, usando las rutas de lectura del contrato WS11 y `tests/`. Límites: no mutar al abrir, no inicializar desde UI y no exceder ese `output_scope`. Depende de WS13 y del gate per-delta G_UI_READ.

AMBIGUEDADES

Ninguna.

DRY-RUN

Un ejecutor futuro leería el contrato WS11, las salidas integradas de WS13, el registro de vistas del host y las pruebas existentes. También verificaría el recibo G_UI_READ correspondiente solo a WS15.2; su estado global pendiente no bloquea otros deltas.

Cambios previstos: implementar la representación de orientación en el directorio indicado, consumiendo las rutas de lectura de WS11; mostrar ruta absoluta y comando sin ejecutar init ni escribir; exponer un refresco de lectura que, tras un init externo, muestre el desk real. Añadir pruebas en `tests/`.

Dependencias: WS13 como agregado cumplido; WS11 de forma transitiva para rutas de lectura; G_UI_READ como recepción por delta.

Validaciones futuras: abrir un fixture sin desk y comprobar orientación, destino y comando, verificando ausencia de mutaciones e init por GET; ejecutar `deskops init` fuera de la UI sobre un proyecto temporal real; refrescar y comprobar que aparece el desk. Los textos exactos y escenarios detallados quedan al TaskDoc de promoción.

FUTURO

WS11 y WS13 deben entregar el contrato de lectura y el lector integrado. El solicitante P01, como receptor de `graph_ui`, emite el acta G_UI_READ del delta concreto al preparar/promover, con evidencia y commit en el repo receptor. La ejecución externa de `deskops init` durante la validación corresponde a un humano u operador, no a este nodo.
