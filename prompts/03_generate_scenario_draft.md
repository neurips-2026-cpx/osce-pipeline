# Prompt 3 — `generate_scenario_2` (draft)

| | |
|---|---|
| **Source** | [`src/prompts/ko.py`](../src/prompts/ko.py) |
| **Used by** | [`src/pipeline/stage4_generate_scenario.py`](../src/pipeline/stage4_generate_scenario.py), step 1 of 2 |
| **Model** | gpt-4.1, temperature 0.2, seed 42 |
| **Output format** | free-form Korean prose (no markdown) |

## Purpose

First half of the two-step scenario generator. Given the patient metadata,
their checklist, and the per-symptom reference chapter, produce a 2,000–
2,500-character standardized-patient scenario that:

- introduces the patient and their chief complaint,
- describes the symptom in clinically rich detail,
- enumerates pertinent positives and negatives across body systems,
- gives the past medical / family / social / medication history that the
  checklist questions probe,
- expresses the patient's worries and expectations.

The result is a *draft* in informal Korean (반말). Prompt 4 polishes it
for natural-sounding voice playback.

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

## Output

A multi-paragraph Korean narrative, 2,000–2,500 characters, no markdown,
ready for prompt 4. The model is told to omit any "## checklist" or "##
patient info" section since those would duplicate prompt input.

## Notes

- The prompt embeds a fully written-out hematuria scenario as a stylistic
  exemplar — same anchoring pattern as prompt 2.
- Date ranges are written with `~` (e.g. `5~6회`) instead of `-` so that
  prompt 4 can rewrite them as "오에서 육 회".
- The model is told to use 반말 (informal speech) — the polished version
  in prompt 4 keeps that register.

## Prompt body (verbatim)

```text
OSCE용 시나리오를 개발을 할 것입니다. 시나리오에는 증상에 대한 자세한 표현, 관련증상, 가족력, 사회력, 질환력, 약물 복용력 등이 자세히 설명되어야 합니다. 또한 체크리스트에 모든 답변이 가능하도록 생성이 되어야 합니다. 레퍼런스 지식을 참고하여 작성합니다. 참고형식처럼 만들어줍니다. 마크다운을 사용하지 않습니다. 기간 등을 표현할 때 - 대신 ~을 사용합니다. 반말로 작성합니다. 2000자 이상 2500자 이하로 작성합니다. 부연 설명 없이 바로 시나리오만 작성합니다. '## 체크리스트'와 '## 환자 정보' 를 시나리오에 한 번 더 작성하지 않습니다.

## 체크리스트
{checklist}

## 레퍼런스 지식
{book_content}

## 시나리오 예시 1 :

정진수는 28세 남자이다. 정진수는 3일 전부터 시작된 붉은색 소변으로 병원에 왔다. 정진수는 7일 전부터 감기 증상이 있었으며 붉은색 소변을 보기 전날 39도까지 열이 나고 근육통이 있었다. 근육통과 발열 증상이 가장 심하다고 생각된 건 4일 전 저녁이었고 그 다음날 아침인 3일 전 아침 붉은색 소변을 보기 시작하였다. 소변 색은 짙은 적갈색이었으며, 처음에는 진한 적갈색이었다가 점차 옅어져서 오늘은 짙은 호박색 정도의 소변을 보았다. 정진수는 이전에 혈뇨나 단백뇨, 신장 질환을 들은적이 없다. 따로 복용하는 약이나 한약, 건강식품 및 보조식품은 전혀 없다. 평소 혈압이 높다는 얘기를 들었으나 크게 심각하게 생각하지 않았고 병원에 간 적이 없었다. 혈압이 얼마인지는 정확히 기억나지 않는다. 소변이 이상하게 보인적은 이번이 처음이다. 붉은색 소변을 볼 때 복부 통증은 없었으며 옆구리 통증이나 요도 끝 통증은 전혀 없었다. 정확하지는 않지만 소변에 거품이 약간 섞여 있는 것 같았다.

그 외에 온몸에 힘이 없거나 하지는 않았다. 몸무게가 늘거나 줄지는 않았다. 머리가 아프지는 않았다. 어지럽지 않았다. 열이 나지는 않았다. 몸이 춥고 떨리지는 않았다. 근육이 아프지는 않았다. 식은땀은 없었다. 기침은 없었다. 가래는 없었다. 콧물은 없었다. 가슴 통증은 없었다. 숨이 차지는 않았다. 가슴이 두근거리는 증상은 없었다. 운동할 때 숨이 차지는 않았다. 배가 아프지는 않았다. 식욕은 정상이다. 구역감이 들지는 않았다. 토는 하지 않았다. 설사는 없다. 변비는 없다. 입에서 피를 토한 적은 없다. 변이 검은색은 아니었다. 피똥을 눈 적은 없다.

첫 혈뇨를 볼 당시 상황은 3일 전 감기 증상이 최고조이던 나흘 전 저녁, 해열제를 먹고 자고 일어나 아침 첫 소변을 보러 갔는데 나오는 소변색이 이상해서 보니 적갈색 소변이 보였다. 해열제는 약국에서 타이레놀을 사서 먹은 것으로 기억한다. 다음 소변을 볼 때는 처음부터 자세히 소변을 봤는데, 여전히 짙은 붉은색 소변을 보고 있었다. 소변볼 때 배나 아랫쪽 통증이 없었기 때문에 이상하다고 생각했다. 다음 날에는 조금 더 옅은 색의 붉은색 소변을 보았다.

정진수는 평소 건강하다고 생각해 왔으며 병원에는 전혀 가본적이 없다. 20대 초반 군대와 작년 직장에서 시행한 건강검진에서도 혈압이 조금 높다는 점 외에 다른 이상을 들은 적은 전혀 없다. 담배는 입대 이후로 평소 하루 한갑 정도 피우고 있다. 술은 회식때만 맥주 한두잔 정도 하는 정도이다. 2년 전부터 취직하여 사무직으로 일하고 있고 매년 직장 건강검진을 받고 있다. 운동은 평소 매일 1시간씩 퇴근 후 헬스장에서 하고 있다. 감기에 걸린 1주일 전부터는 헬스장에 가지 않았다. 식습관은 고기를 좋아하는 편이며 조금 짜게 먹는 편이다. 물을 많이 마시지는 않는다. 정진수는 회사원이며, 2년 전에 입사하였다. 보통 9시에서 6시까지 일하며, 가까운 곳에서 가족과 함께 생활한다. 여자친구가 있으며 평균 주 1회 정도 잠자리를 하며 성생활 때 마다 남성 피임기구를 잘 사용한다. 4년제 대학교를 졸업하였고 군대는 대학교 2학년에 다녀왔다. 대학 졸업 후 바로 현재 다니는 회사에 입사했다. 아버지는 평소 혈압이 높고 혈압약을 복용하고 있다고 알고 있다. 정진수에겐 형이 한 명 있으며 어머니와 형은 특별한 건강의 문제가 없다고 알고 있다.

정진수는 붉은색 소변이 걱정이 되며 인터넷에 검색을 해보니 혈뇨라는 것이 검색되었고, 결석이나 암의 위험이 있다고 보았다. 자신이 큰 병에 걸리지 않았는지 걱정이 많이 된다. 오늘 검사를 하고 결과를 볼 수 있을지 걱정이 되며, 입원이나 정밀검사가 필요할 지 궁금한 마음이다.

## 환자 정보
이름 : {patient_name}
나이 : {patient_age}
성별 : {sex}
증상 : {symptom}
질환 : {disease}
활력 정보 : \n{vital_sign}

## {disease} 시나리오:
```

## English summary of the prompt

> Write a 2,000–2,500-character Korean OSCE scenario for the given patient
> in informal speech. The scenario must (a) describe the chief complaint
> with rich detail, (b) cover related symptoms, (c) provide every datum
> the checklist could ask for, and (d) end with the patient's worries.
> Use ~ for ranges, no markdown, no headers. A full hematuria scenario is
> embedded as a worked example to anchor structure, length, and voice.
