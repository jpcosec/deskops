## REFORMULACION

El nodo es una tarea ejecutable (`task.code`), no un agregado. Propósito: que los contenedores de scion usados por los roles executor y tester dispongan de `pytest-xdist`, evitando ejecuciones de más de una hora sin paralelismo. Resultado esperado: el venv del contenedor incluye xdist —en la imagen o en la preparación del runtime template— y el prompt de ambos roles ejecuta la suite completa con `-n 4`. Repo: `deskops` (worktree entregado por dispatch), con superficie en `deskops/templates`, `desk/roles` y el test correspondiente. Límites: dentro, el runtime template o imagen de scion de deskops y su test; fuera, el resto.

## AMBIGUEDADES

1. “en la imagen o en el paso de preparación del runtime template de scion”: no fija la capa concreta; obligaría a inventar si se modifica Dockerfile/imagen, template o ambos.
2. “el prompt de esos roles corre la suite completa con -n 4”: no identifica archivos ni texto exacto de los prompts; obligaría a inventar dónde y cómo modificar executor/tester.
3. “test o comprobación de que python -c 'import xdist' funciona en un contenedor lanzado con el template”: no define ubicación, framework ni mecanismo de lanzamiento; obligaría a inventar el test y su automatización.
4. “TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py”: única validación declarada, no cubre xdist ni contenedores; obligaría a inventar si basta o si se añaden comprobaciones.

## DRY-RUN

Lecturas: templates de scion en `deskops/templates`, configuración/prompts en `desk/roles`, `tests/test_dispatch.py` y referencias a `venv`/`pip install`. Cambios previstos: añadir `pytest-xdist` al mecanismo de construcción del venv; ajustar prompts de executor y tester para `-n 4`; añadir test/comprobación de importación de xdist. Dependencias: construcción/arranque de contenedor scion, disponibilidad de paquete pip, worktree de dispatch y suite existente. Validaciones futuras: ejecutar el comando de Validation, lanzar contenedor e importar xdist, correr suite con `-n 4`, y commit con `Task-Id`.

## FUTURO

Dispatch entrega el worktree; el entorno de ejecución construye/lanza el contenedor; un revisor humano valida la evidencia y decide aceptar el cierre.
