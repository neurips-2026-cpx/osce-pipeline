# Prompt 9 — `GRADING_FEEDBACK_ASSISTANT_PROMPT`

| | |
|---|---|
| **Source** | [`src/prompts/ko.py`](../src/prompts/ko.py) |
| **Used by** | [`src/runtime/llm_engine.py::generate_feedback`](../src/runtime/llm_engine.py) |
| **Model** | gpt-4o, temperature 0, seed 42 |
| **Output format** | free-form Korean text, OSCE-evaluation format |

## Purpose

Write a 350-word, three-section, student-facing feedback report grounded
in the conversation transcript. The three sections are:

1. **History-taking performance** — Did the student cover the rubric? If
   not, name 1–2 categories indirectly (e.g. "social history was not
   adequately taken") without quoting the exact checklist items.
2. **Patient–doctor relationship** — Focus on the lowest-scoring of the
   five Likert dimensions, with one or two transcript-grounded examples.
3. **Overall assessment** — Total question count (around 30–40
   sentences is appropriate; >50 is excessive), positives, negatives.
   Working-diagnosis errors are surfaced obliquely, never naming the
   actual diagnosis.

If the transcript is shorter than 10 sentences, the model is instructed
to prepend "The exam could not be properly evaluated due to too few
questions" so a short or aborted session is flagged in the feedback.

## Inputs

| Variable | Type | Source |
|---|---|---|
| `{conversation}` | string | rendered transcript |
| `{disease}`      | string | working diagnosis |
| `{symptom}`      | string | chief complaint |

The disease and symptom feed the prompt's *learning-outcome* block —
five outcomes that the OSCE station is designed to assess — so the
feedback can name shortfalls in the appropriate vocabulary.

## Output

Free-form Korean text, ≤ 350 words, structured by `### History-taking
performance`, `### Patient-doctor relationship`, and `### Overall
assessment` headings. The report is delivered to the student verbatim.

## Notes

- The prompt explicitly bans generic closing lines such as "If you
  continue to develop your explanatory skills…" — this avoids template
  text and forces case-specific feedback.
- The actual diagnosis is *never* named in the feedback; this is part of
  the OSCE pedagogy (the student must reason there themselves).

The verbatim prompt body lives in `src/prompts/ko.py` under the name
`GRADING_FEEDBACK_ASSISTANT_PROMPT`.
