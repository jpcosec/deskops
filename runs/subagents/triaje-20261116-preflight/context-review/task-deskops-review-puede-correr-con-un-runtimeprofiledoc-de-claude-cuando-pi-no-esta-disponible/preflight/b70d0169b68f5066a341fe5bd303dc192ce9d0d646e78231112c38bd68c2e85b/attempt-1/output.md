## REFORMULACION
**Propósito:** que `deskops review` funcione con un RuntimeProfileDoc de claude cuando pi no está disponible, como ocurre en la imagen scion-claude. **Resultado:** rama de argv para claude en `deskops/services/review.py`, perfil `runtime-claude` ajustado si hace falta, test del argv y una corrida manual con recibo. **Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`. **Límites:** no instalar pi en la imagen, no cambiar el ritual `context-review`, no elegir modelo por defecto; el default sigue siendo `runtime-pi-deepseek-flash`. Es una tarea ejecutable, no un agregado; no hay hijos que recorrer.

## AMBIGUEDADES
1. «el RuntimeProfileDoc runtime-claude del desk de deskops si hay que ajustar sus campos»: no define qué campos ni cuándo ajustarlos; obligaría a inventar la condición y los valores.
2. «Se fijan los flags exactos leyendo `claude --help` en robocop2»: no indica acceso, disponibilidad ni versión esperada de robocop2; obligaría a inventar el entorno de consulta.
3. «el input se entrega por stdin o por archivo segun lo que acepte claude»: deja abierta la elección concreta; obligaría a inventar el criterio y el formato exacto.
4. «en un desk sandbox»: no identifica ruta, creación ni contenido del sandbox; obligaría a inventar el montaje de prueba.
5. «guardando la salida del run como evidencia»: no especifica formato, ubicación ni criterio de aceptación del recibo; obligaría a inventar el artefacto.
6. Validación incluye `tests/test_review_doc.py`, pero alcance y archivos solo nombran `tests/test_review_command.py`; obligaría a inventar si ese test debe modificarse o solo ejecutarse.

## DRY-RUN
Un ejecutor futuro leería `review.py:150-200`, el modelo RuntimeProfileDoc, los tests existentes y `claude --help` en robocop2. Luego ramificaría el argv: pi actual y claude con `-p`, `--model`, system prompt, flags de aislamiento, sin tools, sesión, contexto, skills ni MCP, y decidiría stdin/archivo. Ajustaría el perfil `runtime-claude` mediante `deskops edit runtime-profile` solo si los campos lo requieren. Añadiría un test unitario del argv sin llamar al modelo. Dependencias: binario claude, acceso a robocop2, sandbox y perfil. Validaciones previstas: pytest de `test_review_command.py`, `test_review_doc.py`, suite completa con `-n 4`, y corrida manual `deskops review preflight <tarea> --engine runtime-claude --root .` guardando recibo. Nada se ejecuta aquí.

## FUTURO
El ejecutor futuro produce el diff, los tests y la evidencia manual. Un validador o humano decide si el recibo demuestra engine `runtime-claude` y salida con secciones del revisor, y si no hay fallas nuevas respecto de `main`.
