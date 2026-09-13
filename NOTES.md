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