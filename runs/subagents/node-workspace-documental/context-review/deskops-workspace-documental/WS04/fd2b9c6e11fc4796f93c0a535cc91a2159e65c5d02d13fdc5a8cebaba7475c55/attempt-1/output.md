## REFORMULACION
WS04 encarga una auditoría de planificación en `deskops`: leer el Board, tareas, código y estado actual de `graph_ui`, identificar sesiones y solapamientos, y registrar en `auditoria/ui.md` la correspondencia entre los nodos de este plan que toquen `graph_ui` y una base reutilizada, delta, ticket o ausencia explícita. También debe reconciliar el SPEC externo indicado, con coincidencias, discrepancias y ausencias. El resultado es un documento verificable; no se modifican tareas, Board ni código de `graph_ui`. Límites: no ejecutar implementación, no resolver autoridad de sesiones y no convertir commits en aceptación ampliada. No es un nodo agregado.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml` para enumerar los nodos que tocan `graph_ui`, el resultado de WS01, el Board y tareas de `graph_ui`, `git status`, los commits `a1b2b22/f16fcd1/134a665`, paneles `herdr` y `/home/jp/proyectos/softfactory_spec/SPEC.md`. Si el solicitante aporta un encargo, lo leería; si no, registraría su ausencia.

Produciría o actualizaría `auditoria/ui.md` con: tareas externas y su path, estado observado, SHA256 del archivo de tarea y alcance; solapamientos por misma tarea o archivos reclamados; sesiones observadas o su ausencia; reconciliación del SPEC con path y hash; y una tabla por nodo `graph_ui` con ID, base/delta/ticket/ausencia explícita, path o símbolo y commit observado si está implementado.

Dependencias: WS01 como prerrequisito; acceso de lectura a `graph_ui`, sus tareas/Board, git y `herdr`; SPEC externo. Validaciones posteriores: cada nodo aplicable tiene fila; cada tarea citada existe con hash correcto; cada solapamiento está justificado; el SPEC tiene path/hash; no se modificaron tareas ni Board. Si falta un dato, se registrará el hueco sin sustituirlo.

## FUTURO
WS06 consumirá esta auditoría para construir su matriz por repo dueño y reconciliar deltas. Las sesiones o responsables de `graph_ui` decidirán, fuera de este nodo, cómo resolver sus solapamientos. La aceptación de producto y las actas por delta corresponden al solicitante y al receptor P01, no a WS04.
