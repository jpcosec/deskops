REFORMULACION
Propósito: dar a los acuerdos un campo propio de conversación (`conversation_ref`) en vez de reutilizar `provenance`. Resultado: campo opcional en `AtomDoc` e `InboxNoteDoc`; `--conv` en `deskops add atom` (alias de `--conversation-ref`) y en `deskops message send`; filtro `--conv` en `deskops list atoms` (y en json); rechazo de duplicado exacto con aviso en stderr y rc 1; tests, hashes de contrato, goldens de ayuda, `sldb models update` y commit con `Task-Id`. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: no toca `deskops/cli/commands/atoms.py` (alias viejos), no crea `add agreement`, no migra atoms antiguos; solo las rutas listadas en `files:`. Es una tarea ejecutable (`task.code`), no un agregado.

AMBIGUEDADES
1. «con la forma "<hilo>/<id de mensaje>" o solo "<hilo>"» — no se dice si se valida con patrón/validator pydantic ni qué pasa con un valor malformado; obligaría a inventar la política de validación.
2. «__template__ = ... provenance: ⸢optrev•provenance⸥» frente a «AtomDoc … e InboxNoteDoc … ganan conversation_ref» — no se indica si las plantillas ganan la línea opcional ni con qué marcador; obligaría a inventar plantilla.
3. «con --format json incluye el campo» — no aclara si el listado en texto también muestra `conversation_ref`; obligaría a inventar el formato de línea.
4. «ya existe <atom id> con conversation_ref <ref>» — no dice si `<ref>` es el valor tecleado o el almacenado (que difieren tras strip); obligaría a inventar el mensaje.
5. «así lo hace /mnt/ssd/proyectos/wf-desks/bin/desk-prompt.sh» — ese script no está en `files:` ni en scope; obligaría a decidir si se modifica otro repo.

DRY-RUN
Lecturas: los 14 archivos listados. Cambios previstos: p1 tests en `tests/test_atoms_cli.py`; p2 test en `tests/test_message_cli.py`; p3 modelos, `registry.py` (flags/alias y `--conv`), rama add de `operations.py` (duplicado), `operations.py`/`services/atoms.py` (filtro), `message.py` (payload); p4 hashes, goldens y `sldb models update AtomDoc/InboxNoteDoc` desde el worktree; p5 suite; p6 commit. Dependencias: store `.sldb`, `--pythonpath .`, `pytest-xdist` para `-n 4`, y `tests/test_output_goldens.py` (nombrado en p4, no en `files:`). Validaciones futuras: los cuatro comandos de la sección Validación. Sin ejecutar.

FUTURO
Dispatch entrega worktree y ejecuta el commit; un humano revisa el diff de goldens y decide sobre `desk-prompt.sh`; el orquestador valida cierre con `deskops doctor` y `sldb stores check`.
