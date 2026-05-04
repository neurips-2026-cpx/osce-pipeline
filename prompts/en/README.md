# Prompts (English variants)

Mirror of the Korean prompts in [`../`](..), translated for users adapting
the pipeline to English-language clinical-skills training. The Korean
prompts are the canonical experimental ones; these English versions are an
alternative.

## Index

### Data generation (stages 1–4)

| # | File | Source variable |
|---|---|---|
| 1 | [`01_generate_disease_list.md`](01_generate_disease_list.md)        | `GENERATE_DISEASE_LIST` |
| 2 | [`02_generate_checklist.md`](02_generate_checklist.md)              | `CHECKLIST_PROMPT_TEMPLATE_DATAGEN` |
| 3 | [`03_generate_scenario_draft.md`](03_generate_scenario_draft.md)    | `SCENARIO_PROMPT_TEMPLATE_1` |
| 4 | [`04_generate_scenario_polish.md`](04_generate_scenario_polish.md)  | `SCENARIO_PROMPT_TEMPLATE_2` |

### Runtime + grading

| # | File | Source variable |
|---|---|---|
| 5 | [`05_runtime_checklist.md`](05_runtime_checklist.md)         | `CHECKLIST_PROMPT_TEMPLATE` |
| 6 | [`06_chatbot_system.md`](06_chatbot_system.md)               | `CHATBOT_SYSTEM_PROMPT` |
| 7 | [`07_grading_checklist.md`](07_grading_checklist.md)         | `GRADING_CHECKLIST_ASSISTANT_PROMPT` |
| 8 | [`08_grading_relationship.md`](08_grading_relationship.md)   | `GRADING_SCORE_ASSISTANT_PROMPT` |
| 9 | [`09_grading_feedback.md`](09_grading_feedback.md)           | `GRADING_FEEDBACK_ASSISTANT_PROMPT` |

All template variable names match the Korean version, so the engine code
needs no changes. To switch:

```python
from src.prompts import get_prompts
P = get_prompts("en")        # was "ko"
template = P.CHATBOT_SYSTEM_PROMPT
```

The verbatim English prompt bodies live in
[`src/prompts/en.py`](../../src/prompts/en.py).
