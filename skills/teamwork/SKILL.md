# SKILL.md

Use this to coordinate complex projects with multiple roles.

## Roles
- **@Architect**: Designs the system. Creates `ARCHITECTURE.md`.
- **@Developer**: Implements the code. Creates `src/`.
- **@Tester**: Writes and runs tests. Creates `tests/`.
- **@Reviewer**: Audits code quality and aesthetics.

## Workflow Protocol
1. **Define Plan**:
   - Architect creates tickets:
     - `create architect "Design System Architecture"`
     - `create developer "Implement Backend" --deps 1`
     - `create tester "Write Unit Tests" --deps 2`
     - `create reviewer "Code Audit" --deps 3`

2. **Execute**:
   - Pick next PENDING ticket.
   - Check deps: `start {id}`.
   - If blocked -> Wait for dependency.
   - If clear -> Do work.
   - Mark done: `finish {id}`.

3. **Verify**:
   - Reviewer MUST approve before project is considered complete.
