# Prompt 3 (English) — `generate_scenario_2_en` (draft)

| | |
|---|---|
| **Source** | [`src/prompts/en.py`](../../src/prompts/en.py) |
| **Used by** | [`src/pipeline/stage4_generate_scenario.py`](../../src/pipeline/stage4_generate_scenario.py), step 1 of 2 |
| **Model** | gpt-4.1, temperature 0.2, seed 42 |
| **Output format** | free-form English prose (no markdown) |
| **Korean original** | [`../03_generate_scenario_draft.md`](../03_generate_scenario_draft.md) |

## Purpose

First half of the two-step scenario generator. Produces a 2,000–2,500-
character English standardised-patient scenario that introduces the
patient, describes the chief complaint in clinically rich detail,
enumerates pertinent positives and negatives, gives the past medical /
family / social / medication history that the checklist questions probe,
and ends with the patient's worries.

The output is a *draft* in casual register; prompt 4 polishes it for
voice playback.

## Inputs

| Variable | Type | Source |
|---|---|---|
| `{patient_name}` | string | from stage 1 |
| `{patient_age}`  | int    | from stage 1 |
| `{sex}`          | string | from stage 1 |
| `{symptom}`      | string | chief complaint |
| `{disease}`      | string | diagnosis |
| `{vital_sign}`   | string | block, from stage 1 |
| `{checklist}`    | string | the checklist rendered into a markdown table by `src.utils.checklist_to_markdown` |
| `{book_content}` | string | per-symptom reference chapter |

## Notes

The few-shot example uses haematuria — same anchoring pattern as the
Korean original. Date ranges use `~` rather than `-` so prompt 4 can
rewrite them as "five or six".

## Prompt body (verbatim)

```text
We are building an OSCE scenario. The scenario must describe the chief complaint in detail and cover related symptoms, family history, social history, past medical history, and medication history. It must also let the patient answer every item on the checklist. Use the reference knowledge. Match the example format. Do not use markdown. When expressing date ranges, use ~ instead of -. Write in casual register. Length must be between 2,000 and 2,500 characters. Output the scenario directly with no preamble. Do not repeat the '## Checklist' or '## Patient information' headings inside the scenario.

## Checklist
{checklist}

## Reference knowledge
{book_content}

## Scenario example 1:

Robert Hayes is a 28-year-old male. Robert came to the hospital because of red urine that started 3 days ago. He had cold symptoms beginning 7 days ago, and the day before the red urine appeared he ran a fever up to 39 degrees with myalgia. The myalgia and fever peaked the evening 4 days ago, and the next morning, 3 days ago, he started seeing red urine. The colour was a deep reddish-brown that started very dark and gradually faded to a deep amber today. Robert has never been told he had haematuria, proteinuria, or kidney disease before. He is not taking any prescription drugs, herbal medicine, or supplements. He has been told that his blood pressure runs high, but he never thought it serious enough to see a doctor and does not remember the exact numbers. This is the first time his urine has looked unusual. There was no abdominal, flank, or distal urethral pain when passing the red urine. He thinks there may have been a small amount of foam in the urine, though he is not sure.

Otherwise he had no generalised weakness. There was no weight gain or loss. He had no headache. He was not dizzy. He had no fever today. He was not chilled or shivery. He had no muscle pain today. He had no night sweats. He had no cough. He had no sputum. He had no rhinorrhoea. He had no chest pain. He was not short of breath. He had no palpitations. He was not short of breath on exertion. He had no abdominal pain. His appetite was normal. He had no nausea. He did not vomit. He had no diarrhoea. He had no constipation. He had not vomited blood. His stool was not black. He had not passed bloody stool.

The first time he saw the haematuria, his cold symptoms had peaked the evening 4 days ago; he took an antipyretic, slept, and went to the bathroom in the morning, where he noticed the urine looked strange — a reddish-brown colour. He recalls buying Tylenol over the counter as the antipyretic. The next time he urinated he watched carefully from the start, and the urine was still deep red. He thought it was strange because there was no abdominal or pelvic pain when urinating. The day after that the colour was a slightly lighter red.

Robert has considered himself healthy and has essentially never been to a hospital. The check-ups he had during military service in his early twenties and at his workplace last year showed nothing unusual aside from slightly elevated blood pressure. He has smoked roughly one pack a day since military service. He drinks beer only at company gatherings, perhaps one or two glasses. He has worked an office job for the past 2 years and has annual workplace check-ups. He works out daily for an hour at the gym after work, but stopped going one week ago when the cold started. His diet leans towards meat and is on the salty side. He does not drink much water. Robert is an office worker who joined his current company 2 years ago. He typically works 9 to 6 and lives close by with his family. He has a girlfriend, has sex about once a week on average, and consistently uses a condom. He graduated from a four-year university and served in the military during his second year of college. He went straight to his current company after graduation. His father has high blood pressure and takes blood-pressure medication. He has one older brother; his mother and brother have no notable health issues.

Robert is worried about the red urine; he searched online, found the term "haematuria", and read that it can be associated with stones or cancer. He is anxious that he might have a serious illness. He wonders whether he can get tested today and see results, and whether admission or further work-up will be needed.

## Patient information
Name: {patient_name}
Age: {patient_age}
Sex: {sex}
Symptom: {symptom}
Disease: {disease}
Vital signs:
{vital_sign}

## {disease} scenario:
```
