## REFORMULACION
Encargo ejecutable de tipo `task.code` en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Propósito: corregir en `doctor` la alerta `lost` restante (tarea borrada sin closeout) para que indique restaurar desde git o cerrar con `closeout`, sin nombrar `desk update --apply`, y condicionar el pie que sugiere `desk update --apply` a que existan alertas que ese comando realmente registre. Resultado: texto corregido, test con `closeout commit` real en desk temporal, asserts actualizados y suite de doctor pasando. Límites: fuera `closed_task_ids`; incluye `doctor.py`, `doctor_findings.py`, `tests/test_doctor_lost_receipts.py` y `CHANGELOG`; commit final con trailer `Task-Id`.

## AMBIGUEDADES
1. «cierra con `deskops closeout resolved-by`» (Goal) frente a «closeout commit» (Rationale/p2). Obliga a inventar el subcomando y sintaxis correctos.
2. «solo se imprime si queda alguna alerta que ese comando sí registre». No se define qué alertas registra `desk update --apply`; obliga a inferir su semántica.
3. «commit desde el worktree que dispatch te da». No hay ruta, rama ni formato de mensaje; obliga a inventarlos.
4. Validación pide solo dos archivos, pero Done When exige `tests/test_doctor_*.py` y p5 la suite completa. Obliga a decidir el alcance mínimo.
5. «anotarlo en el run dir». No se especifica archivo ni formato del registro.
6. «instalar pytest-xdist si falta». No se indica método, entorno ni permisos.
7. Scope incluye `CHANGELOG` sin decir qué entrada añadir.

## DRY-RUN
Sin ejecutar: leer `doctor.py`, `doctor_findings.py`, `tests/test_doctor_lost_receipts.py`, tests de alertas y `CHANGELOG`. Cambiar texto de la sección lost, condicionar el pie de `update --apply`, añadir test que inicialice desk temporal, cree tarea y haga `closeout commit` real, y actualizar asserts del texto viejo. Dependencias: comando closeout, git, pytest y xdist. Validaciones futuras: tests indicados, `deskops doctor --root /mnt/ssd/proyectos/SLDB_1/IR` en lectura, suite completa con `-n 4`, y commit con `Task-Id`.

## FUTURO
Dispatch entrega worktree y Task-Id; un humano aclara el nombre real de closeout y aprueba instalación de dependencias; otro nodo o el run dir recibe la evidencia del doctor sobre IR y el resultado de la suite.
