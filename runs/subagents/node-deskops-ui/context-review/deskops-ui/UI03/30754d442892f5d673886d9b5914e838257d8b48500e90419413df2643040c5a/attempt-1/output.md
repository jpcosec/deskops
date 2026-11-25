REFORMULACION

Propósito: entregar en graph_ui la pantalla Board de la UI de deskops. Resultado: columnas por nodo del ciclo de vida con nombre y conteo; tarjetas con id, título, checklist de gates, conteo n/m, pills y atoms; panel de detalle con objetivo, gates, evidencia, pills y atoms; Avanzar vía POST con confirmación y guarda; Iniciar ejecución/Promover a atom/Diferir deshabilitados; carril de resumen del drawer; errores visibles; e2e. Repo dueño: graph_ui (`frontends/desk/`, `tests/e2e_desk_ui.py`). Límites: consume la vista de UI01 a través de UI02; no escribe salvo Avanzar; no dibuja datos sin fuente; no implementa las demás pantallas. Depende de UI02; requiere G_SHELL, satisfecho.

AMBIGUEDADES

1. «Iniciar ejecución / Promover a atom / Diferir deshabilitados con el motivo de alcance.md» frente a «deshabilitados con el motivo y el nodo que los habilita» (brief). Alcance da motivos, pero para Promover y Diferir no indica nodo habilitador. Obligaría a inventar qué nodo mostrar o a omitir un requisito del brief.

2. «Carril inferior con un resumen del drawer (enlace a la pantalla Drawer)». No define qué compone el “resumen” (conteo, títulos, estados, últimos elementos) ni el destino/ruta del enlace; la pantalla Drawer es UI05, hermana posterior sin arista. Obligaría a inventar contenido y comportamiento del enlace.

DRY-RUN

Lecturas: dag.yaml, brief, alcance, decisiones, contrato de la vista UI01, shell/rutas de UI02, `DESIGN.md` y la referencia Stitch Active Board; salidas de `deskops view board/task` sobre un desk temporal. Cambios previstos: piezas del Board en `frontends/desk/` (columnas, tarjeta, panel, aviso de error, carril drawer) y `tests/e2e_desk_ui.py`. Dependencias: UI01→UI02 (G_VIEW/G_SHELL), `DeskRoutes` para advance, spec de ciclo de vida, fixtures de desk temporal. Validaciones futuras: e2e con dos tareas en nodos distintos; comparación de gates y conteo con `deskops view board`; avance mueve columna y `deskops show task`; conflicto con revisión vieja; ausencia de las cadenas Stitch listadas; foco por teclado; captura contra Stitch; suite completa en robocop2. Nada ejecutado.

FUTURO

UI04, UI05 y UI06 entregan Tarea, Drawer e Inbox/Agentes; PU02 valida las cuatro pantallas y su e2e común. UI01/UI02 fijan el contrato de vista y las rutas. El TaskDoc de promoción fija nombres de archivos, funciones y tests. Un humano anota diferencias visuales, aprueba la comparación con Stitch y ejecuta la validación en robocop2.
