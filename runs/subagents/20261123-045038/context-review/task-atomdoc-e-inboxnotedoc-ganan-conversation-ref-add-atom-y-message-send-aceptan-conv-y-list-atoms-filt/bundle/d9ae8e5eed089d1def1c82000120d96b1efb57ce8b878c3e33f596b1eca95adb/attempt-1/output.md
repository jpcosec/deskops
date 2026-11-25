# REFORMULACION

**Propósito:** dar a los acuerdos un campo propio de conversación en vez de sobrecargar `--provenance` y el texto del átomo.
**Resultado:** `AtomDoc` e `InboxNoteDoc` con `conversation_ref: str | None = None`; `add atom --conv`, `message send --conv` lo escriben; `list atoms --conv` filtra por hilo (prefijo `<hilo>/` incluido) y lo expone en JSON; `add atom` rechaza un `--conv` ya usado.
**Repo:** `/mnt/ssd/proyectos/SLDB_1/deskops` (modelos, CLI, goldens, tests).
**Límites:** fuera un verbo `add agreement` y migrar átomos antiguos con la referencia en provenance.

# AMBIGUEDADES

1. "`deskops list atoms --conv <hilo>`" frente al código real, que enruta `deskops atoms list`; ¿qué superficie exacta se añade? Obliga a inventar el árbol de argparse.
2. "vacío no se escribe": no define si `""`, `None` o solo espacios cuentan como vacío. Obliga a inventar normalización.
3. "lista solo los atoms cuyo conversation_ref es ese hilo o empieza por `<hilo>/`": no aclara si `--conv` compara literal o normaliza `#`. Obliga a inventar la semántica del prefijo.
4. "un `--conv` que ya tiene otro atom": no dice si el duplicado es por ref exacta o por hilo. Obliga a inventar el criterio.
5. "avisa en stderr ... (sale con código 1)": el CLI existente usa `render_error` con `--format`; no dice si JSON cambia la salida. Obliga a inventar el contrato de error.
6. "los goldens de contrato y de ayuda": no nombra archivos ni rutas, y `files:` no los lista. Obliga a inventar qué se regenera.
7. "sldb models update de los dos modelos en el store del desk": no fija `.sldb` concreto ni el `--pythonpath`. Obliga a inventar el store objetivo.

# DRY-RUN

**Lecturas:** los seis archivos de `files:`, goldens y `.sldb` (índices de modelos/documentos).
**Cambios previstos:** campo + descripción en ambos modelos; `--conv` en los dos parsers y paso al payload; filtro en `list_atoms`; comprobación de duplicado antes de crear; plantillas; tests p1–p3; goldens; `models update`.
**Dependencias:** `render`/`render_error`, `DeskopsOperations`, `validate_model_input_roundtrip`, `transaction`.
**Validaciones futuras:** los cuatro `pytest` del TaskDoc, más `deskops doctor --root .` y `sldb stores check --store .sldb` (Done When).

# FUTURO

`dispatch` entrega el worktree; otro nodo ejecuta el commit con trailer `Task-Id: <id>`; la actualización del store y los goldens requieren escritura real; la aceptación final (y cualquier decisión sobre formato de hilo) es de JP/revisión humana.
