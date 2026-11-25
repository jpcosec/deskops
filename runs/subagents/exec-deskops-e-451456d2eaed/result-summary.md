# Result
Files (committed in worktree branch deskops/deskops-e-451456d2eaed): deskops/models/board.py, tests/test_board_phases.py.
- Added PhaseIntegration, Phase, BoardDoc.phases (default []), template marker `phases: ⸢rev•phases⸥` after rituals, validator rejecting a task twice (across or within phases), and a before-validator mapping an absent/None phases to [] (needed so existing Boards extract).
- Validation: see validation.log (21 passed incl. test_model_templates).

Finding: deskops advance task blocked: rule-activation-task-code needs an accepted, intact bundle receipt (preflight review anchor_state=changed). Not advanced.
