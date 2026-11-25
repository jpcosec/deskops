REFORMULACION
Propósito: construir en graph_ui la pantalla “Agentes y corridas” del paquete de pantallas. Resultado: lista de workers vivos (`pane`, `kind`, `status`, `cwd`, título) y de las últimas corridas (`task_id`, `run_dir`, `commit`, modo), con enlace a la tarea si sigue en el Board, sin métricas inventadas. UI06 además cierra el paquete: e2e común de las pantallas, captura comparada con Stitch anotada en el TaskDoc y README de `frontends/desk`. Repo dueño: graph_ui. Límites: datos reales de deskops (`runtime workers`, índice de runs, `deskops view agents`); si herdr falla, mostrar la causa; nada de valores por defecto que parezcan dato; loopback; sin escrituras directas; `output_scope` acotado a `frontends/desk/` y tests.

AMBIGUEDADES
1. “e2e común de las cuatro pantallas” frente a “capturas de las cinco pantallas registradas”. Obliga a inventar si Drawer e Inbox cuentan como una o dos pantallas y cuántas capturas cierran el paquete.
2. “la suite completa de graph_ui verde en robocop2” frente a G_SHELL: “la suite completa de graph_ui no está verde por fallas previas o de entorno… ninguna en frontends/desk”. Obliga a inventar si UI06 debe corregir fallas ajenas, excluirlas o aceptar una excepción.
3. “las últimas corridas” sin criterio de corte ni orden. Obliga a inventar cuántas corridas mostrar y cómo ordenarlas, salvo que `deskops view agents` ya lo fije.

DRY-RUN
Lecturas: `dag.yaml`, guía, brief, alcance, decisiones; salida de UI05; contrato de `deskops view agents`; JSON de `runtime workers` e índice de runs. Cambios previstos: pantalla Agentes/corridas en `frontends/desk/`, e2e común, capturas comparadas, README. Dependencias: UI05 cerrado y G_SHELL satisfecho. Validaciones futuras: pytest de graph_ui, e2e contra desk temporal comparando con `deskops view agents`, prueba de fallo de herdr, capturas de las pantallas y suite completa en robocop2. Nada ejecutado.

FUTURO
UI05 entrega Drawer/Inbox y sus rutas; UI02/G_SHELL aporta el shell; nodos de deskops producen la vista de agentes y corridas; un humano promueve el TaskDoc, hace el preflight y valida las capturas; PU02 cierra el agregado cuando las pantallas cumplen.
