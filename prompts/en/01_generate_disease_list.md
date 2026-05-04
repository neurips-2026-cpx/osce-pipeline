# Prompt 1 (English) — `generate_disease_list_0_en`

| | |
|---|---|
| **Source** | [`src/prompts/en.py`](../../src/prompts/en.py) |
| **Used by** | [`src/pipeline/stage1_process_disease_list.py`](../../src/pipeline/stage1_process_disease_list.py) (when imported as `generate_disease_list_0`) |
| **Model** | gpt-4.1, temperature 0.2, seed 42 |
| **Output format** | JSON inside a ```` ```json ```` fence |
| **Korean original** | [`../01_generate_disease_list.md`](../01_generate_disease_list.md) |

## Purpose

Given a chief complaint and the corresponding reference chapter, synthesise
five fictional patients who could plausibly present with that complaint.
Each patient is annotated with a likely disease, a plausible patient name,
age, gender, and vital signs.

## Inputs

| Variable | Type | Source |
|---|---|---|
| `{symptom}` | string | The chief-complaint label, e.g. `"cough"`. Derived from the seed `.txt` file's stem. |
| `{book_content}` | string | The full per-symptom reference chapter read from `data/seed/{symptom}.txt`. |

## Output schema

```json
{
  "symptom": "<chief complaint, mirrors {symptom}>",
  "patients": [
    {
      "disease":    "<plausible diagnosis>",
      "name":       "<patient name>",
      "age":        <int>,
      "gender":     "male|female",
      "vital_sign": "BP: <bp> mmHg\nHR: <hr> bpm\nRR: <rr>/min\nTemp: <t>°C"
    },
    ...  // five entries
  ]
}
```

## Prompt body (verbatim)

```text
Generate fictional patient information in JSON based on a chief complaint. Diseases must be drawn from the reference knowledge below. Generate exactly five patients.
Each patient entry must include:

symptom: the given chief complaint
disease: a major disease for that complaint, grounded in the reference knowledge
name: a plausible patient name (avoid generic placeholders like "John Doe" or "Jane Doe")
age: an age statistically appropriate for the disease
gender: a gender consistent with the disease's epidemiology

## Reference knowledge:
{book_content}

## Output format (JSON example):
```json
{
  "symptom": "cough",
  "patients": [
    {
      "disease": "Pneumonia",
      "name": "Robert Hayes",
      "age": 65,
      "gender": "male",
      "vital_sign": "BP: 130/85 mmHg\nHR: 95 bpm\nRR: 24/min\nTemp: 38.3°C"
    },
    {
      "disease": "Acute bronchitis",
      "name": "Emily Chen",
      "age": 34,
      "gender": "female",
      "vital_sign": "BP: 118/76 mmHg\nHR: 88 bpm\nRR: 20/min\nTemp: 37.8°C"
    },
    {
      "disease": "Common cold",
      "name": "Daniel Park",
      "age": 27,
      "gender": "male",
      "vital_sign": "BP: 120/80 mmHg\nHR: 80 bpm\nRR: 18/min\nTemp: 37.5°C"
    }
  ]
}
```

## Patient information:
symptom: {symptom}

Answer:
```
