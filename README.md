# OSCE Simulated-Patient Pipeline

A unified, end-to-end framework for synthesising and evaluating Korean OSCE
(Objective Structured Clinical Examination) cases with large language models.
The repository covers two complementary halves:

1. **Data generation** — turns per-symptom medical reference text into a
   structured corpus of fictional patients, OSCE-style interview checklists,
   and voice-ready standardised-patient scenarios.
2. **Runtime + auto-grading** — drives a streaming simulated-patient chat
   from any of those scenarios, then auto-grades the student's session
   against the checklist and a five-dimension patient–doctor-relationship
   rubric.

This release accompanies our NeurIPS submission. The seed corpus and the
full released dataset are distributed separately — see
[`data/README.md`](data/README.md).

## At a glance

```
                    DATA GENERATION                        RUNTIME + GRADING
                    ────────────────                       ─────────────────

 seed/<symptom>.txt                                     example_patient.json
        │                                                       │
        ▼                                                       ▼
   stage 1 (gpt-4.1, t=0.2, seed=42)                  ┌──────────────────────┐
   GENERATE_DISEASE_LIST                              │ chat_with_patient    │
        │                                             │ gpt-4o, t=0.5,       │
        ▼                                             │ streaming, seed=42   │
   stage 2 (no LLM)                                   └──────────┬───────────┘
   merge per-symptom JSONs                                       │  student
        │                                                        │  doctor
        ▼                                                        ▼  session
   stage 3 (gpt-4.1, t=0.2, seed=42)                  ┌──────────────────────┐
   CHECKLIST_PROMPT_TEMPLATE_DATAGEN                  │ generate_checklist   │
        │                                             │ evaluate_checklist   │
        ▼                                             │ evaluate_relationship│
   stage 4 (gpt-4.1, t=0.2, seed=42)                  │ generate_feedback    │
   SCENARIO_PROMPT_TEMPLATE_1 (draft)                 │ gpt-4o, t=0, seed=42 │
   SCENARIO_PROMPT_TEMPLATE_2 (polish)                └──────────┬───────────┘
        │                                                        ▼
        ▼                                                  GradingResult
   all_disease_with_scenarios.json                       (checklist score,
   (each patient gets a "prompt" field;                   relationship 1-5,
    consumable by chat_with_patient)                      total score, grade,
                                                          feedback)
```

All prompts are documented under [`prompts/`](prompts/) (Korean originals)
and [`prompts/en/`](prompts/en/) (English variants). Both languages share
the same placeholder variables, so flipping `lang="ko"` to `lang="en"` is
the only change needed at the API surface.

## Repository layout

```
.
├── src/
│   ├── prompts/                    Bilingual prompt module (ko.py, en.py)
│   ├── pipeline/                   Data-generation stages 1–4
│   ├── runtime/                    Simulator + interactive demo
│   ├── grading.py                  Auto-grader (per-item + relationship)
│   ├── utils.py, logging_utils.py
│   └── json_to_excel.py            Optional checklist export to .xlsx
├── prompts/                        Markdown documentation, one per prompt
│   ├── README.md                   Index of all 9 templates
│   ├── 01_generate_disease_list.md
│   ├── 02_generate_checklist.md
│   ├── 03_generate_scenario_draft.md
│   ├── 04_generate_scenario_polish.md
│   ├── 05_runtime_checklist.md     Runtime-side variant of the checklist prompt
│   ├── 06_chatbot_system.md
│   ├── 07_grading_checklist.md
│   ├── 08_grading_relationship.md
│   ├── 09_grading_feedback.md
│   └── en/                         Mirror of the above, in English
├── data/
│   ├── samples/                    Tiny example I/O committed to the repo
│   └── seed/                       gitignored — corpus + run outputs
├── docs/
│   ├── pipeline.md                 Data-generation flow
│   ├── runtime.md                  Runtime + grading flow
│   └── dataset_card.md
├── run_all.sh                      bulk dataset generation
├── run_demo.sh                     interactive single-patient demo
├── requirements.txt
├── .env.example
└── LICENSE
```

## Models and decoding

| Component | Model | Temperature | Streaming | Seed |
|---|---|---|---|---|
| Data-gen stages 1, 3, 4 | gpt-4.1 | 0.2 | off | 42 |
| Runtime: simulated-patient chat | gpt-4o | 0.5 | **on** | 42 |
| Runtime: checklist / scenario / grading | gpt-4o | 0 | off | 42 |

Two distinct OpenAI models are used because the experiment evolved in two
phases. The data-generation pipeline (gpt-4.1) produced the bulk dataset;
the runtime simulator + grader (gpt-4o) were locked earlier and we keep
them as-run for reproducibility. The chat path uses temperature 0.5 so the
simulated patient does not produce identical replies on identical inputs;
all other LLM calls are deterministic (temperature 0) with `seed=42` for
best-effort reproducibility under OpenAI's seeded-completion API.

## Installation

```bash
git clone <this-repo>
cd <repo>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # then put your OpenAI key in .env
```

## Quickstart — interactive demo

```bash
bash run_demo.sh
# or, in English:
bash run_demo.sh --lang en
```

The demo loads `data/samples/patient/example_patient.json`, runs an
interactive history-taking session in the terminal, and on `exit` prints
the auto-graded result (checklist score, five 1–5 relationship scores,
total score, letter grade, and a 350-word OSCE-format feedback report).

## Bulk data generation

Place one UTF-8 text file per chief complaint under `data/seed/`, then run:

```bash
bash run_all.sh
```

A synthetic placeholder reference file is shipped at
[`data/samples/input/cough.txt`](data/samples/input/cough.txt) — copy it
into `data/seed/` for a single-symptom dry run.

A full run over an 80-symptom corpus takes roughly 3–4 hours; the limiting
factor is the OpenAI rate budget for stage 4 (the longest two-step
generation).

## Running stages individually

```bash
python -m src.pipeline.stage1_process_disease_list
python -m src.pipeline.stage2_merge_json
python -m src.pipeline.stage3_generate_checklist [--test]
python -m src.pipeline.stage4_generate_scenario \
    [--symptom-limit N] [--disease-limit N] [--batch-size N]
```

## Citation

```bibtex
@inproceedings{anonymous2026osce,
  title  = {<paper title>},
  author = {<authors>},
  booktitle = {NeurIPS},
  year   = {2026}
}
```

## License

Code is released under the [MIT License](LICENSE). The seed corpus and
generated dataset are licensed separately — see
[`data/README.md`](data/README.md) and
[`docs/dataset_card.md`](docs/dataset_card.md).
