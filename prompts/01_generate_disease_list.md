# Prompt 1 — `generate_disease_list_0`

| | |
|---|---|
| **Source** | [`src/prompts/ko.py`](../src/prompts/ko.py) |
| **Used by** | [`src/pipeline/stage1_process_disease_list.py`](../src/pipeline/stage1_process_disease_list.py) |
| **Model** | gpt-4.1, temperature 0.2, seed 42 |
| **Output format** | JSON inside a ```` ```json ```` fence |

## Purpose

Given a chief complaint and the corresponding textbook chapter, synthesise
five fictional patients who could plausibly present with that complaint.
Each patient is annotated with the most likely disease, a culturally
appropriate Korean name, age, gender, and vital signs.

The diversity of diseases per symptom (one cough may map to pneumonia,
bronchitis, COPD exacerbation, lung cancer, …) seeds the rest of the
pipeline so that the eventual checklists and scenarios cover a realistic
differential.

## Inputs

| Variable | Type | Source |
|---|---|---|
| `{symptom}` | string | The chief-complaint label, e.g. `"기침이 나요"`. Derived from the seed `.txt` file's stem. |
| `{book_content}` | string | The full per-symptom reference chapter read from `data/seed/{symptom}.txt`. |

## Output schema

```json
{
  "symptom": "<chief complaint, mirrors {symptom}>",
  "patients": [
    {
      "disease": "<plausible diagnosis>",
      "name":    "<Korean given+family name>",
      "age":     <int>,
      "gender":  "남성|여성",
      "vital_sign": "혈압 : <bp> mmHg\n맥박 : <hr> 회/분\n호흡 : <rr> 회/분\n체온 : <t>°C"
    },
    ...  // five entries
  ]
}
```

## Notes

- The prompt explicitly forbids generic Korean names (철수, 영희) so that
  later artifacts read like real OSCE cases.
- Vitals are constrained only by their format string — the model picks
  values consistent with the disease (e.g. tachypnea + fever for
  pneumonia).
- The few-shot example uses `"기침이 나요"` (cough) as a worked illustration.
  The example is written into the prompt body and is the same regardless
  of the target symptom.

## Prompt body (verbatim)

```text
증상에 따라 환자 정보를 JSON 형식으로 생성해 주세요. 질환은 레퍼런스 지식에 있는 주요 질병을 참고하여 작성하도록 합니다. 환자 정보 5개씩 생성합니다.
각 환자 정보는 다음 항목을 포함해야 합니다:

symptom: 주어진 증상
disease: 레퍼런스 지식에 기반한 해당 증상과 관련된 주요 질병
name: 해당 질환에 어울리는 한국식 이름(철수, 영희 같은 흔한 이름은 사용하지 않습니다.)
age: 해당 질환에 걸릴 가능성이 높은 연령
gender: 질환의 통계적 특성을 반영한 성별

## 레퍼런스 지식:
{book_content}

## 출력 형식 (JSON 예시):
```json
{
  "symptom": "기침이 나요",
  "patients": [
    {
      "disease": "폐렴",
      "name": "이영호",
      "age": 65,
      "gender": "남성",
      "vital_sign": "혈압 : 130/85 mmHg\n맥박 : 95 회/분\n호흡 : 24 회/분\n체온 : 38.3°C"
    },
    {
      "disease": "기관지염",
      "name": "이수진",
      "age": 34,
      "gender": "여성",
      "vital_sign": "혈압 : 118/76 mmHg\n맥박 : 88 회/분\n호흡 : 20 회/분\n체온 : 37.8°C"
    },
    {
      "disease": "감기",
      "name": "정민호",
      "age": 27,
      "gender": "남성"
      "vital_sign": "혈압 : 120/80 mmHg\n맥박 : 80 회/분\n호흡 : 18 회/분\n체온 : 37.5°C"
    }
  ]
}
```

## 환자 정보:
증상 : {symptom}

답:
```

## English summary of the prompt

> Generate five fictional patients in JSON for the given chief complaint.
> Each entry must include the symptom, a likely disease drawn from the
> supplied reference chapter, an authentic Korean name (avoid the
> stereotypical 철수/영희), an age and gender that fit the disease's
> epidemiology, and vital signs in the exact format shown. The reference
> chapter is supplied as `{book_content}`; the few-shot example for cough
> illustrates the schema.
