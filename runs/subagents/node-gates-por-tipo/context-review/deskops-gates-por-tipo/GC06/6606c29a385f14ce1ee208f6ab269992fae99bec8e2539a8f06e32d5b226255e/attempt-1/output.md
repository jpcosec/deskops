REFORMULACION
Propósito: cerrar las vías de escape del ciclo de vida en deskops retirando `advance --to` y limitando `edit task`. Resultado: `advance --to` falla como error de uso (exit 2), el help no lo muestra; `edit task` rechaza `status`, `current_node`, `task_type`, `closeout_evidence` e `history` con exit 1 y mensaje que indica quién escribe cada campo; el resto sigue editable; se actualizan goldens, tests, manual, CHANGELOG y se hace ack del inbox. Repo dueño: deskops. Límites: solo `output_scope`; sin tocar sldb; sin banderas de salto; sin cambiar la autoridad de cierre; depende de GC01.

AMBIGUEDADES
1. “cada uso documentado se reemplaza: cerrar → closeout commit; superseded → closeout supersede”. El `output_scope` no incluye comandos de closeout y la aceptación no prueba `superseded`; obliga a decidir si hay que implementar `closeout supersede` o solo documentarlo, pudiendo exceder alcance.
2. “con un error que dice quién escribe cada campo (advance y closeout; add task para task_type)” frente a “lo mismo para current_node, task_type, closeout_evidence e history”. No se asigna escritor explícito a `history` ni se fija si “lo mismo” exige nombrar el escritor exacto en cada mensaje; obliga a inventar la atribución.
3. “se cierra con ack” sin formato ni criterio de aceptación; obliga a inventar el contenido del ack.

DRY-RUN
Leería dag, brief, alcance, decisiones y los archivos de `output_scope`. Quitaría `--to` del parser/help en `registry.py`, su rama en `tasks.py` y ajustaría `edit_artifact_field`/comando para rechazar los cinco campos con error de dominio. Actualizaría goldens de ayuda, `tests/test_cli.py`, `test_cli_help_examples.py`, `docs/operator-manual.md`, CHANGELOG breaking y el ack. Dependencia: GC01 cerrado; sin sldb. Validaría hipotéticamente con pytest, comandos `advance --to` y `edit task` (exit 2/1), edición de `goal`, grep de `--to` y comparación de goldens.

FUTURO
GC08 alineará rituales y documentación más amplia; el dueño valida el CHANGELOG breaking, el ack y la disposición de la revisión en frío.
