FALLA

# Resultado de testing

Task: `task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada`
Commit del ejecutor: `c0df7045058dc5c4ddd6d5f143f9fae4038cd47f`
Archivos del commit:
- `deskops/cli/commands/doctor.py`
- `deskops/doctor_findings.py`
- `tests/test_doctor_lost_receipts.py`

## Tests ejecutados

No hay `python` en PATH; usé el intérprete del venv de IR con `PYTHONPATH` al checkout de deskops. Corrí cada archivo por separado con `TMPDIR=/tmp`:

- `tests/test_doctor_lost_receipts.py`: 2 passed
- `tests/test_doctor_alerts.py`: 5 passed
- `tests/test_doctor_absolute_paths.py`: 14 passed
- `tests/test_doctor_model_registration.py`: 9 passed
- `tests/test_doctor_unmodeled_surfaces.py`: 4 passed

No hay `tests/test_doctor_findings.py`; los tests existentes del módulo/CLI tocado pasan.

## Fallo funcional

El criterio central del Goal/Done When no se cumple: los recibos `lost` preexistentes de tareas cerradas siguen alertando sin intervención manual.

`closed_task_ids()` en `deskops/doctor_findings.py` solo considera cerrada una tarea si algún commit tiene `Task-Id` **y además** trailer `Closeout-Mode` o `Run-Id`. No reconoce el cierre por el asunto canónico `closeout: <task-id>` (el que dejó fijado la resolución aceptada del preflight) ni un cierre registrado en el store. Por eso no suprime cierres históricos/legacy cuyo `Task-Id` falta, está abreviado o solo hay `Run-Dir`.

Evidencia sobre los desks reales (con el commit bajo prueba):

- IR: `doctor` todavía imprime **83** alertas `subject -> ...: lost`, de las cuales **81** corresponden a tareas que sí tienen un commit con asunto exacto `closeout: <task-id>`. Ejemplo:
  - tarea: `task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents`
  - commit de cierre: `89404705c8b44c4b317f03dc8dba8f7ac34e453b`
  - asunto: `closeout: task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents`
  - trailers: `Task-Id` + `Run-Dir`, sin `Closeout-Mode` ni `Run-Id`
  - `doctor` sigue listando sus recibos `bundle-1` / `evidence-commit-1` como lost.
- Deskops: quedan **44** alertas lost; **31** son de tareas con commit de asunto `closeout: <task-id>`. Ejemplo `task-cc31-ciclo-de-vida-declarado-efectos-en-relationdoc-attributes-y-advance-por-edges-holding`: el commit `4e79fbac` tiene el asunto correcto, pero su trailer es `Task-Id: task-cc31`, que no coincide con el id completo.

Esto contradice directamente: "Los recibos lost ya existentes de tareas cerradas ... dejan de alertar sin intervencion manual".

## Carencia del test nuevo

`tests/test_doctor_lost_receipts.py` no hace un closeout real ni usa el servicio de cierre: crea commits vacíos con trailers escritos a mano. Por eso su escenario solo cubre el formato moderno `Task-Id + Closeout-Mode/Run-Id` y no detecta el fallo anterior. El Done When pide "cerrar una tarea con recibos preflight/bundle y correr doctor".

## Hallazgo secundario del mensaje

El Done When pide que "el mensaje de la alerta restante no menciona desk update --apply salvo que ese comando la repare". La salida actual de la sección lost sí menciona literalmente:

    `deskops desk update --apply` does not repair these. ...

Aunque aclara que no lo repara, sigue nombrando el comando que el Done When pide no mencionar salvo que repare la alerta.
