REFORMULACION
WS07 es un nodo de planificación, no un agregado, del repo `deskops`. Su propósito es mantener trazado el registro de decisiones acordadas reutilizando `decisiones.md` y `owner-decisions.json`. El resultado esperado es el registro concreto de P01–P09 con tipo humano/técnico, actor, fecha, fuente y nodos/gates; conservar `baseline_proposal` y dejar `source_mode=editable` condicionado a G_SOURCE. Límites: no implementa UI/API, no repite preguntas resueltas, no infiere aceptación técnica ni permisos Scion y no sustituye la cobertura de UFs ni las auditorías WS06. Salidas: `decisiones.md` y, solo si procede, `baseline_proposal`/`parameters.source_mode` en `dag.yaml`.

AMBIGUEDADES
1. «Cobertura documental se refiere a decisiones.md + owner-decisions.json y covered_work de este nodo». `covered_work` no aparece definido ni localizable en el input; el ejecutor tendría que inventar qué contiene, dónde se consulta y cómo se verifica.
2. «source_mode=editable condicionado a G_SOURCE» junto a «output_scope: ... parameters.source_mode en dag.yaml». G_SOURCE está pendiente y no se indica si debe dejarse el valor actual, escribirse un valor condicional o esperar; el ejecutor inventaría la representación y el momento del cambio.
3. «actualizar solo ante nueva decisión explícita con fuente verificable» / «actualizar solo por cambio real de decisión». No se define qué registro acredita que la decisión es nueva ni quién la declara; el ejecutor podría inventar el criterio de novedad.

DRY-RUN
Lecturas: `decisiones.md`, `owner-decisions.json`, `dag.yaml` raíz y `reconciliacion.md` de WS06. Cambios previstos: ninguno por defecto; solo actualizar el registro si aparece una decisión nueva verificable, preservando `baseline_proposal`. Dependencias: WS06 como prerrequisito directo. Validaciones futuras: contrastar P01–P09 con actor/tipo/fuente, comprobar G_PRODUCT/G_WRITE_POLICY, no crear gates ni aceptaciones, y confirmar que G_SOURCE sigue pendiente antes de habilitar `editable`. Sin ejecución.

FUTURO
WS08, WS09 y WS10 consumen el mapeo de decisiones; WS44 y el ramal E esperan designación de operador/permisos; WS20 debe producir G_SOURCE antes de cualquier `source_mode=editable`. El solicitante o un humano registra nuevas decisiones; la promoción fijará TaskDoc y archivos exactos.
