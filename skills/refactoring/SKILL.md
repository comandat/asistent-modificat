# SKILL.md

Use this to ensure clean, modular, and maintainable code.

## Protocol
Every 3 tasks completed:
1. **Analyze Code**:
   - `python projects/nanobot-config/skills/refactoring/scripts/analyze_code.py workspace/projects/{name}/`
   
2. **Read Report**:
   - If `audit_report.md` exists -> READ IT (`read_file`).
   
3. **Refactor**:
   - **Critical Issues Found?** -> **STOP NEW WORK.**
   - Fix issues immediately:
     - Split large files (>200 lines) into modules.
     - Extract logic from long functions (>30 lines).
     - Remove duplicate code.
     - Use meaningful names.
   - Re-run analysis until `audit_report.md` is gone.

4. **Verify**:
   - Run existing tests (Vitest/Playwright) to ensure refactoring didn't break anything.

## Principles
- **KISS**: Keep It Simple, Stupid.
- **DRY**: Don't Repeat Yourself.
- **Single Responsibility**: One function/class does ONE thing.
