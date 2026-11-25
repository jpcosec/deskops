## REFORMULACION

WS08 es un nodo de planificación del repo `deskops`. Su propósito es mapear los user-flows (UF01–UF10) a las operaciones ya inventariadas en WS02/03/04, cubriendo manual, captura, revisión, cambios, arranque, multidesk, schemas y modo degradado. El resultado es `borradores/user-flows.md`, con entrada/salida, operación, error, nodo del DAG y gate humano por cada UF. Límites: no prometer funciones fuera de alcance, no inventar operaciones ausentes —se marcan como hueco—, no habilitar delegación Scion y distinguir pruebas técnicas de gates humanos. Depende de WS07 y de `G_PRODUCT`, ya satisfecho.

## AMBIGUEDADES

1. «Cubrir todas UF01–UF10»: el input no define qué es cada UF ni dónde está su catálogo. El nodo nombra las auditorías para las operaciones, pero no una fuente para los user-flows. Obligaría al ejecutor a inventar el contenido, entrada y salida de cada UF para poder mapearla.

## DRY-RUN

Un ejecutor futuro leería, sin ejecutar: `decisiones.md`, `owner-decisions.json` y el baseline de WS07; las auditorías `auditoria/{deskops,infraestructura,ui}.md` disponibles transitivamente por WS06/WS07; y los inventarios de operaciones de WS02–WS04. Luego redactaría `borradores/user-flows.md` con una fila por UF, completando operación, nodo, gate humano o «ninguno adicional», y marcando huecos cuando falte operación. Validaría después que las diez UF estén cubiertas, que cada fila tenga los campos exigidos, que los huecos tengan dueño y que ninguna promesa exceda `alcance.md`. No ejecutaría pruebas ni mutaciones.

## FUTURO

WS09 consumirá los UFs para el catálogo de renderizaciones; WS11 y WS12 usarán el mapeo para navegación y operaciones. WS16 y WS30 realizarán validaciones humanas posteriores; WS29 aportará prueba técnica propia. La recepción de deltas y cualquier habilitación Scion quedan fuera de este nodo y corresponden a otros nodos o a decisión humana.
