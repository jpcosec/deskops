FALLA

# Resultado de testing

Task: `task-doctor-no-alerta-como-lost-los-recibos-de-una-tarea-cerrada`
Commit evaluado: `91f44d0d1710c2c428d5edebb8a9e8424c42f89f` (intento 2, sobre `c0df7045058dc5c4ddd6d5f143f9fae4038cd47f`, intento 1)
Archivos del commit 91f44d0d:
- `deskops/doctor_findings.py`
- `tests/test_doctor_lost_receipts.py`

## Entorno

No hay `python` en PATH. Usé `/workspace/sldb/.venv/bin/python` (Python 3.13.18, pytest 9.1.1),
que importa `deskops` desde `/mnt/ssd/proyectos/SLDB_1/deskops` (HEAD `c60b476e`, árbol de
`91f44d0d`). Todos los tests se corrieron con `TMPDIR=/tmp`, de a un archivo.

## Tests ejecutados

- `tests/test_doctor_lost_receipts.py`: 3 passed
- `tests/test_doctor_alerts.py`: 5 passed
- `tests/test_doctor_absolute_paths.py`: 14 passed
- `tests/test_doctor_model_registration.py`: 9 passed
- `tests/test_doctor_unmodeled_surfaces.py`: 4 passed

Total: 35 passed, 1 warning. No existe `tests/test_doctor_findings.py`; los tests del módulo/CLI
tocado y los `tests/test_doctor_*.py` pasan.

## Verificación funcional: el fallo del intento 1 sí queda corregido

- `closed_task_ids()` reconoce ahora el asunto exacto `closeout: <task-id>` (y la variante con
  ` [skip ci]`), comparando el id completo: `task-subj-other` no se considera cerrada por
  `closeout: task-subj`. El test nuevo lo cubre y pasa.
- IR (solo lectura): con la lógica de `c0df7045` (solo trailers) `doctor` dejaba 83 alertas
  `lost`; con `91f44d0d` deja 0. `deskops doctor --root /mnt/ssd/proyectos/SLDB_1/IR` termina
  `Desk is healthy, with 6 alert(s).` y no imprime ninguna línea de recibos `lost`.
- El commit de ejemplo `89404705` (`closeout: task-fixture-mount-copy-de-las-pruebas-copia-los-rundoc-de-runs-subagents`)
  ya no produce alertas `lost` para sus recibos.

## Criterios que siguen sin cumplirse

1. **Done When: el mensaje de la alerta restante no debe mencionar `desk update --apply` salvo
   que ese comando la repare.** La sección de recibos `lost` sigue imprimiendo literalmente:

       `deskops desk update --apply` does not repair these. Restore the task, or close it with `deskops closeout commit` ...

   y el test nuevo lo fija con `assert "does not repair these" in out`. Como el comando no repara
   esas alertas, no debía nombrarse. La resolución aceptada (preflight-2 / bundle-1) pedía que la
   alerta `lost` restante dijera `the task was deleted without closeout: restore it from git or
   close it with deskops closeout resolved-by`, y que el pie `register ... with: deskops desk update
   --apply` solo se imprimiera si queda alguna alerta que ese comando sí registre; el texto actual
   no es ese.

2. **Validation: test nuevo con closeout real y doctor.** Los tests siguen usando commits vacíos
   sintéticos (`git commit --allow-empty`) en vez de cerrar una tarea con `deskops closeout commit`
   y recibos preflight/bundle reales. El test de asunto cubre la regresión nueva, pero no el flujo
   de cierre real que pide la Validation / bundle-1 p1.

3. **Resolución aceptada (preflight-2, punto 2):** `doctor` debía imprimir una línea informativa
   `N receipts of closed tasks (history, not alerts)`. El código actual descarta esos recibos en
   silencio: en IR (293 recibos suprimidos) no aparece esa línea.

4. **Resolución aceptada (bundle-1 p3):** falta la entrada en `CHANGELOG.md`. El commit solo toca
   `deskops/doctor_findings.py` y el test.

5. Divergencia menor: preflight-2 pedía el test en `tests/test_doctor_alerts.py`; está en
   `tests/test_doctor_lost_receipts.py`.

## Conclusión

El bug principal (no reconocer el cierre por asunto `closeout: <task-id>`) está corregido y la
suite `doctor` pasa, pero el Done When y la resolución aceptada siguen incumplidos: el mensaje de
la alerta `lost` todavía menciona `desk update --apply`, y faltan el test con closeout real, la
línea informativa de recibos históricos y la entrada de CHANGELOG.
