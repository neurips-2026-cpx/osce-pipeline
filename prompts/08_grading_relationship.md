# Prompt 8 — `GRADING_SCORE_ASSISTANT_PROMPT`

| | |
|---|---|
| **Source** | [`src/prompts/ko.py`](../src/prompts/ko.py) |
| **Used by** | [`src/runtime/llm_engine.py::evaluate_relationship`](../src/runtime/llm_engine.py) |
| **Model** | gpt-4o, temperature 0, seed 42 |
| **Output format** | JSON inside a ```` ```json ```` fence |

## Purpose

Score the student–patient interaction along five clinical-communication
dimensions, each on a 1–5 Likert scale, with a brief reason citing
specific evidence from the transcript.

The five dimensions:

1. **`1_efficient_questioning`** — Use of open-ended questions, mid-conversation summaries, and confirmation of answers.
2. **`2_active_listening`** — Verbal acknowledgments, attentive tone.
3. **`3_empathy_and_understanding`** — Empathic statements; questions about the patient's situation.
4. **`4_clear_explanation`** — Clear explanations, opportunities for questions, simple word choice.
5. **`5_rapport_building`** — Greeting, self-introduction, polite register, respectful tone.

## Inputs

| Variable | Type | Source |
|---|---|---|
| `{conversation}`  | string | rendered transcript |
| `{patient_name}`  | string | patient's name |

## Output schema

```json
{
  "patient_doctor_relationship_evaluation": {
    "1_efficient_questioning": {
      "reason": "...",
      "score":  <int 1..5>
    },
    "2_active_listening":          { "reason": "...", "score": ... },
    "3_empathy_and_understanding": { "reason": "...", "score": ... },
    "4_clear_explanation":         { "reason": "...", "score": ... },
    "5_rapport_building":          { "reason": "...", "score": ... }
  }
}
```

## Notes

- The few-shot example in the prompt body shows a low-then-high scoring
  pattern across the five dimensions, which calibrates the model on what
  *evidence-backed* reasons should look like at different score levels.
- The downstream metric is the mean of the five scores, contributing
  equally with the checklist score in the final aggregate (see
  `grading.grade_session`).

The verbatim prompt body lives in `src/prompts/ko.py` under the name
`GRADING_SCORE_ASSISTANT_PROMPT`.
