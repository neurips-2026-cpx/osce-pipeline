# Prompt 5 — `CHECKLIST_PROMPT_TEMPLATE` (runtime)

| | |
|---|---|
| **Source** | [`src/prompts/ko.py`](../src/prompts/ko.py) |
| **Used by** | [`src/runtime/llm_engine.py::generate_checklist`](../src/runtime/llm_engine.py) |
| **Model** | gpt-4o, temperature 0, seed 42 |
| **Output format** | JSON inside a ```` ```json ```` fence |

## Purpose

Runtime variant of the OSCE checklist generator. Used by the auto-grader
flow to produce a per-session checklist for a single patient at evaluation
time. The schema differs from the data-generation variant
(`CHECKLIST_PROMPT_TEMPLATE_DATAGEN`): each item carries a numeric `order`
field and the question key is `"question"` rather than `"interview_item"`,
matching what `GRADING_CHECKLIST_ASSISTANT_PROMPT` consumes.

## Inputs

| Variable | Type | Source |
|---|---|---|
| `{symptom}`        | string | chief complaint |
| `{patient_name}`   | string | patient name |
| `{patient_age}`    | int    | patient age |
| `{sex}`            | string | gender |
| `{vital_sign}`     | string | vitals block |
| `{disease}`        | string | working diagnosis |
| `{book_content}`   | string | optional reference chapter (may be empty at runtime) |

## Output schema

```json
{
  "diseases": [
    {
      "symptom": "<chief complaint>",
      "patients": [
        {
          "question": "<a single interview item>",
          "purpose":  "<rubric rationale>",
          "order":    <int 1..n>
        },
        ...  // ≥ 20 items
      ]
    }
  ]
}
```

## Notes

- The hematuria few-shot is the same anchor used in the data-gen variant.
- The runtime expects `order` to be present so that
  `GRADING_CHECKLIST_ASSISTANT_PROMPT` can attach an `asked` 0/1 flag per
  ordered item.

The verbatim Korean prompt body lives in `src/prompts/ko.py` under the
name `CHECKLIST_PROMPT_TEMPLATE`. The English mirror is in
`src/prompts/en.py` under the same name.
