# Prompt 2 (English) — `generate_checklist_1_en`

| | |
|---|---|
| **Source** | [`src/prompts/en.py`](../../src/prompts/en.py) |
| **Used by** | [`src/pipeline/stage3_generate_checklist.py`](../../src/pipeline/stage3_generate_checklist.py) (when imported as `generate_checklist_1`) |
| **Model** | gpt-4.1, temperature 0.2, seed 42 |
| **Output format** | JSON inside a ```` ```json ```` fence |
| **Korean original** | [`../02_generate_checklist.md`](../02_generate_checklist.md) |

## Purpose

Build the per-patient OSCE scoring checklist: at least 20 interview items
that an examinee should ask to evaluate the patient's chief complaint and
reach the underlying diagnosis. The checklist must cover symptom analysis,
past medical / family / social history, and patient education.

The prompt is anchored by a single fully written-out hematuria example —
intentionally a different complaint from any production target so the
example anchors *structure* (granularity, phrasing, ≥20 items, paired
`interview_item` + `purpose`) without leaking content.

## Inputs

| Variable | Type | Source |
|---|---|---|
| `{patient_name}` | string | from stage 1 output |
| `{patient_age}`  | int    | from stage 1 output |
| `{sex}`          | string | gender |
| `{symptom}`      | string | chief complaint |
| `{disease}`      | string | working diagnosis |
| `{vital_sign}`   | string | block as produced by stage 1 |
| `{book_content}` | string | per-symptom reference chapter |

## Output schema

```json
{
  "diseases": [
    {
      "symptom": "<the chief complaint>",
      "patients": [
        {
          "interview_item": "<a single question or instruction>",
          "purpose":        "<why the question is on the rubric>"
        },
        ...  // ≥ 20 items
      ]
    }
  ]
}
```

The wrapping `diseases > patients` shape is preserved so downstream stages
need no changes.

## Prompt body (verbatim)

```text
We are building a question checklist that will serve as the OSCE (Objective Structured Clinical Examination) scoring rubric. The checklist must include the most important history-taking questions about the chief complaint, important questions about social history, past medical history, and family history, and patient education/instructions to deliver in the clinic.

## Patient information:
Name: {patient_name}
Age: {patient_age}
Sex: {sex}
Symptom: {symptom}
Disease: {disease}
Vital signs: {vital_sign}

### Reference knowledge:
{book_content}

Below is an example checklist actually used in a hematuria OSCE station. Following the same format, write at least 20 list-style questions that should be asked in the OSCE for a "{disease}" patient presenting with the chief complaint "{symptom}". Each question should ask about a single thing wherever possible. The checklist must include the questions that allow the examinee to arrive at "{disease}".
Return JSON.

### Example checklist:
{
  "diseases": [
    {
      "symptom": "blood in urine",
      "patients": [
        { "interview_item": "Asked about the colour of the red urine, presence of blood clots, and timing (initial/terminal).", "purpose": "Characterise the haematuria; localise the lesion." },
        { "interview_item": "Asked whether the patient has had haematuria before or any prior abnormal urinalysis.", "purpose": "Recurrence and underlying disease." },
        { "interview_item": "Asked about precipitating factors such as exercise, fever, or infection.", "purpose": "Differentiate exertional/infectious haematuria." },
        { "interview_item": "Asked whether the patient had flank pain.", "purpose": "Differentiate urolithiasis or pyelonephritis." },
        { "interview_item": "Asked whether the patient had oedema.", "purpose": "Nephrotic syndrome or renal dysfunction." },
        { "interview_item": "Asked about at least one of skin rash or joint pain.", "purpose": "Screen for systemic disease such as vasculitis." },
        { "interview_item": "Asked whether urination was uncomfortable or painful.", "purpose": "Lower urinary tract infection such as cystitis." },
        { "interview_item": "Asked about at least two of frequency, residual urine, urgency, or nocturia.", "purpose": "Lower urinary tract irritative symptoms." },
        { "interview_item": "Asked whether there was foamy urine.", "purpose": "Concomitant proteinuria — suspect glomerular disease." },
        { "interview_item": "Asked about medications, especially aspirin and anticoagulants.", "purpose": "Drug-related bleeding." },
        { "interview_item": "Asked whether the patient has a history of urinary tract infection or kidney disease.", "purpose": "Underlying disease." },
        { "interview_item": "Asked whether the family has at least two of haematuria, kidney disease, or genitourinary cancer.", "purpose": "Differentiate hereditary disease." },
        { "interview_item": "Asked about both alcohol consumption and smoking.", "purpose": "Risk factors for bladder and renal cancer." },
        { "interview_item": "Took a sexual history including any recent unfamiliar partners.", "purpose": "Differentiate STI-related urinary infection." },
        { "interview_item": "(Male) Asked about weak urinary stream or straining.", "purpose": "Evaluate benign prostatic hyperplasia." },
        { "interview_item": "Explained possible causes such as glomerulonephritis or IgA nephropathy.", "purpose": "Share suspected diagnosis and educate." },
        { "interview_item": "Explained that a renal biopsy may be needed to identify the cause.", "purpose": "Explain the need for further work-up." },
        { "interview_item": "Explained that smoking may be related to haematuria and recommended cessation.", "purpose": "Health-maintenance counselling." }
      ]
    }
  ]
}

{disease} checklist:
```
