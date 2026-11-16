## REFORMULACION

Encargo: retirar el camino de compatibilidad de `task_type` legacy en el repo `deskops` (cwd `/mnt/ssd/proyectos/SLDB_1/deskops`), una vez migrados sus consumidores (DK3). Resultado: desaparecen `LEGACY_TASK_TYPE_KEYS`, `migrate_task_types`, su llamada en `desk update` y los tests legacy; `desk update` deja de migrar `task_type`. Límites: solo `deskops/workspace.py`, `deskops/cli/commands/desk.py`, `tests/test_task_types.py`, `tests/test_task_lifecycle_validator.py` (casos legacy) y la frase de `docs/workflow-policy-reference.md`; no otros caminos legacy ni comportamiento nuevo. Requisito previo: dependencia externa en `closed`. Cierre: grep vacío, suite sin fallas nuevas, commit.

## AMBIGUEDADES

1. «! grep -rn 'LEGACY_TASK_TYPE\|migrate_task_types' deskops tests docs» frente a «Entra: deskops/workspace.py…». El patrón también casa `LEGACY_TASK_TYPE_MAP` y `canonical_task_type_name` (usados en `deskops/models/task_types.py`, no listado). Obliga a inventar si se borran también esos símbolos o solo el prefijo exacto.
2. «la funcion, la llamada y los tests legacy desaparecen» frente a `desk.py`, que importa y usa `pending_task_type_migration`, y a helpers `_task_type_migration_plan`, `_task_type_migration_line`, `_rewrite_task_type`. Obliga a decidir si quedan como código muerto (el grep no los cubre).
3. «una tarea con task_type viejo se trata como cualquier task_type desconocido hoy (el validador la reporta)» frente a `test_generic_task_doc_accepts_empty_legacy_or_any_task_type`, que afirma que `TaskDoc` acepta `"code"`. Obliga a inventar qué validador reporta y si `TaskDoc` debe cambiar.
4. «Casos legacy = los tests que nombran … un task_type viejo sin prefijo … como valor a migrar, p. ej. … alrededor de 177 y 290-303». «alrededor de» es vago y ese test nombra `"code"`/`"implementation"` pero espera aceptación, no migración. Obliga a decidir si se borra.
5. «la oracion … en su parte 'and migrates legacy task_type strings (...)'». Obliga a inventar la redacción final de la frase tras quitar el fragmento.

## DRY-RUN

Lecturas: los cinco archivos citados y los dos átomos. Cambios previstos (hipotéticos): quitar constante, función, import y llamada; borrar tests legacy; recortar la frase de la doc. Dependencias: `deskops show task … --root .` en `closed`; posible decisión sobre símbolos de `models/task_types.py`. Validaciones futuras, sin ejecutar: grep indicado, `tests/test_task_types.py`, `tests/test_task_lifecycle_validator.py`, `tests/test_cli.py`, suite completa con `-n 4` y baseline en worktree de `origin/main`. El átomo exige commit descriptivo.

## FUTURO

El ejecutor confirma la dependencia cerrada, decide el alcance real de símbolos y helpers, ejecuta las validaciones y registra fallas preexistentes; el humano/coordinador aprueba el informe y el commit.
