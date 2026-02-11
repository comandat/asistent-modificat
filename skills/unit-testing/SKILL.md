# SKILL.md

Use this when ensuring logical correctness and stability.
Adhere strictly to Test-Driven Development (TDD).

## Core Philosophy: TDD
1. **Red:** Write a test that fails (because the feature doesn't exist yet).
2. **Green:** Write the minimum code required to pass the test.
3. **Refactor:** Clean up the code while keeping tests green.

## Protocol

### 1. Initialization
- **Environment Check:** Does `package.json` exist?
  - Yes: `npm install -D vitest @vitest/coverage-v8`.
  - No: Create it (`npm init -y`) and install.

### 2. The Testing Cycle
1. **Identify Logic:** Find pure functions or components to test.
2. **Write Test First:** Create `src/tests/{name}.test.ts`.
   - Import `describe, it, expect` from `vitest`.
   - Write at least one failing test case.
3. **Run Test:** `npx vitest run`.
   - **MUST FAIL.** If it passes, rewrite the test (it's testing nothing).
4. **Implement Code:** Write the actual logic in `src/{name}.ts`.
5. **Run Test:** `npx vitest run`.
   - **MUST PASS.** If fails, fix the code.
6. **Iterate:** Add edge cases (null, empty strings, large numbers).

### 3. Mocking Dependencies
- Use `vi.mock()` for external calls (API, Database).
- Example:
  ```ts
  import { vi } from 'vitest';
  vi.mock('./api', () => ({ fetchData: vi.fn(() => ({ data: 'mocked' })) }));
  ```

### 4. Coverage Standard
- Aim for **80% coverage** on critical paths.
- Run: `npx vitest run --coverage`.
- If coverage is low, add tests for untested branches.

## Troubleshooting
- **Test Timeout?** Check async/await or infinite loops.
- **Import Error?** Check file paths and extensions (`.ts` vs `.js`).
- **Mock not working?** Ensure `vi.mock` is at the top level.
