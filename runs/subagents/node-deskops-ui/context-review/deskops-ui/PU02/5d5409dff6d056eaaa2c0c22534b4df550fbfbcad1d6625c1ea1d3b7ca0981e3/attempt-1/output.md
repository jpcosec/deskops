REFORMULACION
PU02 es un agregado no ejecutable de graph_ui que agrupa las pantallas de la UI de deskops. Su propósito es entregar Board, Tarea, Drawer e Inbox y Agentes como una serie de hijos en un mismo worktree, porque comparten archivos de `frontends/desk/`. El resultado es el conjunto de las aceptaciones de UI03–UI06 más el e2e común; no produce código propio. Límites: owner graph_ui, solo loopback y design system de graph_ui; sin datos de ejemplo, sin escrituras fuera de operaciones deskops; no incluye lo fuera de alcance del brief. Termina cuando terminan sus hijos.

AMBIGUEDADES
1. "Las cuatro pantallas cumplen su aceptación" frente a "Board, Tarea, Drawer e Inbox, Agentes". Obliga a inventar si la aceptación agregada cuenta cuatro nodos hijos o cinco pantallas, y si Drawer e Inbox son una o dos. Es el único punto que un validador del agregado tendría que resolver sin fuente.

DRY-RUN
No se ejecuta: es agregado. Lecturas: dag, brief/alcance/decisiones y salidas de `deskops view`. Un ejecutor futuro seguiría la cadena de hijos: UI03 (tras UI02/G_SHELL) construye Board y el e2e inicial en `frontends/desk/` y `e2e_desk_ui.py`; transfiere shell, consumo de `/api/view/board` y patrón de acciones. UI04 añade Tarea, reutiliza Avanzar y enlaza Inspeccionar; transfiere navegación y comportamiento común de acciones. UI05 añade Drawer e Inbox, rutas POST con confirmación y guarda de revisión, y tests de rutas; transfiere esos patrones. UI06 añade Agentes/corridas, cierra el e2e común, README y capturas. La validación conjunta ejecutaría las aceptaciones de UI03–UI06 en orden y el e2e común de UI06 sobre un desk temporal, comprobando que lo mostrado coincide con `deskops view` y que no aparecen cadenas de Stitch. Antes habría que fijar la lectura de “cuatro/cinco”.

FUTURO
UI01 produce la vista de datos; UI02 el servidor y shell; G_SHELL/G_VIEW son gates de otros. Los TaskDoc de UI03–UI06 fijarán archivos, funciones, tests y worktree exactos. UI06 produce el e2e común, README y capturas; el humano valida capturas y merge en robocop2.
