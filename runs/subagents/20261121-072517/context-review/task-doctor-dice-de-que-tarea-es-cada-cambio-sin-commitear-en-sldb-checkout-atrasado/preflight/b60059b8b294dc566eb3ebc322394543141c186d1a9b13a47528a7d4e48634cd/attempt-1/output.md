REFORMULACION
El nodo es una tarea ejecutable (`task.code`), no un agregado. Propósito: que `deskops doctor` liste los cambios sin commitear bajo `.sldb/`, agrupados por la tarea o documento de desk que los originó, y marque los sin dueño. Resultado: comando `doctor` con esa agrupación/marcado y un test con un repo real cuyo `.sldb` fue modificado por dos tareas. Repo afectado: `deskops`; depende de `sldb` para API y para H1/H2 en merges. Límites: leer estado git de `.sldb` y sujetos vía API de `sldb`; no reimplementar el diff del store.

AMBIGUEDADES
1. «agrupados por la tarea (o el documento de desk) que los origino»: no define cómo inferir el origen desde cambios git; obligaría a inventar reglas de mapeo cambio→tarea/documento.
2. «lee el estado de git de .sldb y el sujeto de cada documento por la API de sldb»: “sujeto” no aclara qué campo identifica la tarea; obligaría a inventar el contrato API.
3. «Depende de H1/H2 en sldb para el caso de merge»: H1/H2 no están definidos; obligaría a inventar su alcance y comportamiento.
4. «test nuevo de deskops (nombre a fijar al promover)»: nombre y momento de fijación indeterminados; obligaría a inventar el nombre o el criterio de promoción.
5. «un repo real cuyo .sldb cambiaron dos tareas»: no especifica fixture, setup ni cómo simular dos tareas; obligaría a inventar el escenario de prueba.
6. «no reimplementa el diff del store (sldb)»: no fija la frontera exacta; obligaría a decidir qué cálculo pertenece a deskops.

DRY-RUN
Lecturas: TaskDoc, código de `deskops doctor`, estado git de `.sldb`, API de `sldb`. Cambios previstos: lógica de agrupación/marcado y test de repo real con dos tareas. Dependencias: git, API de `sldb`, H1/H2 para merge. Validaciones futuras: ejecutar el test nuevo y la suite de deskops; comprobar agrupación y marcado de huérfanos.

FUTURO
Un humano fija el nombre del test al promover y aclara el mapeo/API si falta; `sldb` entrega H1/H2.
