# Result
- integrate.py: skips `git push origin <code>:<branch>` when code is ancestor of origin/<branch> (prints "código ya en origin: <sha12>"), still pushes the tip.
- tests/test_integrate.py: new test_code_already_behind_origin_main_is_not_pushed; the desk-only-range test now uses `in` for "integrado " (extra info line).
- CHANGELOG.md: Fixed entry.
- Validation: tests/test_integrate.py 20 passed (validation.log, exit 0).
Files: deskops/integrate.py tests/test_integrate.py CHANGELOG.md
