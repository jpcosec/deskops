**REFORMULACION**
Nodo ejecutable `task.code`, no agregado. Propósito: convertir una decisión de arquitectura en un subtipo de átomo, `atom.adr`, con estado, contexto, consecuencias y relación de reemplazo. Resultado: modelo `AtomAdrDoc`, registro de tipos, CLI `deskops add atom --atom-type`, listado filtrado, arista `supersedes`, reglas, materialización Markdown, manual y cinco ADR cargados. Repo: `deskops`; el input menciona además rutas de `sldb` e `IR`. Límites: no modificar `AtomDoc` ni su hash, no crear interfaz, no migrar decisiones anteriores, no federar ADR entre desks.

**AMBIGUEDADES**
1. “las cinco del 2026-11-25 (cuatro de sldb/docs/architecture/ y IR/docs/decisiones/paridad-por-capacidades.md)”: no nombra los cuatro ADR ni cómo resolver `IR/` desde `deskops`; obliga a inventar rutas y títulos.
2. “pron-is-archived reemplazando la sección de pron del ADR sldb-absorbs-kgdb”: `supersedes` es ADR a ADR, pero aquí se reemplaza una sección; obliga a inventar supersesión parcial o una edición no modelada.
3. “se lista filtrando los vigentes” frente a “por defecto solo los accepted”: no define si `proposed`, `rejected` o `superseded` son “vigentes”; obliga a inventar el criterio.
4. “Si al leer aparece que task.decision, los átomos de decisión o review dispose ya cubren […] con un cambio menor, se extiende eso”: no fija qué es “cambio menor” ni cobertura suficiente; obliga a decidir sin criterio.
5. “alternatives (opcional) y not_verified (opcional)” frente a la lista materializada “Status, Date, Decision Maker, Supersedes, Context, Decision y Consequences”: no dice si las opcionales se renderizan; obliga a inventarlo.

**DRY-RUN**
Lecturas: `deskops/models/task_types.py`, `atom.py`, reglas y activación de `task.decision`, materialización y tests; ADR fuente citados. Cambios previstos: modelos/registro, CLI add/list, `RelationTypeDoc supersedes`, `RuleDoc`, materializador, manual, datos y test `test_adr_artifact.py`. Dependencias: contrato/hash de `AtomDoc` intacto, motor de reglas y CLI existentes. Validaciones futuras: ejecutar los dos `pytest`, comprobar rechazo de estado/recibo, supersesión, listado y Markdown; no se ejecuta ahora.

**FUTURO**
Un humano debe confirmar los cinco ADR fuente y la política de recibo de owner. Otro nodo ejecutará tests y materialización; este revisor no produce cambios.
