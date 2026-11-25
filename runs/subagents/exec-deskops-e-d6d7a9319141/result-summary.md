# Result summary
- Added autouse fixture `_clear_global_caches` in tests/conftest.py: after each test calls invalidate_runtime_cache, invalidate_index_cache, built_cache.clear, alert_sink.forget, and clears doc_access._DOC_PAYLOADS/_READ_HASHES/_INDEX_ENTRIES.
- Committed in worktree .worktrees/deskops-e-d6d7a9319141 (Task-Id trailer).
- Validation: pytest tests/test_transaction.py tests/test_operational.py -n 4 (TMPDIR=/tmp, basetemp /tmp/pytest-$HOSTNAME): 19 passed.
- Not done: full-suite single-process MemoryMax=2G measurement was not re-run here (session hit the 2h limit); supervisor/tester should verify it.
