REFORMULACION
PK01 es un agregado de planificación, no ejecutable, con repo dueño deskops. Propósito: fijar una base factual y una matriz de deltas verificables para evitar duplicar código. Resultado: brief/glosario cubierto (WS01), auditorías de superficies Deskops (WS02), persistencia/consultas/notaciones (WS03), UI/SPEC/trabajo en curso (WS04), inventario Scion (WS05) y reconciliacion.md con matriz por repo dueño (WS06). Límites: no implementar, no tocar Board/tareas ajenas, no probes vivos ni credenciales, no producir gates ni aceptación de producto; la agrupación no añade tareas ni aristas.

AMBIGUEDADES
ninguna.

DRY-RUN
Hipotético: WS01 verifica brief.md y su recibo covered_work; entrega brief/glosario como prerrequisito a WS02, WS03, WS04 y WS05. WS02, WS03 y WS04 avanzan en paralelo tras WS01, solo lectura, con salidas propias: auditoria/deskops.md, auditoria/infraestructura.md y auditoria/ui.md. WS05, también tras WS01, produce auditoria/scion.md sin contactar endpoints; no se entrega a WS06: alimenta E como ramal independiente. WS06 espera WS02–WS04 e integra sus evidencias en reconciliacion.md: una fila por delta/capacidad, agrupada por repo dueño, con cubierto/extender/nuevo/ausencia y path/símbolo/commit. Lecturas: archivos y comandos de solo lectura del checkout, ../UIs/graph_ui, ../scion y SPEC externo; sin cambios de código. Validación conjunta futura: comprobar que existen las seis salidas, que cada auditoría cita ubicación, operación y estado comprobado/no comprobado con causa, que la matriz cubre cada delta sin omitir nodos graph_ui ni Scion, y que no hay firmas, gates ni recepción ficticia. La completitud no se prueba por status/hash: exige revisar cobertura y evidencia; las revisiones de comprensión no equivalen a producto.

FUTURO
La aceptación de deltas y las actas corresponden al receptor P01 en su repo; WS11/WS12 aportan contratos y enlazan actas; WS44 produce la evidencia G_SCION; WS32/WS33 conservan dependencias Scion; el TaskDoc de promoción fija archivos y pruebas. Nada de eso lo decide PK01.
