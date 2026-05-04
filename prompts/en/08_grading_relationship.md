# Prompt 8 (English) — `GRADING_SCORE_ASSISTANT_PROMPT`

| | |
|---|---|
| **Source** | [`src/prompts/en.py`](../../src/prompts/en.py) |
| **Used by** | [`src/runtime/llm_engine.py::evaluate_relationship`](../../src/runtime/llm_engine.py) |
| **Model** | gpt-4o, temperature 0, seed 42 |
| **Korean original** | [`../08_grading_relationship.md`](../08_grading_relationship.md) |

Same five 1–5 dimensions as the Korean version: efficient questioning,
active listening, empathy and understanding, clear explanation, rapport
building. Output schema and downstream metric are identical.

The verbatim English body is in `src/prompts/en.py` under the name
`GRADING_SCORE_ASSISTANT_PROMPT`.
