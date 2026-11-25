REFORMULACION

Propósito: que el Board real se pueda recorrer como trabajo navegable en tres representaciones —lista, tablero agrupado por estado y dependencias declaradas en el TaskDoc— sin sustituir el workflow. Resultado: vistas en graph_ui que abren el mismo TaskDoc y sus pills/átomos referenciados en el lector, con selección y links comunes y estados/lifecycle tomados de deskops. Repo dueño: graph_ui. Límites: salidas solo en `frontends/mindmap/views/workspace/board/` y `tests/`; nada de drag-and-drop de status; no duplicar tareas ni presentar predicado satisfecho como test aprobado. Depende de WS13 y WS09; gate G_UI_READ por delta.

AMBIGUEDADES

1. «estados y condiciones de lifecycle leídos de deskops (Board, lifecycle), no de dag.yaml»: el nodo exige leer Board/lifecycle, pero no nombra quién produce ese contrato/API ni lo incluye en `depends_on` (solo WS13 y WS09; WS09 es inventario/catálogo, no contrato). Obligaría al ejecutor a inventar la fuente/API o a asumir WS12 sin declararlo.

DRY-RUN

Lecturas: salidas de WS13 (lector, foco/historia, registry de vistas), catálogo WS09 (fila Board/renderizaciones), contrato de lectura de Board y lifecycle en deskops. Cambios previstos: módulos de lista, tablero y dependencias bajo `views/workspace/board/`, registrados en el registry existente; tests en `tests/`. Dependencias: WS13 completo, WS09 disponible, contrato de Board/lifecycle y recibo G_UI_READ del delta concreto; si falta el contrato, detenerse y registrar hueco, no crear sustituto. Validaciones futuras: tests de que las tres representaciones abren el mismo TaskDoc y sus pills/átomos; selección/links compartidos con lector; estados/lifecycle provenientes de deskops y no de dag.yaml; ausencia de duplicación; distinción predicado/test.

FUTURO

El receptor de graph_ui emite el acta G_UI_READ por delta; el TaskDoc de promoción fija archivos, escenarios y textos; WS30 valida manualmente; WS26 consume WS22; si falta el contrato de lectura, el responsable del repo dueño decide y abre tarea, y WS09 podría actualizar su fila.
