REFORMULACION  
WS09 es un encargo de planificación en `deskops`: inventariar las renderizaciones y vistas existentes o previstas, incluyendo fuente, consultas, Board, ritual, conocimiento/crossroads, issues, FAQ, Code y vistas actuales. El resultado es `borradores/vistas.md`, con una ficha por fila y tablas completas según la aceptación. Límites: no implementa UI ni renderers, no modifica otros repos, no trata ViewDoc como contrato universal de UI y no inventa actores, APIs, campos, relaciones ni errores disponibles.

AMBIGUEDADES  
Ninguna.

DRY-RUN  
Lecturas previstas: `decisiones.md`/`owner-decisions.json` y registro de WS07; `borradores/manual.md` de WS10 para la convención de estado; `borradores/user-flows.md` de WS08; auditorías WS02–WS04 de forma transitiva, incluida `auditoria/ui.md` para disponibilidad actual. Cambios previstos: crear o actualizar `borradores/vistas.md` con las tablas y fichas por fila, clasificando authored/derivado/preferencia local y estado disponible/propuesto/bloqueado. Dependencias: WS07, WS10 y WS08; `G_PRODUCT` ya satisfecho. Validaciones futuras: cada fila debe tener origen, contrato o «sin contrato», renderer, acción/dueño, error y estado; los campos sin evidencia se marcarán no definidos con productor WS11/12 o futura implementación; las filas compuestas admitirán listas; los estados propuesto/bloqueado no inventarán error actual. No se ejecuta nada.

FUTURO  
WS11 consumirá el catálogo para cerrar el contrato de navegación e identidad y clasificar huecos. WS18 usará WS09 y WS11 para definir selecciones y notación; si el catálogo no fija una selección mínima, su promoción deberá detenerse y corregir antes ese contrato. WS22, WS23 y WS24 usarán el catálogo para representar Board, procedimientos y grafo local. No se requiere una nueva decisión humana para WS09: `G_PRODUCT` ya está registrado.
