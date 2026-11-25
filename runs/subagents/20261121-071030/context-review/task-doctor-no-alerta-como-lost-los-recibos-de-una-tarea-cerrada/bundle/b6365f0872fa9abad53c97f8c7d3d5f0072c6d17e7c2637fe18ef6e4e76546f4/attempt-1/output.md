## REFORMULACION
**Propósito:** evitar que `doctor` reporte como `lost` los recibos de auditoría de tareas ya cerradas. **Resultado:** el closeout re-ancla o archiva los recibos; los recibos `lost` preexistentes de tareas con cierre dejan de alertar sin intervención manual; solo alertan recibos de tareas desaparecidas sin cierre; el texto de alerta nombra un comando que realmente repara. **Repo/superficie:** deskops (`services/closure.py`, `doctor`, `models/review.py`). **Límites:** los recibos no se borran; deskops no recalcula anclas, el estado lo da sldb; queda fuera reparar tareas sin cierre.

## AMBIGUEDADES
1. “el closeout re-ancla los recibos al commit de cierre o los marca archivados” frente a “el estado del ancla lo da sldb, deskops no recalcula anclas”: no se sabe si deskops escribe el ancla o solo consulta; obligaría a inventar el responsable y el mecanismo.
2. “closeout registrado en git o en el store”: no se define precedencia, formato ni cómo detectar cada fuente; obligaría a inventar la lógica de detección.
3. “el texto de la alerta de doctor nombra un comando que de verdad la resuelve”: no se indica qué comando; obligaría a inventar la CLI.
4. “borrar una tarea sin cierre si las da”: no se explica cómo correlacionar un recibo con una tarea borrada; obligaría a inventar el criterio de identificación.
5. “## Implementation Path” vacío: no hay ruta prevista; obligaría a inventar orden y puntos de cambio.
6. “test nuevo de deskops (nombre a fijar al promover)”: el nombre queda explícitamente diferido, pero no se fija el alcance exacto del test.

## DRY-RUN
El nodo es un plan, no ejecutable. Un ejecutor futuro leería el TaskDoc, la referencia de inbox, `closure.py`, `doctor`, `models/review.py` y la API de anclas de sldb. Cambios previstos: hook de closeout, filtro en doctor, texto de alerta y test. Dependencias: estado de ancla en sldb y closeout en git. Validaciones futuras: los cuatro escenarios de “Done When” y el test nuevo. Los rituales hijos enrutados por el Board (preflight/bundle/closeout) aportarían recibos, contexto y registro de cierre; la validación conjunta exige que doctor no alerte tras cierre, sí alerte tras borrado sin cierre y no mencione `desk update --apply` si no repara.

## FUTURO
Deciden un humano o nodos posteriores: si sldb o deskops posee el re-anclaje; qué comando nombra la alerta; el nombre del test al promover; y la aceptación de los ~107 recibos preexistentes. Otro nodo ejecutará el test y el closeout.
