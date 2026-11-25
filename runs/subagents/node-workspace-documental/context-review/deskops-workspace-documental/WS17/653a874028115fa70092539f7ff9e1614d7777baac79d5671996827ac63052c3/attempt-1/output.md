REFORMULACION
WS17 es un nodo de documentación en `deskops`. Propósito: escribir entradas e índices authored del desk ejemplo como plantillas Markdown versionadas bajo el paquete del plan (`ejemplo/nav/`), sin producir el corpus. Resultado: plantillas que WS40 materializa en su root temporal y WS43 reutiliza en publicación real. Límites: no copiar inventarios derivados, no duplicar el registry de deskops, no enlazar al checkout real en el conjunto temporal y no escribir repos reales; depende del contrato WS11 y del manifiesto WS40. Aceptación: regenerar el corpus con las plantillas, recorrer links Markdown sin UI, verificar resolución identidad/root/store/aliases contra el manifiesto WS40 y que el conjunto cubra ambos desks, con las plantillas como fuente única.

AMBIGUEDADES
1. «cada plantilla resuelve el root/store de procedencia de los dos desks del manifiesto WS40» frente a «conjunto de plantillas cubre ambos desks, no cada plantilla individual». Obliga a inventar si cada plantilla debe enlazar ambos desks o basta que lo haga el conjunto, y qué cuenta como cobertura. Puede producir redundancia o cobertura insuficiente.

DRY-RUN
Lecturas: `contratos/navegacion.md` de WS11, generador y manifiesto de WS40, e inventario WS02 del registry. Cambios previstos: plantillas Markdown bajo el paquete del plan. Dependencias: WS11 y WS40, con WS08 detrás. Validaciones futuras, sin ejecutar: regenerar el corpus con la ruta de plantillas; recorrer cada link y comprobar su resolución contra roots/stores/aliases del manifiesto; verificar ausencia de copia del registry y de enlaces al checkout real; comprobar cobertura conjunta de ambos desks y que el destino se regenera desde las plantillas. WS30 enumerará plantillas, paths y hashes; WS43 mapeará a publicación real.

FUTURO
WS11 debe entregar el contrato de identidad/root/store/aliases; WS40 debe aceptar la ruta de plantillas y emitir manifiesto con roots/stores; WS30 valida humanamente y enumera plantillas; WS43 publica en el desk real. La aceptación final y las actas corresponden al responsable humano/receptor.
