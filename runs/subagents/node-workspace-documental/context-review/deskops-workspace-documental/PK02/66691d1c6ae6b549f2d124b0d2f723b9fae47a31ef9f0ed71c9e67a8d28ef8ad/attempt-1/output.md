## REFORMULACION
PK02 es un agregado de planificación en `deskops`: agrupa WS07–WS12 para producir el paquete de decisiones y contratos que permite preparar cada delta del workspace documental. Resultado: registro P01–P09 trazado, UFs con operaciones/errores/IDs/gates, convención e índice del manual, catálogo de vistas con soporte/origen, contrato de navegación/identidad y whitelist técnica de operaciones/escritura, con huecos y productores. Límites: no ejecuta, no crea tareas ni aristas, no implementa UI/API, no sustituye la recepción por delta ni asume editable sin `G_SOURCE`; termina cuando terminan sus hijos.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Hipotético, siguiendo las aristas: WS07 lee `decisiones.md`, `owner-decisions.json` y WS06; actualiza el registro y entrega Pxx/actores/fuentes a WS08, WS10, WS09, WS11 y WS12. Tras WS07, WS08 y WS10 pueden avanzar en paralelo: WS08 escribe `borradores/user-flows.md` con UF01–UF10 y transfiere operaciones a WS09 y WS11/WS12; WS10 escribe `borradores/manual.md` con índice, convención, ejemplo futuro WS40 y disponibilidad, y transfiere la convención a WS09. WS09, tras WS08 y WS10, escribe `borradores/vistas.md` con origen/contrato/renderer/acción/dueño/error/estado y transfiere el catálogo a WS11. WS11, tras WS09 y WS08, escribe `contratos/navegacion.md` con identidad, foco, enlaces, multidesk read-only, huecos clasificados y mapa de recibos; transfiere el contrato a WS12. WS12, tras WS11 y WS08, escribe `contratos/operaciones.md` con whitelist, precondición, efectos y huecos/productores; no muta nada.

Validación conjunta futura: cruzar cada Pxx con nodos/gates; cada UF con operación/nodo/gate; cada fila de vistas con soporte/contrato/error; cada hueco con productor; WS12 debe cubrir las operaciones de WS11/UF y marcar faltantes; WS10 no declara disponible sin evidencia; `G_SOURCE` pendiente impide editable; los recibos por delta no se sustituyen por revisión de comprensión.

## FUTURO
WS20/`G_SOURCE`, WS40/corpus, P01 y repos receptores emiten actas por delta, WS45/`G_PAYLOAD_PRECONDITION`, WS16/`G_UI_READ`, y los gates `G_PRODUCT`/`G_WRITE_POLICY`. Un humano decide cambios de alcance.
