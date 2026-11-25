REFORMULACION
PF4 es el agregado de cierre (P5) del plan, en deskops y no ejecutable: termina cuando cierran CC51, CC52 y CC53, no se promueve. Su encargo: medir qué quedó como código y como configuración, verificar los 6 desks y el Board, y documentar cómo se declara un tipo de tarea nuevo. Resultado exigido: `docs/config-vs-code.md` con inventario; los 6 desks verdes; Board < 1 s caliente sobre el desk real; `docs/configuration.md` publicada. Límites: no escribe en sldb, no suple reglas con Python, no cambia formato del desk ni gramática del CLI, no toca P4 y no ejecuta cambios propios.

AMBIGUEDADES
1. «docs/configuration.md publicada»: “publicada” no define destino, índice ni forma de publicación; obligaría a inventar si basta con que exista en `docs/` —como acepta CC53— o si requiere otro canal. Cita: «docs/configuration.md publicada».

DRY-RUN
Un ejecutor futuro no correría PF4: comprobaría que CC51, CC52 y CC53 están cerrados y que sus artefactos satisfacen la aceptación agregada. Lecturas: `dag.yaml`, TaskDocs y reportes de los hijos, `docs/config-vs-code.md`, `docs/configuration.md`, enlaces desde `operator-manual` y `workflow-policy-reference`, CHANGELOG. Cambios previstos: ninguno. Dependencias: los tres hijos y, transitivamente, CC30–CC38 y sus gates. Validaciones: que `docs/config-vs-code.md` tenga las dos mediciones, el inventario justificado y la sección de verificación; que `docs/configuration.md` exista y su receta se pruebe; que CC52 registre doctor, view board, `stores check`, `rules check` y la mediana caliente < 1 s en los 6 desks. CC51 aporta medición e inventario; CC52 la tabla de verificación; CC53 el mapa de configuración y la receta. No hay transferencia entre hermanos salvo el documento compartido por CC51 y CC52.

FUTURO
El dueño fija N tras CC30 (DA3); el supervisor corre las suites completas; sldb entrega los gates; el coordinador promueve los hijos, no PF4; graph_ui y la publicación efectiva de la documentación quedan fuera de este nodo.
