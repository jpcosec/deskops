REFORMULACION
Propósito: evitar que `advance` y `closeout` dejen en el desk del proyecto consumidor archivos centrales sin trackear (`desk/lifecycle/rule-activation-task-*.md` y `desk/runtimes/runtime-pi-deepseek-flash.md`). Resultado: que las semillas centrales se lean del paquete en runtime o se escriban solo mediante `deskops desk update --apply`, quedando trackeadas y declaradas. Repo/superficie: deskops, `lifecycle.py`, `workspace.py`, `cli/commands/desk.py`. Límites: incluye decidir el enfoque en preflight y añadir un test de regresión; no incluye ejecutar aquí. Nodo ejecutable `task.code`, no agregado.

AMBIGUEDADES
1. "decision de cual de las dos formas en el preflight": no se registra la decisión ni criterios; obliga a inventar si se lee en runtime o se escribe solo con `--apply`.
2. "test nuevo de deskops (nombre a fijar al promover)": no hay nombre, ruta ni framework; obliga a inventar ubicación y convención.
3. "git status limpio fuera de lo que la tarea toca": no define qué archivos puede tocar; obliga a inventar el conjunto permitido.
4. "Las semillas centrales (deskops/data/rules, runtime por defecto)": no enumera las 7 reglas ni identifica el runtime por defecto; obliga a inventar inventario.
5. "queden trackeadas y declaradas": no especifica dónde/cómo se declaran; obliga a inventar mecanismo.
6. "Implementation Path" vacío y `summary: ''`: no hay ruta ni dependencias; obliga a inventar plan y orden.

DRY-RUN
Lecturas: TaskDoc, `lifecycle.py`, `workspace.py`, `desk.py`, datos de `deskops/data/rules`, runtimes y tests existentes; estado git de un desk consumidor. Cambios previstos: aplicar el enfoque decidido para no escribir semillas sueltas, ajustar `advance`/`closeout` y añadir test de regresión. Dependencias: decisión de enfoque, fixture de desk consumidor y convención de test. Validaciones futuras: ejecutar el test nuevo y comprobar `git status` limpio salvo cambios declarados. Sin ejecutar.

FUTURO
Un humano o nodo de decisión elige la estrategia y el alcance permitido; el nodo de promoción fija nombre/ruta del test; el de validación ejecuta pruebas y revisa git status.
