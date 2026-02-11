# SKILL.md

Use this to coordinate complex projects with strict quality control.
This skill transforms Nanobot from a solo worker into a disciplined software team.

## Roles & Responsibilities

### 👑 @ProductOwner
- **Focus:** User Needs & Requirements.
- **Output:** `REQUIREMENTS.md` (What are we building? Why? Who for?).
- **Action:** Defines the scope.

### 🏛️ @Architect
- **Focus:** System Design & Structure.
- **Input:** `REQUIREMENTS.md`.
- **Output:** `ARCHITECTURE.md` (Diagrams, Stack choices, File structure).
- **Action:** Breaks down the project into tickets.

### 👷 @Developer
- **Focus:** Implementation.
- **Input:** Ticket description + `ARCHITECTURE.md`.
- **Output:** Working code in `src/`.
- **Action:** Writes code. DOES NOT MARK AS DONE. Submits for review.

### 🧪 @Tester
- **Focus:** Verification.
- **Input:** Working code.
- **Output:** `tests/` + Test Reports.
- **Action:** Ensures code works as intended.

### 🔍 @Reviewer
- **Focus:** Quality Assurance & Code Style.
- **Input:** Submitted code + Test results.
- **Output:** Approval or Rejection with comments.
- **Action:** The Gatekeeper. Only the Reviewer can mark a task as DONE.

## The Workflow Algorithm

1. **Initialization**:
   - `create product_owner "Define Scope"`
   - `start 1` -> Write `REQUIREMENTS.md` -> `submit 1` -> `review 1 approve`.

2. **Planning**:
   - `create architect "System Design" --deps 1`
   - `start 2` -> Write `ARCHITECTURE.md` -> Break down work into tickets (Dev, Test, Review) -> `submit 2`.

3. **Development Loop (The Engine)**:
   - Developer picks a ticket: `start {id}`.
   - Developer works.
   - Developer finishes: `submit {id} --notes "Implemented login logic."`
   - **Status changes to: NEEDS_REVIEW**.

4. **Review Loop (The Quality Gate)**:
   - Reviewer picks a NEEDS_REVIEW ticket.
   - **Audit**: Check code style, run tests, read logic.
   - **Decision**:
     - ✅ **Pass**: `review {id} approve --notes "LGTM!"` -> Status: **DONE**.
     - ❌ **Fail**: `review {id} reject --notes "Fix the bug in line 40."` -> Status: **REJECTED**.
   - **If Rejected**: Developer must `start {id}` again, fix issues, and re-submit.

## Critical Rules
- A Developer NEVER approves their own PR/Ticket.
- A Ticket is not DONE until it passes tests AND review.
- If the Architect changes the plan, all dependent tickets must be updated.
