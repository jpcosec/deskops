# Result
Files: deskops/sldb_layout.py (new), deskops/cli/commands/doctor.py, deskops/cli/commands/core.py (init), README.md, .claude/skills/deskops-workflow/SKILL.md, tests/test_doctor_sldb_layout.py (new).
- doctor: the three signals (.sldb/runtime/, .sldb/journal, .gitignore line ignoring .sldb/core|runtime) give an error with `sldb stores migrate-layout --store <repo>/.sldb`; no "Desk is healthy" while any remains.
- init: exits 1 with the same remedy before touching anything.
- Docs: README + skill procedure.
Validation: see validation.log. Full suite ran with -n 4 (51 min). Reviewer: test_help_goldens fails on the drawer help golden, outside this task; the clean-main re-run did not finish, please confirm it fails there too.
