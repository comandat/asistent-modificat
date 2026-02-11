# SKILL.md

Use this when you need to understand a new technology, debug a complex error, or find documentation.

## Decision Tree
Is the information readily available in your training data?
- Yes -> Provide answer.
- No -> Is it about a specific error?
    - Yes -> Run: `python projects/nanobot-config/skills/research/scripts/deep_research.py "error message + context" --depth 3`
    - No (General Topic) -> Run: `python projects/nanobot-config/skills/research/scripts/deep_research.py "TOPIC detailed guide" --depth 5`

## Execution Protocol
1. **Define Query**: Be specific. Include language/framework version.
2. **Execute Research**: Run script. Wait for `research_TOPIC.md`.
3. **Read Report**: Use `read_file` to ingest the generated markdown report.
4. **Synthesize**:
   - Extract key steps/code snippets.
   - Summarize for user.
   - Cite sources (URL).
