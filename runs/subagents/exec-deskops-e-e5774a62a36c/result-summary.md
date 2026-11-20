# Result
build_neighbours (deskops/absolute_paths.py) now resolves each registry entry with resolve_registered_root (expands ~, relative against root), same as doc_access.repository_root. Roots registered as neighbours when the entry is not absolute after expanduser.
New test in tests/test_doctor_absolute_paths.py (tilde with HOME in sandbox + relative): same dir via both paths.
Validation: 22 passed (see validation.log).
Files: deskops/absolute_paths.py, tests/test_doctor_absolute_paths.py (committed with Task-Id).
