# OSCE Simulated-Patient Pipeline

A unified, end-to-end framework for synthesising and evaluating Korean OSCE
(Objective Structured Clinical Examination) cases with large language models.
The repository covers two complementary halves:

1. **Data generation** — turns per-symptom medical reference text into a
   structured corpus of fictional patients, OSCE-style interview checklists,
   and voice-ready standardised-patient scenarios.
2. **Runtime + auto-grading** — drives a simulated-patient chat from any of
   those scenarios, then auto-grades the student's session against the
   checklist and a five-dimension patient–doctor-relationship rubric.

This release accompanies our NeurIPS submission. The seed corpus and the
full released dataset are distributed separately — see
[`data/README.md`](data/README.md).

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

| Component | Model | Temperature | Seed |
|---|---|---|---|
| Data-gen stages 1, 3, 4 | gpt-4.1 | 0.2 | 42 |
| Runtime: checklist / scenario / grading | gpt-4o | 0 | 42 |

Two distinct OpenAI models are used because the experiment evolved in two
phases. The data-generation pipeline (gpt-4.1) produced the bulk dataset;
the runtime + grader (gpt-4o) were locked earlier and we keep them as-run
for reproducibility. All LLM calls use `seed=42` for best-effort
reproducibility under OpenAI's seeded-completion API.

## Installation

```bash
git clone <this-repo>
cd <repo>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # then put your OpenAI key in .env
```

## Bulk data generation

Place one UTF-8 text file per chief complaint under `data/seed/`, then run:

```bash
bash run_all.sh
```

A synthetic placeholder reference file is shipped at
[`data/samples/input/cough.txt`](data/samples/input/cough.txt) — copy it
into `data/seed/` for a single-symptom dry run.

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
