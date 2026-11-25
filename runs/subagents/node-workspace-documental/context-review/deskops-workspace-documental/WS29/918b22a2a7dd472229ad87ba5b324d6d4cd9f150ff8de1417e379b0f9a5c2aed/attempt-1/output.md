REFORMULACION
WS29 es un nodo `implementation` de `graph_ui`, rol delivery, que amplía la tarea Changes existente. Propósito: integrar en Changes el impacto comprobable de una mutación: documento afectado, relaciones entrantes y salientes a 1 hop según la API de grafo de sldb, y hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`, agrupados por comando. Resultado: vista que muestra esos datos y enlaza cada hallazgo al comando documentado en su repo dueño; reparar no es automático. Límites: no CST ni árbol Kimun supuesto; pruebas sobre store temporal real; no bloquea lector/manual básico. Repo y salidas: `frontends/mindmap/views/workspace/changes/`, rutas de integridad según contrato WS11 y `tests/`. No es agregado: se ejecuta como delta.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: tarea Changes actual y contrato WS11 en graph_ui; API de grafo de sldb disponible vía WS24; documentación de los tres comandos en sldb/deskops. Cambios previstos: extender la vista Changes para mostrar documento afectado, vecindad 1-hop entrante/saliente y hallazgos agrupados; añadir enlaces a la documentación del comando correspondiente; tests. Dependencias: WS15 y WS24 terminados; `G_UI_READ` con recibo per-delta de WS29. Validaciones futuras: crear store temporal real, aplicar una mutación, comprobar documento/relaciones/errores, verificar enlaces y ausencia de reparación automática; si falta contrato/API, detenerse y registrar hueco. Sin ejecutar.

FUTURO
El TaskDoc de promoción fija archivos, escenarios y textos; el receptor humano P01 emite el acta G_UI_READ del delta concreto; WS11 y WS24 aportan contrato y API; los repos dueños de los comandos publican su documentación. Nada de eso se decide en esta revisión.
