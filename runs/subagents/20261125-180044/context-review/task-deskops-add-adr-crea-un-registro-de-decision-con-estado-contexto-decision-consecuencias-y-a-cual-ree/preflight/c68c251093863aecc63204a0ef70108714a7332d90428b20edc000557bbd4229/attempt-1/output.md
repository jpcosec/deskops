## REFORMULACION

Encargo ejecutable `task.code`: añadir a deskops un artefacto ADR modelado, con estado (propuesto/aceptado/reemplazado), contexto, decisión, consecuencias y relación de reemplazo. Debe existir CLI `deskops add adr`, `list adrs`, `show` y `edit`; `list adrs` muestra por defecto solo vigentes; marcar reemplazo cambia el estado del anterior; `task.decision` puede citar un ADR como documento de cierre. Antes de modelar hay que auditar cómo registran decisiones `task.decision`, los átomos de decisión y `review dispose`, y documentar por qué no bastan; si uno cubre el caso con cambio menor, se extiende y no se crea tipo. Se cargan cinco ADR iniciales y se actualiza el manual del operador. Repo: deskops, con documentos fuente en sldb e IR. Límite: no interfaz gráfica ni migración histórica más allá de esos cinco.

## AMBIGUEDADES

1. “si uno de ellos lo cubre con un cambio menor, se extiende ese y no se crea un tipo” frente a “un tipo de artefacto nuevo”: el criterio de “cambio menor” no está definido; obliga a inventar el umbral de decisión.
2. “IR/docs/decisiones/paridad-por-capacidades.md”: no se indica la raíz del repo IR ni si la ruta es relativa a deskops; obliga a inventar la resolución.
3. “deskops list adrs muestra por defecto solo los vigentes”: no se define si “vigente” incluye `propuesto`, solo `aceptado`, o ambos; obliga a inventar semántica de estado.
4. “cuatro de sldb/docs/architecture/ (mechanism-in-sldb-content-in-specir, ...)”: faltan extensiones y rutas completas; obliga a inventar nombres de archivo.
5. “El manual del operador”: no se indica archivo ni ubicación; obliga a inventar destino.
6. “que un task.decision pueda citar un ADR como su documento de cierre”: no se especifica campo, formato ni validación; obliga a inventar el contrato.
7. “dejar escrito en la tarea por qué ninguno cubre…”: no queda claro si se edita esta TaskDoc o se produce otro documento; obliga a inventar el soporte.

## DRY-RUN

Lecturas previstas: `deskops/models/task_types.py`, definición de átomos de decisión, implementación de `review dispose`, `sldb/docs/architecture/sldb-absorbs-kgdb.md` y los cinco documentos fuente. Cambios previstos: modelo y validaciones ADR; comandos `add/list/show/edit`; relación de reemplazo y transición de estado; referencia desde `task.decision`; tests `tests/test_adr_artifact.py`; manual; carga inicial de cinco ADR. Dependencias: framework CLI, capa de modelos/artefactos, docs de sldb e IR. Validaciones futuras: los dos `pytest` indicados y comprobación manual de CLI/estados.

## FUTURO

Un ejecutor producirá modelo, CLI, tests, manual y ADR iniciales. Un humano decidirá si se extiende un mecanismo existente o se crea tipo nuevo, aprobará el contenido de los cinco ADR y confirmará la semántica de “vigente” y las rutas fuente.
