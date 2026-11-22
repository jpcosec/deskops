# Result (intento 2)
- Cambio: `closed_task_ids` (deskops/doctor_findings.py) también cuenta como cerrada una tarea con un commit de asunto `closeout: <task-id>` (con sufijo opcional ` [skip ci]`, id completo, sin prefijos), vía `%s` en el mismo `git log`.
- Test nuevo: tests/test_doctor_lost_receipts.py::test_closeout_known_only_by_its_subject_does_not_alert (cierre solo en asunto; un id más largo con el mismo prefijo sigue alertando).
- IR (solo lectura) `deskops doctor --root IR | grep -ci lost`: antes 83, después 0 (con el código del worktree vía PYTHONPATH).
- Validación: tests/test_doctor_*.py -> 35 passed (validation.log).
- Archivos: deskops/doctor_findings.py, tests/test_doctor_lost_receipts.py
- run_id/session/session_sha256: no disponibles (ejecutor Scion, sin sesión hija).
