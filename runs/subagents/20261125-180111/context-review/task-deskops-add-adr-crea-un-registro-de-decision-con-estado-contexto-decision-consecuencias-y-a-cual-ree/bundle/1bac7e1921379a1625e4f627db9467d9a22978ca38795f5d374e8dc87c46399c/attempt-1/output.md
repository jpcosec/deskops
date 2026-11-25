## REFORMULACION
Propósito: modelar una decisión de arquitectura como artefacto del desk, con estado, contexto, decisión, consecuencias y relación de reemplazo, operable por CLI. Resultado: `deskops add adr`, `list adrs`, `show` y `edit`; reemplazo que actualiza el estado anterior; listado por defecto de vigentes; cinco ADRs iniciales; `task.decision` puede citar un ADR como documento de cierre; manual del operador. Repo: deskops, con referencias a documentos de sldb e IR. Límites: fuera una interfaz y migrar decisiones antiguas más allá de las cinco indicadas. El cold-bundle solo aporta el TaskDoc y la instrucción; no incluye rituales, pills, átomos ni archivos nombrados, así que la reformulación se basa únicamente en el TaskDoc. Es un `task.code` ejecutable.

## AMBIGUEDADES
1. “add, list, show y edit” frente a “deskops add adr” y “deskops list adrs”: no se fija sintaxis, flags ni nombre de `show`/`edit`; obligaría a inventar la interfaz CLI.
2. “estado propuesto, aceptado o reemplazado”: no define transiciones ni quién las autoriza; obligaría a inventar una máquina de estados.
3. “Marcar que un ADR reemplaza a otro cambia el estado del anterior”: no dice a qué estado ni si el vínculo es recíproco; obligaría a inventar semántica de reemplazo.
4. “muestra por defecto solo los vigentes”: “vigentes” no está definido (¿aceptados?, ¿no reemplazados?); obligaría a inventar el filtro.
5. “que un task.decision pueda citar un ADR como su documento de cierre”: no indica campo, formato ni validación; obligaría a inventar el cambio de esquema.
6. “El formato de partida es el de sldb/docs/architecture/sldb-absorbs-kgdb.md”: el contenido no está en el bundle; obligaría a inventar campos si no se lee.
7. “tests/test_adr_artifact.py”: no se especifica su contenido ni cobertura; obligaría a inventar los casos.

## DRY-RUN
Lecturas hipotéticas: `deskops/models/task_types.py`, átomos de decisión, `review dispose`, el ADR de ejemplo y los cinco documentos citados; inspección del registro CLI y almacenamiento. Cambios previstos: tipo de artefacto ADR, comandos add/list/show/edit, relación de reemplazo, cita desde `task.decision`, pruebas y manual. Dependencias: modelo, registro CLI, persistencia y documentación. Validaciones futuras: `pytest -q tests/test_adr_artifact.py` y `pytest -q`. Sin ejecutar nada.

## FUTURO
Un humano decide las ambigüedades y aprueba el alcance. Otro nodo ejecuta la implementación y produce modelo, CLI, pruebas, ADRs iniciales y manual. Un nodo de validación ejecutará las pruebas indicadas.
