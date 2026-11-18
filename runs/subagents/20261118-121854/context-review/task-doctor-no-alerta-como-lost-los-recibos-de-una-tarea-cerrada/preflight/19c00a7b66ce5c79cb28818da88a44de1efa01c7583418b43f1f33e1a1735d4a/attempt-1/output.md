## REFORMULACION
Encargo ejecutable (`task.code`, no agregado; sin hijos): en el repo **deskops**, hacer que `doctor` no alerte como `lost` los recibos/ReviewDoc de tareas cerradas. Al registrarse un cierre por commit o `resolved-by`, los recibos deben reanclarse al commit de cierre o marcarse archivados; solo alertarán los recibos de tareas desaparecidas sin cierre. Resultado: cambios en `deskops/services/closure.py`, `deskops doctor` y `deskops/models/review.py`, más un test nuevo de deskops que cierre una tarea con recibos preflight/bundle y compruebe que `doctor` no da alertas `lost`; borrar sin cierre sí debe darlas. Límite: el estado del ancla lo aporta sldb; deskops no recalcula anclas.

## AMBIGUEDADES
1. “test nuevo de deskops (nombre a fijar al promover)”: el nombre no existe; obligaría a inventar archivo/ruta del test si se ejecuta antes de promover.
2. “el closeout re-ancla los recibos al commit de cierre o los marca archivados”: no se define el campo, estado o API para “archivado” ni para “re-anclar”; obligaría a inventar el modelo de persistencia.
3. “closeout registrado en git o en el store”: no se indica fuente de verdad ni precedencia; obligaría a inventar cómo detectar y combinar ambos cierres.
4. “deskops doctor”: no se especifica comando, módulo ni formato de alerta; obligaría a inventar el punto exacto de integración.
5. “tareas que desaparecieron sin cierre”: no se define “desaparecer”; obligaría a inventar la detección de borrado.

## DRY-RUN
Leería el TaskDoc, el drawer de origen, `closure.py`, el código de `doctor`, `review.py`, la interfaz de anclas de sldb y tests existentes. Cambiaría los flujos de cierre para registrar/reanclar o archivar recibos; ajustaría `doctor` para alertar solo si no hay cierre; añadiría el test con cierre real y caso de borrado sin cierre. Dependencias: estado de anclas de sldb, registros de cierre en git/store y fixtures de prueba. Validaciones futuras: ejecutar el test nuevo, la suite de deskops y una comprobación manual de `doctor`. Sin ejecutar nada.

## FUTURO
Un humano decide el nombre del test al promover y acepta el alcance; el responsable de sldb confirma la API/estado de anclas; otro nodo valida la implementación y sus pruebas.
