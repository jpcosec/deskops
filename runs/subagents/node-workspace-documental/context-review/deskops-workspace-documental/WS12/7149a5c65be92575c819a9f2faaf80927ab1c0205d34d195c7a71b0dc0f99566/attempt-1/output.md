REFORMULACION
Nodo de planificación (no agregado) para cerrar en deskops el contrato de operaciones y escritura en `contratos/operaciones.md`: whitelist de lectura/mutación por operación, campo, modelo, canal, actor, revisión y efectos; política de coordinador, Git, campos workflow-protegidos, precondición de escritura (`expected` por valor, token publicado o CAS solo si el contrato lo fija), locks, fallos parciales, permisos y closeout fuera del servidor UI. Resultado: matriz de capacidades/efectos y huecos con dueño y prueba, sin habilitar mutaciones. Repo dueño: deskops; solo escribe contrato y enlaces, no ejecuta mutaciones ni crea actas interrepo. Depende de WS11 y WS08; G_WRITE_POLICY ya está satisfecho; produce G_WRITE_CONTRACT con evaluación por delta.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: brief, alcance, decisiones, `dag.yaml`, `contratos/navegacion.md` (WS11), `borradores/user-flows.md` (WS08), inventarios WS02–04 y código/API/pruebas reales de deskops, sldb y graph_ui citando path/símbolo/commit.
Cambios previstos: redactar `contratos/operaciones.md` con whitelist, representación de precondición elegida y justificada, matriz y huecos asignados; solo enlaces en deskops.
Dependencias: WS11/WS08 y auditorías transitivas; productores WS20, WS45, WS46, WS47 y WS48 para los huecos.
Validaciones futuras: cada fila comprobada con evidencia real citada y faltantes con dueño; G_WRITE_CONTRACT por ID/efecto; contraste con WS11; ninguna mutación ejecutada.

FUTURO
WS45 verifica la precondición de payload y G_PAYLOAD_PRECONDITION; WS20 aporta raw-source/G_SOURCE; WS46 prueba o completa la captura; WS47 la guarda de contenido; WS48 la admisión de escritura. Los receptores P01 emiten actas por delta (G_UI_WRITE, G_SLDB_WRITE). WS34.1/WS34.2 fijan el umbral de timeout en la sección del contrato al preparar esos deltas. WS19/25/26/28/39/42 consumen el contrato. El humano decide la aceptación de cada delta.
