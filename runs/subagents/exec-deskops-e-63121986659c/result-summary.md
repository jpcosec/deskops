# Result
Hecho. dispatch start quita el tracking (untrack_doc) de un RunDoc huérfano de la identidad antes de record_scion_run; si record falla, borra el run_dir vacío. Un RunDoc con run_dir presente sigue contando como intento.
Archivos (commiteados en la rama deskops/deskops-e-63121986659c): deskops/dispatch.py, tests/test_dispatch.py (test_start_untracks_a_stale_rundoc_whose_run_dir_is_missing), CHANGELOG.md.
Validación: tests/test_dispatch.py 38 passed (validation.log).
