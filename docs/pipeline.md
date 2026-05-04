# Data-generation pipeline

Four stages turn per-symptom reference text into voice-ready
standardised-patient scripts. Stages 1, 3, 4 call gpt-4.1 with
temperature 0.2 and seed 42; stage 2 is a deterministic file merge.

## Stage 1 — synthesise patient cohorts

```
data/seed/<symptom>.txt  ──►  GENERATE_DISEASE_LIST  ──►  data/seed/results/<symptom>_diseases.json
                                  (gpt-4.1, t=0.2, seed=42)
```

For each `.txt` file under `data/seed/`, the script asks the model to
produce five fictional patients who could plausibly present with that
chief complaint. Each patient gets a disease, name, age, gender, and vital
signs. The reference chapter is injected as `{book_content}` so the
diseases stay grounded in the local content. See
[`../prompts/01_generate_disease_list.md`](../prompts/01_generate_disease_list.md).

A consolidated dict-shaped file `data/seed/results/all_diseases.json` is
also written for debugging.

## Stage 2 — merge per-symptom JSONs

```
data/seed/results/*_diseases.json  ──►  merge  ──►  data/seed/all_diseases.json
```

No LLM call. Reads every per-symptom file from stage 1 and emits the
canonical list-shaped union expected by the rest of the pipeline:

```json
{ "diseases": [ { "symptom": "...", "patients": [...] }, ... ] }
```

## Stage 3 — generate OSCE checklists

```
data/seed/all_diseases.json  ──►  CHECKLIST_PROMPT_TEMPLATE_DATAGEN  ──►  data/seed/all_disease_with_checklists.json
                                       (gpt-4.1, t=0.2, seed=42)
```

For each patient, the prompt requests at least 20 OSCE-style interview
items, each paired with a `purpose` line that captures the rubric
rationale. Items are emitted with the `interview_item` / `purpose`
schema. See [`../prompts/02_generate_checklist.md`](../prompts/02_generate_checklist.md).

`--test` mode processes only the first two patients per symptom. Use it
when iterating on prompt edits.

## Stage 4 — scenario draft + polish

```
data/seed/all_disease_with_checklists.json
        │
        ▼
SCENARIO_PROMPT_TEMPLATE_1  (draft, 2,000–2,500 chars, 반말, no markdown)
        │
        ▼
SCENARIO_PROMPT_TEMPLATE_2  (polish — voice-ready, numerals spelled out)
        │
        ▼
data/seed/all_disease_with_scenarios.json
```

The polished string is attached to each patient as the `prompt` field —
this is the artifact that drives the LLM-based simulated patient at
runtime (see [`runtime.md`](runtime.md)).

Patients are processed in async batches: each batch first runs all drafts
in parallel and then all polishes in parallel. `--batch-size` (default 5)
trades concurrency against rate-limit pressure. See
[`../prompts/03_generate_scenario_draft.md`](../prompts/03_generate_scenario_draft.md)
and [`../prompts/04_generate_scenario_polish.md`](../prompts/04_generate_scenario_polish.md).

## Cost and runtime

A single `--batch-size 5` run over ~80 symptoms × 5 patients takes
roughly 3–4 hours. Token usage is dominated by stages 3 and 4
(checklists and scenarios are long-form Korean output).
