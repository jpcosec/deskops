REFORMULACION

WS13.3 es un nodo de implementación en `graph_ui`: entregar pestañas y divisiones del lector workspace, con dos documentos lado a lado, documento activo, foco por documento, origen e historia de navegación que vuelve en orden inverso. La disposición es estado local de sesión de navegador, no documento compartido, y no se exige persistir tras recargar. Límites: `frontends/mindmap/views/workspace/layout/`, rutas de lectura del contrato WS11 y `tests/`. Depende de WS11 y WS13.1; G_UI_READ queda pendiente por delta.

AMBIGUEDADES

1. «Volver sigue el orden inverso de navegación.» No define qué acciones entran en la historia: abrir pestaña, cambiar pestaña, cambiar división, cerrar pestaña o seguir enlace. Obliga a inventar la granularidad de eventos y qué ocurre al volver a una pestaña cerrada.
2. «abrir dos documentos en divisiones» y «Cambiar de pestaña o división cambia el documento activo»: no aclara si las pestañas son globales o propias de cada división. Obliga a inventar el modelo de disposición y la relación entre pestaña, división y documento activo.

DRY-RUN

Lecturas: contrato WS11 para rutas, foco e historia; entrega de WS13.1 para documento, fuente y foco; P07 y reglas comunes de alcance. Cambios previstos: layout de pestañas y dos divisiones; estado local de sesión para disposición, foco por documento e historia; navegación atrás; pruebas. Dependencias: WS11 debe dar rutas de lectura y WS13.1 el lector/foco; si falta, detenerse y registrar el hueco, sin crear sustituto. Validaciones futuras: abrir, cambiar y cerrar pestañas; dos documentos lado a lado; alternar documento activo; volver restaurando documento, foco y origen en orden inverso; comprobar que no se exige persistencia tras recarga; acta G_UI_READ de este delta por P01 en `graph_ui`. Sin ejecutar.

FUTURO

El TaskDoc de promoción fijará archivos, escenarios y textos de pantalla. P01/receptor del repo emitirá el acta G_UI_READ del delta. El agregado WS13 validará el conjunto cuando sus hijos cumplan, y los dependientes de WS13 consumirán el lector integrado.
