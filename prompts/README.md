# Prompts

Nine templates document every LLM call this repository makes. Four drive
the data-generation pipeline (stages 1–4), four drive the
runtime-side evaluation (chat + grading), and one runtime-only checklist
generator that feeds the grader.

The Korean versions live in [`src/prompts/ko.py`](../src/prompts/ko.py) and
the English mirrors in [`src/prompts/en.py`](../src/prompts/en.py).
Placeholder variables are identical across languages, so swapping the
language is a single argument: `get_prompts("ko")` vs `get_prompts("en")`.

## Index

### Data generation (stages 1–4)

| # | File | Source variable | Stage | Model |
|---|---|---|---|---|
| 1 | [`01_generate_disease_list.md`](01_generate_disease_list.md)        | `GENERATE_DISEASE_LIST`            | 1 | gpt-4.1, t=0.2, seed=42 |
| 2 | [`02_generate_checklist.md`](02_generate_checklist.md)              | `CHECKLIST_PROMPT_TEMPLATE_DATAGEN`| 3 | gpt-4.1, t=0.2, seed=42 |
| 3 | [`03_generate_scenario_draft.md`](03_generate_scenario_draft.md)    | `SCENARIO_PROMPT_TEMPLATE_1`       | 4a | gpt-4.1, t=0.2, seed=42 |
| 4 | [`04_generate_scenario_polish.md`](04_generate_scenario_polish.md)  | `SCENARIO_PROMPT_TEMPLATE_2`       | 4b | gpt-4.1, t=0.2, seed=42 |

### Runtime + grading

| # | File | Source variable | Used by | Model |
|---|---|---|---|---|
| 5 | [`05_runtime_checklist.md`](05_runtime_checklist.md)         | `CHECKLIST_PROMPT_TEMPLATE`           | `LLMEngine.generate_checklist`       | gpt-4o, t=0,   seed=42 |
| 6 | [`06_chatbot_system.md`](06_chatbot_system.md)               | `CHATBOT_SYSTEM_PROMPT`               | `LLMEngine.chat_with_patient`        | gpt-4o, t=0.5, seed=42, **streaming** |
| 7 | [`07_grading_checklist.md`](07_grading_checklist.md)         | `GRADING_CHECKLIST_ASSISTANT_PROMPT`  | `LLMEngine.evaluate_checklist`       | gpt-4o, t=0,   seed=42 |
| 8 | [`08_grading_relationship.md`](08_grading_relationship.md)   | `GRADING_SCORE_ASSISTANT_PROMPT`      | `LLMEngine.evaluate_relationship`    | gpt-4o, t=0,   seed=42 |
| 9 | [`09_grading_feedback.md`](09_grading_feedback.md)           | `GRADING_FEEDBACK_ASSISTANT_PROMPT`   | `LLMEngine.generate_feedback`        | gpt-4o, t=0,   seed=42 |

### English variants

[`en/`](en/) mirrors all nine markdown documents and points at
`src/prompts/en.py`. The English templates use identical placeholder
variable names — wiring is the same, only the natural-language surface
changes.

## Why two checklist prompts?

`CHECKLIST_PROMPT_TEMPLATE_DATAGEN` (data-gen, prompt 2) and
`CHECKLIST_PROMPT_TEMPLATE` (runtime, prompt 5) target different output
schemas:

- **Prompt 2 / data-gen** emits items as `{"interview_item", "purpose"}`.
  This is what the bulk dataset under
  `data/seed/all_disease_with_checklists.json` carries.
- **Prompt 5 / runtime** emits items as `{"question", "purpose", "order"}`.
  The grader (prompt 7) attaches `"asked": 0|1` to this exact shape.

Both versions are preserved verbatim because they reflect the actual
prompts as run during the experiment.

## Conventions shared by all prompts

- **Few-shot anchoring on hematuria.** Prompts 2, 3, 5, 7 each embed a
  fully written-out hematuria example. The example is the same regardless
  of the target disease — it anchors structure (item count, granularity,
  vocabulary) without leaking content for any specific target.
- **Reference-knowledge injection.** Prompts 1, 2, 3, 5 take a
  `{book_content}` variable holding the per-symptom reference chapter.
  The variable may be empty at runtime if no chapter is supplied.
- **JSON enforcement.** Prompts 1, 2, 5, 7, 8 emit JSON in a fenced
  block. The downstream parser (`LLMEngine._parse_json`,
  `src.utils.trimAndLoadJson`) tolerates trailing commas, missing
  closing braces, and ASCII control characters.
- **Voice-ready output.** Prompt 4 (and the runtime chat in prompt 6)
  prefer everyday Korean: numerals are spelled out (`20` → `이십`,
  `5~6` → `오에서 육`), and medical jargon is replaced with lay terms
  (`편도` → `목 안쪽`).
