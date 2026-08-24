# Full-system agent robustness audit

This directory contains deterministic, synthetic tests used by the full-system
agent robustness audit. It is intentionally outside `backend/app/tests` so
known failing audit cases do not silently become part of the normal backend
regression gate before the product team accepts and fixes them.

The tests do not call production services or mutate production data. They use
in-memory SQLite, dependency-injected model doubles, temporary files, and the
packaged local interview-knowledge catalog.

Run from the repository root:

```powershell
$env:PYTHONPATH = "backend"
& .\backend\.venv\Scripts\python.exe -m pytest `
  evaluation\agent_robustness\test_full_system_agent_robustness.py `
  -q --tb=short
```

The assertions describe the desired robust behavior. A pytest failure is an
executed FAIL with reproduction evidence; it is not recorded as PASS merely
because the current behavior was observed successfully.

