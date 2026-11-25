## REFORMULACION
UI05 es un nodo code/delivery de graph_ui, hijo de PU02, que construye las pantallas Drawer e Inbox en `frontends/desk`. Propósito: convertir tareas diferidas y notas del inbox en superficies de trabajo. Resultado: Drawer con lista (título, status, extracto), Markdown crudo de solo lectura y comando `deskops add task --from-drawer <id>` copiable; Inbox con lista (emisor→destino, kind, título, fecha, ack), cuerpo y acciones Reconocer y Pasar al drawer vía POST nuevo en `frontends/desk/serve.py`, con confirmación y guarda por hash de la nota. Límites: sin hilo, firmas, prioridad ni métricas; escritura solo por operaciones de deskops; ningún dato sin fuente; alcance en `frontends/desk` y tests.

## AMBIGUEDADES
1. "lista con emisor → destino, kind, título, fecha y estado de ack": alcance.md define InboxNoteDoc como "kind, title, body, sender/to", sin fecha. Obliga a inventar de dónde sale la fecha o a omitir un campo exigido, contra DU5.
2. "lista de tareas diferidas con título, status y extracto": "extracto" no tiene criterio; alcance.md solo dice "primeras líneas". Obliga a fijar cuántas líneas y con qué formato.
3. "el comando copiado es exacto" frente a "el comando deskops add task --from-drawer <id> listo para copiar": no se define si se copia el literal con `<id>` o el id real. Obliga a elegir uno.
4. "una ruta POST nueva" frente a "pytest de las rutas POST nuevas": singular/plural no aclara si son uno o dos endpoints. Obliga a decidir la forma del contrato HTTP.

## DRY-RUN
Lecturas: fuentes del plan; código existente de `frontends/desk`, `serve.py`, rutas de UI03/UI04 y operaciones deskops (`message list|ack`, `promote inbox-to-drawer-task`, vista drawer). Cambios previstos: pantallas Drawer/Inbox, endpoints POST, tests de rutas y e2e. Dependencias: UI04 integrado y G_SHELL satisfecho. Validaciones futuras: pytest de rutas; e2e sobre desk temporal (listados, comando exacto, ack visible, promoción equivalente al CLI, conflicto por nota modificada); ausencia de textos de Stitch; suite de graph_ui en robocop2.

## FUTURO
UI06 ejecuta el e2e común de las cuatro pantallas, las capturas comparadas con Stitch y el README; un humano valida esas capturas y la suite verde en robocop2, cuyos pendientes ya constan en la evidencia de G_SHELL.
