run_id: exec-deskops-e-bd1040135fe6
session: n/a (claude harness)  session_sha256: n/a

Changed (committed in worktree branch deskops/deskops-e-bd1040135fe6): deskops/doctor_findings.py, tests/test_doctor_lost_receipts.py, CHANGELOG.md.
- lost section now: "the task was deleted without closeout: restore it from git or close it with `deskops closeout resolved-by`." No mention of desk update --apply. The "register ... --apply" footer was already only printed under findings.alerts (separate from lost), unchanged.
- Old-text assert replaced; new test closes a real task with closeout verify + closeout commit in lifecycle_desk and checks doctor prints no lost.
Validation: see validation.log. IR doctor: no lost alerts.
