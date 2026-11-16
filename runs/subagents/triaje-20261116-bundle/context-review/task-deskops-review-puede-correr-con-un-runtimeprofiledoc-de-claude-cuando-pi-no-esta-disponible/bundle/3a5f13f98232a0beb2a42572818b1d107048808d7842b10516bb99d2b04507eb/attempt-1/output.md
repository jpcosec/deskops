REFORMULACION
El nodo debe hacer que `deskops review preflight|bundle|node --engine <perfil>` funcione con un `RuntimeProfileDoc` cuyo binario sea `claude`, manteniendo `runtime-pi-deepseek-flash` como default. El resultado esperado es una rama de argv en `deskops/services/review.py` que invoque claude en modo no interactivo (`-p`), con el modelo del perfil, el system prompt del revisor, sin tools, sin sesión persistida y sin contexto, skills ni MCP del usuario; el input irá por stdin o archivo según acepte claude. El manifest debe registrar binario, modelo y flags de aislamiento. Se modifican `review.py`, el perfil `runtime-claude` si procede y `tests/test_review_command.py`; `tests/test_review_doc.py` solo se ejecuta. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Fuera de alcance: instalar pi, cambiar el ritual context-review y elegir modelo por defecto.

AMBIGUEDADES
1. “sin sesion persistida y sin cargar contexto, skills ni MCP del usuario” no nombra flags. Sin `claude --help` en el input, obliga a inventar qué flags de claude producen ese aislamiento.
2. “El input va por stdin (no @ruta)” contradice parcialmente “por stdin o por archivo segun lo que acepte claude”. Obliga a decidir si stdin es obligatorio y cómo se combina con modelo/system prompt.
3. “El manifest registra binario, modelo y flags de aislamiento igual que con pi”: el manifest actual guarda `argv`, `model` global y `profile`, no claves explícitas de binario/flags. Obliga a inventar el esquema.
4. “binary claude, model haiku” no fija el identificador exacto del modelo ni si se crea o edita el perfil. Obliga a inventar el valor válido de modelo.
5. “se acepta si output.md trae las secciones REFORMULACION, AMBIGUEDADES y DRY-RUN”, pero `technical_ok` solo exige `REFORMULACION`. Obliga a decidir si se cambia la validación o es criterio humano.

DRY-RUN
Lecturas: `review.py` alrededor de 150-200, modelo `RuntimeProfileDoc`, `tests/test_review_command.py`, perfiles en `desk/runtimes/` y `claude --help` en robocop2. Cambios: rama por binario en `_argv`; argv claude con `-p`, modelo, system prompt, aislamiento y entrada por stdin; manifest con binario/modelo/flags; test unitario del argv sin llamar al modelo. Dependencias: claude instalado en robocop2, perfil `runtime-claude` y CLI deskops. Validaciones: los tres comandos pytest declarados; prueba manual en sandbox `/dev/shm` con `git init`, `deskops init` y evidencia en `run_dir`. Sin ejecutar nada.

FUTURO
Un humano u operador ejecuta la prueba manual en robocop2 y decide si la evidencia es aceptable; el repo scion instala pi en su imagen, fuera de este nodo.
