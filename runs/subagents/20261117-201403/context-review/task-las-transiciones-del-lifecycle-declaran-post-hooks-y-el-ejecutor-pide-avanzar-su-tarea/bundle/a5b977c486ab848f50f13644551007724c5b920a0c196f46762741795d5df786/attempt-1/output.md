REFORMULACION  
Propósito: que las transiciones del lifecycle declaren post-hooks deterministas y que el ejecutor pida `deskops advance task` al terminar. Resultado: `attributes.hooks` leído desde RelationDoc, ejecución ordenada tras persistir, log en `runs/hooks/...`, rollback de status/current_node/history y error con hook/código/log si falla; conservación en `desk update --apply`, exclusión en doctor, salida en `next`/`show task`, textos de ejecutor/coordinador, atom y manual. Repo: deskops; superficie en los archivos nombrados por el TaskDoc. Límites: no cola/runner, no rol nuevo, no cambios en sldb, no hooks en otros comandos, no declarar hooks concretos.

AMBIGUEDADES  
1. “el texto del coordinador (`_render_coordinator_agents_md`) deja de avanzar el esa transicion y pasa a verificar que ocurrio.” No define qué evidencia o comprobación concreta debe hacer; obligaría a inventar comandos y criterio de verificación.  
2. “deja el hallazgo en su resumen y senala `sciontool status blocked` con ese texto.” No precisa si “ese texto” es el mensaje completo de `advance`, el nombre del hook o una síntesis; obligaría a inventar el formato.  
3. “`runs/hooks/<id de la tarea>/<relation_type>-<fecha y hora UTC compacta>.log`” no fija el formato exacto de la marca temporal; obligaría a inventar el patrón.  
4. “una entrada puede traer `timeout` (entero, segundos)” no fija rango ni si `0` o negativo es inválido o malformado; obligaría a inventar validación.

DRY-RUN  
Lecturas: TaskDoc, Board, rituales, pills, átomos y los archivos listados; RelationDoc y semillas; tests y manual. Cambios previstos: `Transition.hooks` en `lifecycle.py`; en `advance_task`, validar hooks antes de persistir, guardar snapshot, persistir, ejecutar secuencialmente con cwd en raíz, variables, timeout y log, y revertir campos ante fallo; `next`/`show task` listan hooks; doctor y `desk update --apply` preservan; templates, atom y manual; tests con comandos reales. Dependencias: metadata de RelationDoc, runner con timeout y fixture `lifecycle_desk`. Validaciones futuras: los tres comandos de Validation. Nada ejecutado.

FUTURO  
El ejecutor implementa y decide estructura interna; el coordinador o humano adjudica las ambigüedades 1–4 y valida manual/atom; revisión independiente y suite deciden aceptación. No es un agregado ni paquete no ejecutable.
