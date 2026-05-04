# Prompt 7 — `GRADING_CHECKLIST_ASSISTANT_PROMPT`

| | |
|---|---|
| **Source** | [`src/prompts/ko.py`](../src/prompts/ko.py) |
| **Used by** | [`src/runtime/llm_engine.py::evaluate_checklist`](../src/runtime/llm_engine.py) |
| **Model** | gpt-4o, temperature 0, seed 42 |
| **Output format** | JSON inside a ```` ```json ```` fence |

## Purpose

Per-checklist-item binary grader. Given the full student–patient
conversation and the runtime checklist (output of prompt 5), the model
attaches an `asked` field to every item: `1` if the student asked the
question (or a paraphrase thereof) anywhere in the conversation, `0`
otherwise. The grader is instructed to remain JSON-valid even when the
conversation is implausibly short or ill-formed, so downstream
post-processing can rely on the schema.

## Inputs

| Variable | Type | Source |
|---|---|---|
| `{conversation}`     | string | rendered transcript (see `grading.format_conversation`) |
| `{checklist_json}`   | string | the runtime checklist as JSON (see `grading.checklist_to_json`) |
| `{disease}`          | string | working diagnosis (used for grounding) |
| `{patient_name}`     | string | for explicit reference inside the prompt |

## Output schema

```json
{
  "diseases": [
    {
      "symptom": "<chief complaint>",
      "patients": [
        {
          "question": "...",
          "purpose":  "...",
          "order":    1,
          "asked":    1
        },
        ...
      ]
    }
  ]
}
```

The presence of every original item is preserved; only the `asked` flag
is added.

## Notes

- The grader is told *"Even if the conversation is very short or unusual,
  you must still respond in valid JSON."* This is critical: students who
  give up early would otherwise yield ambiguous outputs.
- The downstream metric is the proportion of items with `asked == 1`,
  multiplied by 100. See `grading.grade_session`.

The verbatim prompt body lives in `src/prompts/ko.py` under the name
`GRADING_CHECKLIST_ASSISTANT_PROMPT`.
