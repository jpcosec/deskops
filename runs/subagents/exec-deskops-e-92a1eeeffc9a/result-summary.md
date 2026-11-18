# Result summary — task-deskops-desk-update-apply-sobre-el-repo-de-deskops-no-vacía-el-path-de-los-modelos-en-sldb-core-mode

run_id: exec-deskops-e-92a1eeeffc9a
session: (not available to the executor)
session_sha256: (not available)

## Reproduction (clean clone of HEAD 0b858613)
Evidence: repro-diff-stat.txt, repro-diff.txt (before), after-fix-diff-stat.txt, after-fix-diff.txt (after).
Before: 29 files changed; RoleDoc.yaml etc. `path: deskops/models/role.py` -> `path: ''`; store.yaml entries lose `path` and gain `origin: deskops`; has_model.md rewritten; reltype-links_to added.

## Cause
- Paths: deskops/bootstrap.py `_register_models` (the loop that calls `_inherit_model`) inherits any entry that has no origin and matches MODEL_REFS from the owner store linked as `deskops`. `desk.py` (copied_models detection, ~l.320) flags them as "Copied deskops models" and triggers it. Inherited entries keep no path (sldb ModelEntry.origin) -> path ''. Only skipped when root == owner store; any other checkout with local models (the integrador's tools at 31460a48) was converted.
- Relation types: the same `_register_models` always calls `init_relations` (sldb/src/sldb/api/edges/init_relations.py). The has_model change (cardinality many_to_many) and reltype-links_to come from sldb's builtin declarations (sldb/src/sldb/models/builtin_relation_types.py). deskops declares none of them (no relation type in deskops/models or deskops/data); so they are not deskops'.

## Fix
- bootstrap.py: new `SLDBBootstrap.is_local_model_entry` (non-empty path resolving to a file inside the store's repo); `_register_models` skips inheriting such entries; `init_relations` runs only when RelationTypeDoc/RelationDoc are not registered.
- desk.py: copied_models ignores local-path entries.
- Test: tests/test_desk_sync.py::test_desk_update_apply_keeps_the_local_path_of_a_declared_model (fails before: '' != 'deskops/models/role.py'; passes after).
- CHANGELOG.md entry.

## After fix (clean clone, same command)
.sldb/core/models: only RelationDoc/RelationTypeDoc hash/documents_count change (legit: new lifecycle relation docs from desk/lifecycle); no model path touched; sldb/relation_types untouched; no links_to.
Remaining diffs (lifecycle graph docs, tag_namespaces in store.yaml) are normal desk update output unrelated to this bug.

## Files changed
deskops/bootstrap.py, deskops/cli/commands/desk.py, tests/test_desk_sync.py, CHANGELOG.md

## For the supervisor
- NOT committed: the system instructions for this role forbid handcrafted commits (closeout commit does it), which conflicts with prompt.md's "Entrega" section. The working tree also holds unrelated dirty files from others; do not stage them.
- Only tests/test_desk_sync.py run (9 passed); full suite is integrate's.
