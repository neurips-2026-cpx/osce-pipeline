# Prompt 2 — `generate_checklist_1`

| | |
|---|---|
| **Source** | [`src/prompts/ko.py`](../src/prompts/ko.py) |
| **Used by** | [`src/pipeline/stage3_generate_checklist.py`](../src/pipeline/stage3_generate_checklist.py) |
| **Model** | gpt-4.1, temperature 0.2, seed 42 |
| **Output format** | JSON inside a ```` ```json ```` fence |

## Purpose

Build the per-patient OSCE scoring checklist: a list of at least 20
interview questions that an examinee should ask to evaluate this patient's
chief complaint and reach the disease that drives the case. The checklist
must cover the symptom analysis, past medical / family / social history,
and patient education.

The prompt is anchored by a single fully written-out example for hematuria
(혈뇨). The example is intentionally a different symptom from any target
case in production; this anchors the *structure* (granularity, phrasing,
20+ items, "interview_item" + "purpose" pairs) without leaking content for
the target disease.

## Inputs

| Variable | Type | Source |
|---|---|---|
| `{patient_name}` | string | from stage 1 output |
| `{patient_age}`  | int    | from stage 1 output |
| `{sex}`          | string | gender, from stage 1 |
| `{symptom}`      | string | chief complaint |
| `{disease}`      | string | the target diagnosis for this patient |
| `{vital_sign}`   | string | block as produced by stage 1 |
| `{book_content}` | string | per-symptom reference chapter from `data/seed/{symptom}.txt` |

`{symptom}` and `{disease}` are interpolated *twice* — once in the patient
metadata block and once in the trailing instruction line, to keep the
target salient when the model emits its list.

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

The wrapping `diseases > patients` shape is preserved through the
pipeline; downstream stage 4 reads `checklist['diseases'][i]['patients']`.

## Notes

- The instruction "한 질문에서는 가급적 하나의 질문만 물어보도록" pushes the
  model to avoid compound questions, which simplifies later scoring.
- Hematuria few-shot covers all four buckets: red-flag symptom probing,
  past medical/social history, patient education, and recommended next
  steps. This implicitly teaches the model the OSCE rubric structure.

## Prompt body (verbatim)

```text
의사실기시험인 OSCE 시험에서 채점표로 활용한 질문 체크리스트를 만드려고 합니다. 체크리스트에는 OSCE시험에서 평가해야 하는 증상에 대한 중요한 문진 질문과 사회력, 과거력, 가족력에 대한 중요한 질문, 그리고 환자 교육 및 진료실에서 해줄 수 있는 지침과 교육에 대한 내용을 포함하여야 합니다.

## 환자 정보:
이름 : {patient_name}
나이 : {patient_age}
성별 : {sex}
증상 : {symptom}
질환 : {disease}
활력 징후 : {vital_sign}

### 레퍼런스 지식 :
{book_content}

다음은 "혈뇨" OSCE에서 실제로 사용하는 예시 체크리스트입니다. 아래와 같은 형식으로 "{symptom}" 라는 주증상으로 온 "{disease}" 환자의 OSCE 시험에서 물어봐야 할 주요 질문을 20개 이상으로 리스트 형식으로 작성하도록 합니다. 한 질문에서는 가급적 하나의 질문만 물어보도록 질문 문장을 만들도록 합니다. 체크리스트에는 "{disease}"을 도출할 수 있는 주요 질문들이 포함되어야 합니다.
json 형태로 줘.

### 예시 체크리스트 :
{
  "diseases": [
    {
      "symptom": "혈뇨가 있어요",
      "patients": [
        { "interview_item": "붉은 소변의 색상, 피떡 포함 여부, 시기(처음/끝)를 물어보았다", "purpose": "혈뇨 양상 파악, 위치 감별" },
        { "interview_item": "과거에도 혈뇨가 있었는지, 소변검사 이상을 들은 적이 있는지 물어보았다", "purpose": "재발성 여부, 기저질환 가능성" },
        { "interview_item": "운동, 발열, 감염 등 혈뇨 유발 요인을 물어보았다", "purpose": "운동성/감염성 혈뇨 감별" },
        { "interview_item": "옆구리 통증이 있었는지 물어보았다", "purpose": "요로결석, 신우신염 감별" },
        { "interview_item": "부종이 있었는지 물어보았다", "purpose": "신증후군/신장 기능 이상" },
        { "interview_item": "피부 발진 또는 관절통 중 하나 이상을 물어보았다", "purpose": "전신 질환(혈관염 등) 감별" },
        { "interview_item": "배뇨 시 불편감 또는 통증이 있었는지 물어보았다", "purpose": "방광염 등 하부요로 감염" },
        { "interview_item": "빈뇨, 잔뇨감, 절박뇨, 야간뇨 중 2가지 이상을 물어보았다", "purpose": "하부요로 자극 증상 평가" },
        { "interview_item": "거품뇨가 있었는지 물어보았다", "purpose": "단백뇨 동반 여부 – 사구체성 질환 의심" },
        { "interview_item": "약물 복용 여부를 물어보았다 (특히 아스피린, 항응고제 등)", "purpose": "약제성 출혈 여부 확인" },
        { "interview_item": "과거 요로감염 또는 신장질환 병력이 있었는지 물어보았다", "purpose": "기저 질환 확인" },
        { "interview_item": "가족 중 혈뇨, 신장질환, 비뇨기계 암 병력이 있는지 2가지 이상 물어보았다", "purpose": "유전 질환 감별" },
        { "interview_item": "음주 및 흡연 여부를 모두 물어보았다", "purpose": "방광암, 신장암 위험 인자 평가" },
        { "interview_item": "최근 낯선 사람과의 성관계 등 성생활 관련 문진을 하였다", "purpose": "성병 관련 요로감염 감별" },
        { "interview_item": "(남성) 소변 줄기 약화 또는 힘줘야 소변 나오는지 물어보았다", "purpose": "전립선비대증 여부 평가" },
        { "interview_item": "사구체신염, IgA신증 등 혈뇨의 가능 원인에 대해 설명하였다", "purpose": "의심 진단 공유 및 교육" },
        { "interview_item": "혈뇨 원인 확인 위해 신장 조직검사가 필요할 수 있음을 설명하였다", "purpose": "추가 검사 필요성 설명" },
        { "interview_item": "흡연이 혈뇨와 관련 있을 수 있음을 설명하고 금연을 권고하였다", "purpose": "건강관리 교육" }
      ]
    }
  ]
}

{disease} 체크리스트:
```

## English summary of the prompt

> Build an OSCE-style scoring checklist of 20+ interview items for the
> given patient (`{patient_name}`, `{patient_age}`, `{sex}`, presenting
> with `{symptom}`, working diagnosis `{disease}`). Items must cover the
> symptom analysis, past medical / social / family history, and patient
> education. Each item is a single, atomic question paired with its
> rubric-style purpose. The model is anchored by one full hematuria
> example. Output is wrapped in a `diseases > patients` JSON block.
