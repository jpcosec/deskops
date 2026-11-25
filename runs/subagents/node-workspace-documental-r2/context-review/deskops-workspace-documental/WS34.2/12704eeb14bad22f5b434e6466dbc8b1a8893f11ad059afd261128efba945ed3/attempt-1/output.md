## REFORMULACION
WS34.2 es un encargo de implementación en `deskops`, no un agregado. Propósito: exponer un adaptador público restringido para reply vinculado al intento, con timeout/errores y autoridad del coordinador. Resultado: código en `runtime/`, `cli/commands/runtime.py` o la API que fije WS12, y `tests/`. Límites: no mandar mensajes durante planificación; no elegir umbral de timeout propio; detenerse y registrar hueco si falta la política WS12; requiere G_EXEC/G_SCION/G_WRITE_CONTRACT y depende de WS33, WS12 y WS34.1. Aceptación: gates y agente real que demuestre reply al intento correcto y timeout reportado como fallo sin confirmación.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Lecturas: WS34.2; aristas WS33, WS12, WS34.1; gates G_EXEC/G_SCION/G_WRITE_CONTRACT; guía, brief, alcance y decisiones. Cambios previstos: implementar el adaptador y sus pruebas, sin envíos reales en planificación. Dependencias: WS33 aporta referencias/procedencia; WS12, whitelist, adapter, autoridad y umbral de timeout por delta; WS34.1, dispatch e identidad/correlación del intento; G_SCION, acceso/probe Scion; G_EXEC, autorización. Validaciones futuras: G_WRITE_CONTRACT aceptado para WS34.2; G_EXEC/G_SCION pasan; prueba con agente real de reply al intento correcto; timeout como fallo sin confirmación; ausencia de política → parada y registro de hueco.

## FUTURO
WS12 fija la política y el umbral de timeout; WS44 produce el probe de G_SCION; un humano externo resuelve G_EXEC; WS34.1 entrega dispatch y correlación; el TaskDoc de promoción fija archivos, escenarios y textos; la recepción `per_delta` registra el recibo. Nada de esto es ambigüedad del nodo.
