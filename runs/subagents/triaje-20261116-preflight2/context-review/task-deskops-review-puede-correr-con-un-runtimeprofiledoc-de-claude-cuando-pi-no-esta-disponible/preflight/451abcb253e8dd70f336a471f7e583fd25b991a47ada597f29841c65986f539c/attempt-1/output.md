# REFORMULACION

**Propósito:** que `deskops review` (subcomandos `preflight|bundle|node`) pueda ejecutarse con un RuntimeProfileDoc cuyo binario sea `claude`, para que el coordinador dentro de la imagen scion-claude opere sin `pi`.

**Resultado:** rama de argv en `deskops/services/review.py` (~líneas 166-186) que para claude use modo no interactivo `-p`, modelo del perfil, system prompt del revisor, sin tools, sesión, contexto, skills ni MCP de usuario, con input por stdin; manifest registra binario, modelo y flags de aislamiento. Test unitario del argv sin invocar al modelo. Default sigue `runtime-pi-deepseek-flash`.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops`; toca `deskops/services/review.py`, `tests/test_review_command.py` y opcionalmente el runtime-profile `runtime-claude`.

**Límites:** no instalar pi, no cambiar el ritual context-review, no elegir modelo por defecto, no modificar `tests/test_review_doc.py`.

# AMBIGUEDADES

1. "el system prompt del revisor" — no se indica dónde vive ni su texto; obligaría a inventar la fuente o el literal.
2. "sin cargar contexto, skills ni MCP del usuario" — no se nombran flags concretos; obligaría a inventar la sintaxis exacta de claude.
3. "Se fijan los flags exactos leyendo `claude --help` en robocop2" vs. "El input va por stdin (no @ruta)" — tensión resuelta solo parcialmente; qué flag de stdin usa claude queda sin cita.
4. "model haiku" — identificador exacto de modelo no especificado; obligaría a inventar el string.
5. "alrededor de las lineas 166-186" — números de línea pueden haber derivado; obligaría a localizar por contenido.
6. "El RuntimeProfileDoc runtime-claude del desk de deskops" — no aclara si es el desk del repo real o el del sandbox `/dev/shm`; obligaría a elegir root.

# DRY-RUN

**Lecturas:** `review.py:150-200`, modelo RuntimeProfileDoc, `tests/test_review_command.py`, `claude --help` en robocop2. **Cambios previstos:** rama por binario pi/claude; construcción de argv (`-p`, `--model`, system prompt, flags de aislamiento, stdin); test de argv; posible `deskops edit/add runtime-profile`. **Dependencias:** claude instalado en robocop2, `.venv`, CLI deskops. **Validaciones futuras:** `pytest tests/test_review_command.py`, `pytest tests/test_review_doc.py`, suite completa con baseline en worktree `origin/main`, y corrida manual en sandbox `/dev/shm` guardando run_dir.

# FUTURO

Otro nodo/humano decide: aprobación del informe y evidencia, si se instala pi en scion, y qué modelo por defecto. No son ambigüedades de este encargo.
