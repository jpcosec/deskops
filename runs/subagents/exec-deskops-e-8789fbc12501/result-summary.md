run_id: exec-deskops-e-8789fbc12501
session: (retomada tras limite de 2h de scion; sin path de sesion hijo)
session_sha256: n/a

Implementado en la rama deskops/deskops-e-8789fbc12501 (commit con Task-Id): init --id, repo whoami --set (slug, reescribe solo project_identity), aviso en repo register.
Archivos: deskops/cli/commands/core.py, deskops/cli/commands/repo.py, deskops/cli/registry.py, deskops/workspace.py, goldens help init y repo_whoami, tests/test_repo_identity.py.
Validacion: 22 tests pasan (test_repo_identity, test_scaffold_golden, test_output_goldens). La suite completa -n 4 NO se corrió; revisar.
