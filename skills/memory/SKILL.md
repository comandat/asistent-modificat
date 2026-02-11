# SKILL.md

Use this to access Long-Term Semantic Memory (Vector Search).

## Setup
First time? Run: `pip install chromadb`

## Decision Tree
Is user asking a complex question or referencing past work?
- Yes -> SEARCH: `python projects/nanobot-config/skills/memory/scripts/memory_engine.py search "QUESTION" -n 5`

Did you just finish a significant task or learn something new?
- Yes -> STORE: `python projects/nanobot-config/skills/memory/scripts/memory_engine.py add "LESSON_LEARNED_TEXT" --metadata '{"project": "NAME"}'`

## Example Usage
- **Find Solution:** "How did I fix the CSS bug last time?" -> `search "CSS layout fix webshop"`
- **Remember Lesson:** "Never use float:left for layout." -> `add "Do not use float:left, prefer flex/grid. It causes bugs." --metadata '{"topic": "css"}'`
