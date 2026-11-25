## REFORMULACION
Nodo ejecutable (no agregado) para corregir en el repo `deskops` la alerta `lost` de `doctor`: debe indicar que la tarea se borró sin closeout y cómo repararla sin nombrar `desk update --apply`; el pie con `desk update --apply` solo aparecerá si aún hay alertas que ese comando registre. Además, un test debe cerrar una tarea real con `deskops closeout commit` en un desk temporal y verificar que `doctor` no reporta recibos `lost`. Límites: tocar `deskops/cli/commands/doctor.py`, `deskops/doctor_findings.py`, `tests/test_doctor_lost_receipts.py` y `CHANGELOG`; fuera: `closed_task_ids`. Resultado observable: tests `test_doctor_*.py` pasan, el texto ya no nombra `desk update --apply` y existe el test con closeout real.

## AMBIGUEDADES
1. “close it with deskops closeout resolved-by” frente a “test con closeout real … deskops closeout commit”: no queda claro si `resolved-by` es subcomando válido, alias o texto ilustrativo; obligaría a inventar la sintaxis canónica y qué debe ejecutar el test.
2. “solo se imprime si queda alguna alerta que ese comando sí registre”: no define qué alertas “registra” ni el predicado exacto; obligaría a inventar la condición.
3. “commit desde el worktree que dispatch te da”: el input no incluye ruta, rama ni worktree; obligaría a inventarlos.
4. “anotarlo en el run dir”: no se especifica el directorio de ejecución; obligaría a inventar ubicación y formato.
5. “Suite completa con -n 4 (instalar pytest-xdist si falta)”: no autoriza ni concreta instalación; obligaría a decidir método y entorno.
6. “CHANGELOG”: no indica ruta ni formato de entrada; obligaría a inventarlos.

## DRY-RUN
Lecturas previstas: TaskDoc, `doctor.py`, `doctor_findings.py`, `tests/test_doctor_lost_receipts.py`, tests `doctor_*`, `CHANGELOG` y estado del worktree. Cambios previstos: reescribir la alerta `lost`, condicionar el pie, añadir test con `deskops init`/add task/`closeout commit` en desk temporal y actualizar asserts. Dependencias: worktree de dispatch, CLI `deskops`, git, pytest y, si falta, `pytest-xdist`. Validaciones futuras: pytest focalizado, `deskops doctor --root /mnt/ssd/proyectos/SLDB_1/IR` en lectura, suite con `-n 4`, anotación en run dir y commit con `Task-Id`.

## FUTURO
Dispatch entrega el worktree; el runner ejecutará pruebas y `doctor`; un humano o CI revisará/aprobará el commit.
