# Prompt 9 (English) — `GRADING_FEEDBACK_ASSISTANT_PROMPT`

| | |
|---|---|
| **Source** | [`src/prompts/en.py`](../../src/prompts/en.py) |
| **Used by** | [`src/runtime/llm_engine.py::generate_feedback`](../../src/runtime/llm_engine.py) |
| **Model** | gpt-4o, temperature 0, seed 42 |
| **Korean original** | [`../09_grading_feedback.md`](../09_grading_feedback.md) |

Same three-section, ≤350-word OSCE-evaluation report as the Korean
version: history-taking performance, patient–doctor relationship,
overall assessment. The same constraints apply (no quoting checklist
verbatim, no naming the actual diagnosis, short-conversation guard
prepended when the transcript is under 10 sentences).

The verbatim English body is in `src/prompts/en.py` under the name
`GRADING_FEEDBACK_ASSISTANT_PROMPT`.
