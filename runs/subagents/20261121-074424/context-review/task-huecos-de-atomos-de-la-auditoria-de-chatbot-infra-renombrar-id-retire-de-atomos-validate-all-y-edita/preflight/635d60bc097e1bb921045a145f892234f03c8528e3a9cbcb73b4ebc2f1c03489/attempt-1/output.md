## REFORMULACION

Encargo ejecutable (`task.debug`) en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`: cerrar los huecos 1, 3, 4, 5 y 6 de la auditoría de Chatbot_Infra. Propósito: para cada hueco, registrar un recibo de reproducción (o constancia de no reproducción con comando y salida) y, si se reproduce, corregirlo con test. Resultado: `atoms rename` transaccional que reescribe referencias vía `sldb rewrite_references`; verbo `atoms retire` que falla con referencias entrantes; `validate --all` sin falsos positivos; un verbo para editar `desk/contexts/pills.md`; `doctor` resolviendo el store enlazado tras mover el workspace. Límites: no citas código→átomo ni repos AntonIA; un sandbox en `/dev/shm` por hueco, borrado al final; un commit por corrección.

## AMBIGUEDADES

1. "no hay verbo para editar desk/contexts/pills.md" — no define nombre, sintaxis ni semántica del verbo; obligaría a inventar la interfaz CLI.
2. "validate --all sin falsos positivos" — no define qué cuenta como falso positivo ni criterio de éxito; obligaría a inventar una taxonomía de hallazgos.
3. "deskops atoms retire <id> --reason <texto> --root ." — no indica el efecto (¿borrar archivo, marcar `status: retired`, mover?); obligaría a inventar la semántica del retiro.
4. "test_atom_materialization.py para rename y retire, test_doctor*.py para el 6" — no asigna archivo de test a los huecos 4 y 5; obligaría a inventar su ubicación.
5. "copiar un desk con store enlazado a deskops a otra profundidad" — no dice cómo construir ese store enlazado ni qué se copia; obligaría a inventar el setup.
6. "registrar `deskops review record <tarea> --kind reproduction`" — no indica cómo adjuntar comando y salida; obligaría a inventar el formato.

## DRY-RUN

Lecturas: TaskDoc, `deskops/services/atoms.py`, `deskops/cli/registry.py`, `deskops/cli/commands/doctor.py`, `tests/test_atom_materialization.py`, pill de ciclo de vida, tarea del drawer. Cambios previstos: rename con validación `^atom-[a-z0-9-]+$`, error si el id existe y reescritura transaccional; nuevo verbo retire con chequeo de referencias; corrección de resolución de provenance en `validate --all`; verbo de edición de pills; resolución del store enlazado en doctor; tests por hueco. Dependencias: API de sldb, `.venv`, `/dev/shm`, `git init` + `deskops init` en cada sandbox. Validaciones futuras: reproducción por hueco, `review record`, los tres pytest indicados, suite completa con worktree base para fallas preexistentes, e informe con esa lista.

## FUTURO

Un humano decide la interfaz del verbo de edición de pills, la semántica exacta de "retire" y el formato del recibo. Otro nodo ejecuta y entrega commits; la revisión acepta o rechaza fallas preexistentes y el informe.
