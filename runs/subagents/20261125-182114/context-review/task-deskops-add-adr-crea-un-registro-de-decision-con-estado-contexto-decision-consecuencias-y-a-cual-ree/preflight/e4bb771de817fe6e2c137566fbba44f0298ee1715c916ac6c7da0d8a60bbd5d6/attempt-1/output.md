**REFORMULACION**

Propósito: incorporar ADR de primera clase en deskops para que las decisiones arquitectónicas tengan estado, contexto, consecuencias y reemplazo verificables. Resultado: `atom.adr` como subtipo de `AtomDoc` (solo agrega campos), alta vía `deskops add atom --atom-type`, reglas de aceptación y consistencia, relación `supersedes`, listado filtrado, materialización Markdown, cinco ADR cargados y manual. Repo: deskops (`SLDB_1/deskops`). Límites: no modificar el contrato/hash de `AtomDoc`, no crear interfaz, no migrar decisiones previas a las cinco indicadas, no federar ADR. Es un `task.code` ejecutable, no un agregado.

**AMBIGUEDADES**

1. «con una opción todos»: no se define nombre ni sintaxis de la opción; obliga a inventar el flag CLI.
2. «cuatro de sldb/docs/architecture/ y IR/docs/decisiones/paridad-por-capacidades.md»: faltan nombres de los cuatro archivos y la raíz de `IR/`; obliga a inventar rutas.
3. «recibo de owner para pasar a accepted»: no se especifica formato, origen ni validación del recibo; obliga a inventar evidencia y compuerta.
4. «los repos afectados van como tags repo:<nombre>»: no indica cómo determinar los repos afectados; obliga a inventar el criterio.
5. «con un cambio menor, se extiende eso y se deja escrito por qué»: «cambio menor» y dónde registrar el motivo no están definidos; obliga a fijar un umbral y un destino.

**DRY-RUN**

Lecturas: `deskops/models/task_types.py`, `deskops/models/atom.py`, implementación de `task.decision`, reglas sembradas, materialización y CLI de listado/alta. Cambios previstos: `AtomAdrDoc`, registro `ATOM_TYPE_MODELS`, `--atom-type`, filtros de listado, `supersedes`, reglas, materialización Markdown, manual y tests. Dependencias: `AtomDoc` estable, `RuleDoc`, `RelationTypeDoc`, mecanismo de recibos y materializador existentes. Validaciones futuras: `pytest tests/test_adr_artifact.py`, `pytest -q` y comprobaciones manuales del CLI y del hash. No se ejecuta nada.

**FUTURO**

Deciden humanos: aceptar los cinco ADR, emitir el recibo de owner y aprobar el manual. Otro nodo o revisión valida el diseño final y la consistencia global; el sistema aplica las reglas en tiempo de ejecución.
