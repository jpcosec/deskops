## REFORMULACION

**Propósito:** eliminar el camino de compatibilidad de `task_type` ya migrado: el mapa `LEGACY_TASK_TYPE_KEYS` (deskops/workspace.py:520), la función `migrate_task_types` (:712), su llamada en deskops/cli/commands/desk.py:452, los tests legacy y la frase de migración en docs/workflow-policy-reference.md:75.

**Resultado:** `grep -rn 'LEGACY_TASK_TYPE\|migrate_task_types' deskops tests docs` vacío y suite sin fallas nuevas; `desk update` deja de migrar `task_type` viejos.

**Repo:** /mnt/ssd/proyectos/SLDB_1/deskops.

**Límites:** no tocar otros caminos legacy; no añadir comportamiento nuevo (un `task_type` viejo pasa a tratarse como desconocido y el validador lo reporta). Precondición: dependencia externa cerrada.

## AMBIGUEDADES

1. «la dependencia externa esta cerrada cuando `deskops show task task-traderbot-... --root .` da status closed» — no fija qué ejecutable `deskops` (¿venv?), desde qué cwd ni qué hacer si el comando falla; obligaría a inventar binario y política de fallo.
2. «tests en tests/test_task_types.py:107 y 149» y «alrededor de 177 y 290-303» — líneas aproximadas; obligaría a inventar el criterio exacto de qué bloques son casos legacy.
3. «un task_type viejo sin prefijo (code, implementation, test, docs, spec, design, external, vacio)» — lista posiblemente no exhaustiva y «vacio» ambiguo; obligaría a decidir si otros valores cuentan.
4. «la oracion ... linea 75 que empieza con 'A desk adds its own subtypes' en su parte 'and migrates legacy task_type strings (...)'» — la línea puede desplazarse; obligaría a inventar el método de localización textual.

## DRY-RUN

**Lecturas:** workspace.py:520 y :712; desk.py:452; tests citados; doc:75; comprobar dependencia con `deskops show ... --root .`.

**Cambios previstos:** borrar mapa, función, llamada, tests legacy y oración de la doc.

**Dependencias:** tarea externa en `closed`.

**Validaciones futuras (no ejecutadas):** grep vacío; pytest de test_task_types.py, test_task_lifecycle_validator.py, test_cli.py; suite completa `-n 4`; fallas comparadas contra `git worktree add /dev/shm/wt-base origin/main` y listadas en el informe.

## FUTURO

El nodo externo (traderbot/sldb) debe cerrar la dependencia; un ejecutor correrá borrado y validaciones; un humano decidirá la aceptación de fallas preexistentes y el cierre de la tarea.
