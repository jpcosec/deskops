REFORMULACION
WS19.2 es una entrega de implementación en `graph_ui`: habilitar alta/baja de relaciones permitidas por el contrato WS12, usando API real y la precondición de escritura que ese contrato fije, sin crear semántica de relaciones en el componente. El resultado debe persistir y confirmarse tras recarga; rechazar con error visible relaciones no permitidas, revisiones obsoletas y tipos/relaciones protegidos; y borrar un RelationDoc con su índice mediante el canal público de sldb (`/save delete` con `expected`), deshabilitando y declarando la baja si el modo local solo destrackea. Límites: no habilitar mutaciones UI sin `G_HUMAN_READ`; desarrollo y pruebas API aisladas pueden avanzar. Repo: `graph_ui`; alcance: `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y `tests/`.

AMBIGUEDADES
Ninguna.

DRY-RUN
Nodo no agregado. Un ejecutor futuro leería el contrato WS12 y las salidas de WS47/WS48; revisaría la vista de relaciones existente, endpoints autorizados y pruebas. Cambiaría la UI de alta/baja para llamar al canal real y al punto de admisión de escritura, aplicaría la precondición de WS12 y, solo si el modo ofrece `/save delete` con `expected`, habilitaría la baja de RelationDoc; en modo local limitado la deshabilitaría y declararía el límite. Dependencias: WS12, WS47 y WS48; gates `G_HUMAN_READ`, `G_PAYLOAD_PRECONDITION`, `G_UI_WRITE` y `G_WRITE_CONTRACT`. Validaciones futuras: alta/baja persisten tras recarga; relación no permitida, revisión obsoleta y protegidos se rechazan visiblemente; borrado de RelationDoc elimina documento e índice y no reaparece; modo local declara límite; quitar referencia de campo queda fuera y con prueba propia. Sin ejecutar nada.

FUTURO
WS12 produce el contrato y la precondición; WS47 la guarda de contenido; WS48 la admisión de escritura de UI. WS45 verifica `G_PAYLOAD_PRECONDITION`. El receptor P01 emite el acta por delta de `G_UI_WRITE`, y WS16/una persona satisfacen `G_HUMAN_READ` antes de habilitar mutaciones UI. WS19 solo cierra cuando cumplen WS19.1 y WS19.2.
