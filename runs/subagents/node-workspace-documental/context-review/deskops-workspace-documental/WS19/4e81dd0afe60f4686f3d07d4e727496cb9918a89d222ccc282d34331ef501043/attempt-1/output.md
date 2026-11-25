## REFORMULACION
WS19 es un agregado de implementación en `graph_ui`: integrar edición de campos con conflicto visible y alta/baja de relaciones permitidas por contrato sobre el workspace integrado `a1b2b22`, reutilizando editores y API reales, con la precondición de escritura que fije WS12/verifique WS45, sin crear semántica de relaciones en el componente y sin editar workflow-protected fields por ese canal. Resultado: salidas de WS19.1 y WS19.2. Límites: agregado no ejecutable; G_HUMAN_READ solo habilita uso de mutaciones en UI, no desarrollo ni pruebas aisladas de API.

## AMBIGUEDADES
Ninguna. La aceptación remite a los hijos y las expresiones «precondición de escritura (WS45/WS12)», «workflow-protected fields» y «relaciones permitidas por contrato» tienen productor/contrato nombrado; archivos, textos y pruebas quedan al TaskDoc de promoción. Que `depends_on` incluya WS19.1/WS19.2 es coherente con la regla del agregado: termina cuando terminan sus hijos.

## DRY-RUN
WS19 no se ejecuta: es agregado. Un ejecutor futuro leería `dag.yaml` —WS19, hijos, aristas WS12/WS19.1/WS19.2 y gates—. WS19.1 produciría edición de campos en `frontends/mindmap/views/workspace/fields/` y tests, consumiendo endpoints WS12. WS19.2 produciría relaciones en `.../relations/` y tests. Ambos esperan WS12 (contrato), WS47 (guarda de contenido) y WS48 (admisión de escritura), y sus gates por delta: G_PAYLOAD_PRECONDITION (WS45), G_UI_WRITE/G_WRITE_CONTRACT con recibo propio, y G_HUMAN_READ antes de usar mutaciones UI. WS19 no transfiere artefacto propio: sus hijos aportan sus salidas al agregado; WS21/WS42 podrán consumir WS19 cuando ambos cumplan. Validación conjunta: aceptación de WS19.1 y WS19.2, sin exigir aceptación conjunta de gates de otros deltas.

## FUTURO
P01/receptor de `graph_ui` emite actas G_UI_WRITE por delta; WS16 produce el acta G_HUMAN_READ; WS45 evidencia G_PAYLOAD_PRECONDITION; WS12 publica el contrato, y WS47/WS48 sus guardas y admisión. No se inventa aprobación de implementación, API ni Scion.
