## REFORMULACION

El nodo (ejecutable, `task.code`) encarga implementar en el repo **deskops** que `doctor` deje de emitir alertas `lost` por recibos (ReviewDoc) de tareas cerradas: el cierre (closeout commit o resolved-by) debe re-anclar esos recibos al commit de cierre o marcarlos archivados, y solo deben alertar recibos de tareas desaparecidas sin cierre. Además, los recibos `lost` ya existentes de tareas cerradas (~107 en desk de IR) deben dejar de alertar sin intervención manual, y el texto de la alerta debe nombrar un comando que realmente repare (hoy sugiere `deskops desk update --apply`). Límites: superficie en `services/closure.py`, `doctor` y `models/review.py`; el estado del ancla lo provee sldb, deskops no recalcula anclas.

## AMBIGUEDADES

1. "closeout commit y resolved-by" / "el estado del ancla lo da sldb": no define la API ni el campo con que doctor consulta el ancla; obligaría a inventar el contrato sldb↔deskops.
2. "re-ancla los recibos al commit de cierre o los marca archivados": dos alternativas sin criterio de elección ni ubicación de persistencia; obligaría a inventar cuál usar y su semántica.
3. "closeout registrado en git o en el store": no fija precedencia ni cómo leer git; obligaría a inventar ambas fuentes.
4. "~107 en el desk de IR, inbox 20261121-032540": recuento aproximado y desk externo; obligaría a inventar el conjunto exacto y su ruta.
5. "hoy sugiere deskops desk update --apply": no cita el string ni el archivo donde vive; obligaría a inventar ubicación y redacción.
6. "test nuevo de deskops (nombre a fijar al promover)": nombre y formato del pseudocomando `test:` indeterminados; obligaría a inventar la convención.
7. "sin intervencion manual": no aclara si exige backfill, migración o auto-reparación en doctor; obligaría a inventar el mecanismo.

## DRY-RUN

Lecturas: `closure.py`, entrada de `doctor`, `models/review.py`, tests existentes y recibos `lost` actuales. Cambios previstos: al cerrar, escribir ancla/estado archivado en ReviewDoc; en doctor, suprimir alerta si hay ancla; actualizar texto de alerta; backfill de existentes. Dependencias: API de sldb para el ancla y acceso al registro git del cierre. Validaciones futuras: test con closeout real + doctor sin `lost`; borrado sin cierre sí alerta; `lost` preexistente con closeout no alerta; mensaje no menciona `desk update --apply` salvo que repare.

## FUTURO

Un humano fija el nombre del test y decide backfill vs auto-reparación; el dueño de sldb confirma la semántica del ancla; otro nodo promueve el TaskDoc y aporta el conjunto exacto de recibos.
