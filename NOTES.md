# Phase 1 — Notes

## 1. Why Vikunja as the SUT : 
It runs locally and in CI, web UI,
It has an API, Docker and real business flows
Not Juice Shop: it's deliberately vulnerable, so its interesting behaviour is security flaws rather than the ordinary CRUD a client would want regression-tested.
## 2. Why version 2.5.0
2.5.0 shipped almost four weeks before starting this project, so it's had time for problems to surface.
## 3. Why bind mounts instead of named volumes
Named volumes gave Vikunja a folder owned by root, which it couldn't write to, so it wouldn't start. Switched to bind mounts (./data/...) - folders in the repo, owned by whoever runs docker compose up — so setup stays a single command with no manual permission step.

## 4. State persistence: local vs CI
State persists locally, so I don't lose my account between restarts while developing. CI will start from an empty instance every run, so the suite has to pass against both a used and a clean instance. That shapes how tests set up their own data.

## 5. Observations from manual exploration
- status=403 : Forbidden for giving a wrong password. Should be 401 Unauthorized, since this is a failed authentication rather than an authenticated-but-not-permitted request. 

- level=ERROR. Vikunja logs failed logins at error level.

- empty login → blocked client-side, no request
  wrong password → 403, server-side, ~130ms
  unknown → whether the server itself rejects empty credentials (untestable via UI)

- File upload works. Files are stored in data/files named by attachment ID, not original filename — the real name lives in the database.
- Vankuja allows to add duplicate tasks titles

## 6. Open questions

Does file upload work? yes
Does the server reject an empty login, or only the browser?
BDD/Gherkin — now, or as a later extension?

## 7. Where I used AI
Set up the Environment 
reading the logs
explain the error codes

## 8. Observations with Playwright
Failing test still creates data — everything before the failing assertion executes. Cleanup must happen regardless of pass/fail, which is what fixture teardown is for. 

- Login rate limit (Vikunja 2.5.0): logins were rejected with
  "Too Many Requests" after repeated test runs.
- Measured: 12 wrong-password POSTs to /api/v1/login within a minute
    -> requests 1-10 returned 403, requests 11-12 returned 429.
- Source (v2.5.0, pkg/routes/rate_limit.go and routes.go): 10 requests
    per 60 s per IP (`ratelimit.noauthlimit`), cannot be disabled.
    Login, register, password reset and token refresh share this budget.
- Not yet measured: whether the web login also triggers a token
    refresh, which would explain hitting the limit after 6 logins.
- Impact on tests: every UI login and registration uses this budget.
- JWT appears to live ~10 minutes (measured from exp).
- SQLite write lock: PUT /api/v1/projects/{id}/tasks returned 500 twice
    during full-suite runs (24 Sep).
- Vikunja log: level=ERROR ... status=500 err="database is locked",
    timestamps 10.091 (API setup) and 10.092 (browser write).
- Cause: setup goes through the API while the browser is still writing
    from the previous test. SQLite allows one writer at a time.
- Environmental, not an application defect. Proper fix would be
    PostgreSQL in the test environment instead of the default SQLite.
- Not observed when running a single test file, only full runs.
- Deliberately not retried in code: a retry would hide the constraint.