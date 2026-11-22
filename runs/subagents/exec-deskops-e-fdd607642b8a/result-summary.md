PASA (executor)

- deskops/dispatch.py: `_unintegrated_executor_branch`; `start` rol tester sale EXIT_BUSY (3) con 'en espera: la rama deskops/<ejecutor> de la tarea no está integrada' si una rama de ejecutor (intentos 1 y 2) tiene commits fuera de la rama base.
- tests/test_dispatch.py: 2 tests nuevos (espera y luego lanza tras reap; sin commits nuevos lanza).
- CHANGELOG.md: entrada en Fixed.
- Validación: tests/test_dispatch.py 40 passed. Commit en rama deskops/deskops-e-fdd607642b8a con Task-Id.
