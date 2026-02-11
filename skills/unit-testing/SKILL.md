# SKILL.md

Use this when writing UNIT tests for JavaScript/TypeScript projects (Node.js, React, Vue, Svelte).

## Decision Tree
Is `package.json` present?
- No -> Use `python projects/nanobot-config/skills/webapp-testing/SKILL.md` (Playwright E2E) or plain Node.js assertions.
- Yes -> Check `devDependencies`:
    - Has `vitest`? -> Run `npx vitest run`
    - Has `jest`? -> Run `npx jest`
    - None? -> Install Vitest: `npm install -D vitest` -> Create `vitest.config.ts` (optional) -> Run `npx vitest run`

## Execution Protocol
1. **Identify Logic**: Find pure functions or components to test.
2. **Write Test**: Create `src/tests/name.test.ts` using `import { describe, it, expect } from 'vitest'`.
3. **Run**: `npx vitest run` (Single run, not watch mode).
4. **Iterate**: If fail -> Fix code -> Re-run.

## Best Practices
- Use `describe` blocks to group tests.
- Mock external dependencies (API calls, DB) using `vi.mock()`.
- Keep tests fast and isolated.
