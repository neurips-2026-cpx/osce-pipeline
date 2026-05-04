# Prompt 6 — `CHATBOT_SYSTEM_PROMPT`

| | |
|---|---|
| **Source** | [`src/prompts/ko.py`](../src/prompts/ko.py) |
| **Used by** | [`src/runtime/llm_engine.py::chat_with_patient`](../src/runtime/llm_engine.py) |
| **Model** | gpt-4o, temperature **0.5** (streaming), seed 42 |
| **Output format** | streaming Korean text |

## Purpose

System prompt that instantiates the LLM as a simulated patient at the
OSCE station. Each line yielded back to the student is prefixed with the
patient's name to make the role boundary explicit in the transcript. The
bot intentionally:

- answers concisely (≤ 25 words),
- never volunteers information that was not asked,
- never reveals the diagnosis (replies "I'm not sure" if asked directly),
- speaks in lay vocabulary instead of medical jargon,
- gives approximate, colloquial values rather than exact numerics.

These rules together make the simulated patient behave like a typical
standardised patient in a real OSCE.

## Inputs

| Variable | Type | Source |
|---|---|---|
| `{symptom}`       | string | chief complaint |
| `{prompt}`        | string | the polished scenario produced by `SCENARIO_PROMPT_TEMPLATE_2` |
| `{patient_name}`  | string | patient name |

## Output

Conversational Korean text. Each turn begins with the literal prefix
`{patient_name} 모의 환자 :` (or its English equivalent in `en.py`) so
post-hoc transcript splitting is trivial.

## Notes

- Conversation history is held in `LLMEngine.memories[session_id]`; the
  system prompt is not re-rendered on each turn.
- Temperature 0.5 is intentional: a fully deterministic patient would
  give identical responses to identical questions, which makes the
  simulator feel scripted to students.

The verbatim prompt body lives in `src/prompts/ko.py` under the name
`CHATBOT_SYSTEM_PROMPT`.
