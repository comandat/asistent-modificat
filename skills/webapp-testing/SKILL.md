# SKILL.md

Use this when testing web applications.

## Decision Tree
Is static HTML?
- Yes -> Read HTML -> Use Selectors -> Success? (Y: Done, N: Treat as dynamic)
- No -> Server Running?
    - No -> Run `python projects/nanobot-config/skills/webapp-testing/scripts/with_server.py --help` -> Use helper + simplified script
    - Yes -> Reconnaissance-then-action (Navigate -> Wait networkidle -> Inspect -> Act)

## Execution
Write a black-box python script using `sync_playwright`.
Do not inspect DOM before `networkidle`.
ALWAYS close browser.
