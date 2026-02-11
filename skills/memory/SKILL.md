# SKILL.md

Use this to access Long-Term Semantic Memory (Vector Search).
This skill allows the agent to recall past projects, solutions, and mistakes.

## Philosophy
**NEVER START FROM SCRATCH.**
Always check memory first. Always update memory last.

## Decision Tree

### 1. START: Before Any Task
**Search Memory:** `python projects/nanobot-config/skills/memory/scripts/memory_engine.py search "{query}" -n 5`
- Is this a known problem? (e.g., "React hydration error")
  - Yes: **Read Solution** -> Apply fix -> Skip research.
  - No: Continue as usual.
- Is this a new project?
  - Yes: Search for "setup template" or "boilerplate".
  - No: Search for "current project status".

### 2. END: After Completion
**Store Lesson:** `python projects/nanobot-config/skills/memory/scripts/memory_engine.py add "{text}" --metadata '{json}'`
- Did you solve a tough bug?
  - Yes: Store the **Solution** + **Error Message**.
  - Metadata: `{"topic": "debugging", "tech": "react", "error": "hydration"}`
- Did you learn a new library?
  - Yes: Store the **Usage Example**.
  - Metadata: `{"topic": "tutorial", "tech": "library_name"}`
- Did you make a significant design choice?
  - Yes: Store the **Reasoning**.
  - Metadata: `{"project": "name", "type": "decision"}`

## Example Prompts
- **Context Injection:** "Before writing the CSS, search memory for 'brutalist design patterns'."
- **Learning:** "Store this lesson: 'Avoid `float:left`, use Flexbox/Grid. It breaks layout.' Metadata: `{'topic': 'css', 'bad_practice': 'float'}`."
