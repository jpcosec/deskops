REFORMULACION
Propósito: verificar o completar en `sldb` la precondición de escritura de payload, distinguiendo before-image (`expected`/409), token publicado (`version`/`content_hash`) y precondición compartida aún no probada. Resultado: inventario con path/símbolo/commit frente al contrato WS12 y pruebas reales focalizadas; solo si falta capacidad, código mínimo con tarea propia en `sldb`. Repo dueño: `sldb`. Límites: no fuerza CAS ni elige hash, no toca UI, no depende de `source_mode`/raw-source y no crea sustituto si falta un contrato.

AMBIGUEDADES
ninguna

DRY-RUN
Nodo ejecutable (`implementation`), no agregado.
Lecturas: WS45, contrato WS12 y gates; código/API/CLI/tests reales de `sldb`; `brief.md`, `alcance.md` y `decisiones.md` como límites.
Cambios previstos: inventario de la capacidad existente y pruebas focalizadas en `tests/`; modificar `src/sldb/api/documents/` o `src/sldb/cli/serve/` solo si la ejecución demuestra capacidad faltante y con tarea propia en `sldb`. Sin cambios de UI ni de raw-source.
Dependencias: WS12 produce representación, operaciones y escritores alcanzados; por transitividad, WS11/WS08. Gates: `G_WRITE_CONTRACT` por delta y `G_SLDB_WRITE` como recibo del delta concreto.
Validaciones futuras: para cada operación/escritor del contrato, prueba real de rechazo observable de precondición obsoleta sin cambios, aplicación de precondición vigente y observabilidad por el llamante; si la capacidad es parcial, completar lo faltante y reprobar todo el contrato. `G_PAYLOAD_PRECONDITION` solo con esa evidencia verificable.

FUTURO
WS12 decide y documenta la representación de la precondición, operaciones y escritores, y produce `G_WRITE_CONTRACT` por delta. El receptor humano P01 en `sldb` emite el acta `G_SLDB_WRITE` del delta concreto. Si falta capacidad, un humano/autorización de trabajo debe abrir la tarea propia en `sldb`; WS45 no la crea. No hay decisión humana pendiente sobre CAS, algoritmo de hash, UI ni aprobación de implementación.
