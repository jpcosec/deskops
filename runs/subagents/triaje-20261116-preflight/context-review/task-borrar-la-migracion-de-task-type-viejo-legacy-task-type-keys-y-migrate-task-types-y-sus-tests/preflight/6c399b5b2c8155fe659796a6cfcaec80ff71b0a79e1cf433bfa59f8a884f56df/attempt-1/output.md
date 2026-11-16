## REFORMULACION
Propósito: retirar el camino de compatibilidad de `task_type` viejo en deskops cuando sus consumidores ya migraron (DK3). Resultado: eliminar `LEGACY_TASK_TYPE_KEYS` (`deskops/workspace.py:520`), `migrate_task_types` (`:712`), su llamada en `deskops/cli/commands/desk.py:452` y los tests legacy, de modo que `desk update` ya no migre `task_type` viejos. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límites: solo `deskops/workspace.py`, `deskops/cli/commands/desk.py`, `tests/test_task_types.py`, `tests/test_task_lifecycle_validator.py` (casos legacy) y `docs/workflow-policy-reference.md` (frase de migración); fuera: otros caminos legacy. Cierre: grep vacío y suite sin fallas nuevas.

## AMBIGUEDADES
1. «Confirmar que la dependencia externa cerro»: no indica cómo verificarlo (estado, commit, ejecución). Obligaría a inventar el criterio de cierre.
2. «tests/test_task_lifecycle_validator.py (casos legacy)»: no identifica qué casos. Obligaría a inventar cuáles son legacy.
3. «docs/workflow-policy-reference.md (la frase de migracion)»: no cita el texto exacto. Obligaría a inventar qué frase borrar.
4. «sin fallas nuevas respecto de main»: no fija rama/commit base ni método de comparación. Obligaría a inventar el baseline.
5. «desk update ya no migra task_type viejos»: no dice el comportamiento sustituto (ignorar, error, aviso). Obligaría a inventar la semántica posterior.

## DRY-RUN
Lecturas: `workspace.py` (520, 712), `desk.py:452`, ambos tests, doc citado. Cambios previstos: borrar mapa, función, llamada, casos legacy y frase. Dependencias: `task-traderbot-y-sldb-migran-sus-task-type-viejos-con-deskops-desk-update-apply` cerrada. Validaciones futuras: grep sin coincidencias, pytest de `test_task_types.py`, `test_task_lifecycle_validator.py`, `test_cli.py` y suite completa (`-n 4`) sin fallas nuevas. Sin ejecutar nada.

## FUTURO
Otro nodo/humano confirma el cierre de la dependencia y define el baseline `main`; la decisión sobre comportamiento sustituto de `desk update` y la identificación exacta de casos/frase corresponden a quien planifica o al ejecutor autorizado, no a esta revisión.
