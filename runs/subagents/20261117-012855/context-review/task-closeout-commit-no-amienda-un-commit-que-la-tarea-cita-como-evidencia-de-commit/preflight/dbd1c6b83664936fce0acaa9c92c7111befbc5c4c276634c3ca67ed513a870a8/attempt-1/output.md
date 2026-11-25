## REFORMULACION
**Propósito:** evitar que `closeout commit` reescriba mediante `--amend` un commit que la tarea cita como evidencia, dejando un recibo apuntando a un SHA inalcanzable. **Resultado:** en `deskops/services/closure.py`, `closeout commit` creará un commit nuevo cuando el SHA del HEAD coincida con un commit citado por la tarea; en caso contrario mantendrá el amend actual. Se añadirán dos tests en `tests/test_closeout.py`. **Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`. **Límites:** solo la decisión amend/commit nuevo y sus tests; quedan fuera el amend de `index.jsonl`, trailers y otros modos de cierre. Es una tarea ejecutable, no un agregado ni paquete.

## AMBIGUEDADES
1. «su sha, completo o abreviado, esta en references de la tarea o es el value de un recibo evidence-commit aceptado de la tarea». No se define dónde ni con qué formato se almacenan esos SHA en `references` ni cómo reconocer un recibo “aceptado”; obligaría a inventar el esquema de references/recibos.
2. «completo o abreviado». No se especifica la longitud mínima ni la regla de comparación del SHA abreviado con `rev-parse HEAD`; obligaría a inventar el criterio de coincidencia.
3. «verify y closeout commit». No se indican comandos, API interna ni secuencia exacta en el sandbox; obligaría a inventar la invocación de prueba.

## DRY-RUN
Un ejecutor futuro leería la rama `head_task_id == task_id` de `_close` en `closure.py`, la lectura de `references` y de recibos `evidence-commit`, y los tests existentes. Localizaría el punto previo a elegir `--amend`, obtendría `rev-parse HEAD` y compararía ese SHA con los commits citados; si coincide, forzaría commit nuevo; si no, conservaría el amend. Añadiría dos tests con `tmp_path`: commit de código citado que sobrevive con su SHA y cierre en commit aparte; HEAD con `Task-Id` no citado que sigue amendándose. Dependencias: git, sandbox de desk y utilidades de test existentes. Validaciones previstas, sin ejecutar: los dos `pytest` de `tests/test_closeout.py` y `tests/test_closeout_declared_evidence.py`.

## FUTURO
El nodo ejecutor implementará los cambios y aportará la salida de los tests; otro nodo o un humano decidirá la aceptación y el cierre de la tarea.
