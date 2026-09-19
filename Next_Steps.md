# Next steps

## Where I am
- Vikunja 2.5.0 in Docker, version pinned
- 2 tests (login, create task), both passing
- Page Object Model: LoginPage, HomePage
- Locators live in page objects; tests only assert
- Unique task title per run, so leftover data can't affect the check

## Known gaps
- Tests depend on a user that only exists in my local database
- Login steps repeated in both tests
- No cleanup: tasks accumulate every run
- Credentials and URL hardcoded
- Login rate limit (10/min, shared with registration) will block a growing suite

## Plan, in order

### 1. Make tests self-sufficient
- Fixture creates its own test user (registration API)
- Fixture logs in once and reuses the browser session
- Cleanup: delete tasks the test created

### 2. Remove local assumptions
- Base URL from config (pytest-base-url)
- requirements.txt with pinned versions
- Credentials not in code

### 3. Build out the suite
- Failed login (wrong password)
- Registration
- Task CRUD: edit, complete, delete
- Data-driven cases (e.g. several invalid inputs, one test)
- Duplicate task titles: Vikunja accepts them (found during exploration)

### 4. CI with GitHub Actions
- On every push: start Vikunja in Docker, run pytest
- Publish HTML report, keep Playwright traces for failed tests
- Expected first problem: folder permissions on the Linux runner

### 5. README
- Decisions and trade-offs: why POM, locator strategy, test independence
- What changes at 500 tests instead of 20

## Time estimate

Estimate based on my pace in Phases 1–3 (about one week, including learning Playwright).
Not measured; it will be updated as I go.

| Step | Estimate | Reason |

| 1. Fixtures, own user, session reuse, cleanup | 6–10 h | Fixtures are new to me; hardest concept |
| 2. Config, requirements, credentials | 2–3 h | Small, mostly mechanical |
| 3. Build out the suite | 10–15 h | Five areas, but the pattern already exists |
| 4. CI | 6–10 h | Biggest uncertainty: Linux permission issues |
| 5. README | 3–4 h | Most decisions already documented |
| **Total** | **~27–42 h** | |

Calendar time: about 2–3 weeks alongside work (~15 h/week).

Biggest risk: CI. The Docker setup was fixed on macOS; a Linux runner
handles folder permissions differently.