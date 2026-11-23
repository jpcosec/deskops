PASA

Commit del ejecutor: 5fff4cdaf4fd8a5f4513b41281fbeac1ed84ae0b ("Borrar detector legacy de related_atoms y alias scaffold_desk/ensure_lifecycle_graph")

Archivos del commit:
- deskops/atom_references.py
- deskops/graph/checks.py
- deskops/graph/desk_graph.py (consumidor adicional de LEGACY_FIELDS, también limpiado)
- deskops/lifecycle.py
- deskops/workspace.py
- tests/test_atom_reference_convention.py

Validación
- grep exacto de la tarea (`! grep -rnE 'LEGACY_FIELDS|LEGACY_FIELD_VIOLATION|scaffold_desk|ensure_lifecycle_graph' deskops tests`): vacío, exit 0. Antes fallaba solo por .pyc obsoletos en __pycache__ (no versionados); tras limpiarlos pasa. `git grep` sobre los archivos versionados también sale vacío. No queda ningún uso de related_atoms salvo el ejemplo en bloque fenced de test_fenced_yaml_examples_are_not_scanned, conservado a propósito.
- tests/test_atom_reference_convention.py: 5 passed.
- tests/test_graph_checks.py: 9 passed.
- tests/test_desk_graph_runs_target.py: 2 passed.
- tests/test_lifecycle_graph.py: 24 passed.
- tests/test_lifecycle_seed_drift.py: 8 passed.
- tests/test_cli.py: 103 passed.
- Tests de grafo afectados por REFERENCE_FIELDS: test_graph_extract_edges, test_graph_declared_edges, test_graph_store_index_not_nodes, test_graph_self_reflection, test_graph_atom_trace, test_graph_missing_existing_files, test_graph_snapshot, test_graph_cli, test_graph_extract_docs, test_graph_extract_sources: todos pasan.
- tests/test_lifecycle_end_to_end.py: 4 de 5 pasan. test_auto_commit_task_closure_commits_only_its_own_paths queda colgado (>300 s) en este entorno; reproducido igual en un checkout limpio de origin/main, por lo que no es una falla nueva del commit. Los otros cuatro tests del archivo pasan.
- No se corrió la suite completa (la integra el host), según las instrucciones del rol tester.

Observación fuera de alcance: /mnt/ssd/proyectos/SLDB_1/reports/rescate-hdd-2026-11-22/20261102-ws13-1-lector/tester/build_fixture.py importa scaffold_desk y ensure_lifecycle_graph. Es un artefacto archivado del rescate del HDD, fuera del árbol del proyecto y no versionado por deskops; no se considera consumidor vivo. Los restantes matches del grep amplio están en .worktrees de otros runs, que son checkouts separados.

Veredicto: PASA. El código legacy y los alias desaparecen, los greps de validación quedan vacíos y los tests relevantes pasan sin fallas nuevas.
