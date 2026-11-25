REFORMULACION
WS35 es un nodo de implementación, no agregado. Encarga a `graph_ui` una vista de ejecución/trazabilidad que lea tarea de deskops, intento/decisión de WS32/WS33, mensajes de Scion por API y resultados vinculados por WS33.1. Resultado: mostrar cada mensaje, resultado y decisión bajo su intento y tarea, enlazar su fuente, abrir evidencia en el lector WS13 y mantener `completed` separado de aprobado/cerrado. Límites: solo `frontends/mindmap/views/workspace/execution/` y `tests/`; depende de WS33 y WS27 y requiere G_SCION y G_UI_READ.

AMBIGUEDADES
1. «intento y decisión de WS32/WS33»: no aclara si las decisiones vienen de WS32, de WS33.2 o de ambos, ni cómo se asocian al intento. Obliga a inventar la fuente y el criterio de inclusión.
2. «Cada mensaje, resultado y decisión se muestra bajo su intento y tarea»: no define qué hacer con elementos sin intento o tarea asociados —omitirlos, agruparlos aparte o bloquear—. Obliga a inventar el fallback.

DRY-RUN
Lecturas: salidas de WS33 (WS33.1 resultados, WS33.2 decisiones, referencias/procedencia), evidencia de WS27.2, lector WS13, tarea de deskops y API de mensajes Scion. Cambios previstos: vista e integración en `execution/` y tests. Dependencias: WS33 y WS27 completos; G_SCION verificado y recibo G_UI_READ del delta. Validaciones futuras: agrupación bajo intento/tarea, enlace a fuente, apertura de evidencia en WS13, etiqueta `completed` no aprobatoria y error visible si faltan API/permisos. Si falta contrato/dato, detenerse y registrar el hueco; no inventar sustituto.

FUTURO
WS33/WS27 producen datos y contratos; WS44 resuelve G_SCION; el receptor de `graph_ui` emite G_UI_READ por delta; el TaskDoc fija archivos, pruebas y textos. Son dependencias o decisiones externas, no ambigüedades de WS35.
