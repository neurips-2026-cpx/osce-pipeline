# Prompt 6 (English) — `CHATBOT_SYSTEM_PROMPT`

| | |
|---|---|
| **Source** | [`src/prompts/en.py`](../../src/prompts/en.py) |
| **Used by** | [`src/runtime/llm_engine.py::chat_with_patient`](../../src/runtime/llm_engine.py) |
| **Model** | gpt-4o, temperature 0.5 (streaming), seed 42 |
| **Korean original** | [`../06_chatbot_system.md`](../06_chatbot_system.md) |

The English version follows the same five behavioural rules as the
Korean version: ≤25-word answers, no volunteered prior information,
no diagnosis disclosure, lay vocabulary, approximate values. Each turn
is prefixed with `Simulated patient {patient_name}: ` so transcripts
remain easy to split.

The verbatim English body is in `src/prompts/en.py` under the name
`CHATBOT_SYSTEM_PROMPT`.
