# Prompt 4 — `generate_scenario_3` (polish)

| | |
|---|---|
| **Source** | [`src/prompts/ko.py`](../src/prompts/ko.py) |
| **Used by** | [`src/pipeline/stage4_generate_scenario.py`](../src/pipeline/stage4_generate_scenario.py), step 2 of 2 |
| **Model** | gpt-4.1, temperature 0.2, seed 42 |
| **Output format** | free-form Korean prose |

## Purpose

Take the draft scenario from prompt 3 and rewrite it as a clean,
voice-ready script for the simulated patient. The order and content of the
narrative are preserved; only the surface form changes.

The polished output is what the downstream simulator actually consumes —
it is attached to each patient under the `prompt` field of
`all_disease_with_scenarios.json`.

## Inputs

| Variable | Type | Source |
|---|---|---|
| `{scenario}` | string | the draft produced by prompt 3 |

## The eight rewrite rules

1. Every sentence must read naturally aloud.
2. Arabic numerals are spelled out (`20` → `이십`, `1주일` → `일주일`,
   `2kg` → `이 키로그람`, `5~6회` → `오에서 육회`).
3. Each sentence is a simple declarative, short enough to speak verbatim
   as a patient line.
4. Sentences are atomised — one or two facts each. The example given in
   the prompt:
   *"모의환자는 평소 건강한 편이었고, 특별한 만성질환이나 신장 질환을 진단받은 적이 없다"* →
   *"모의환자는 평소 건강한 편이었다. 만성 질환이나 신장 질환이 있다고 들은 적은 없다."*
5. Where medications or events are mentioned, include both onset and
   duration.
6. The narrative is split into 4–5 paragraphs: self-introduction →
   symptoms → meds + social history → other.
7. Medical jargon is replaced with lay vocabulary (`편도` → `목 안쪽`,
   `농가진` → `농`).
8. No preamble — emit the rewritten scenario directly.

## Notes

- This is a pure rewrite step. The model is told not to alter content or
  ordering, only the surface form.
- Failure mode to watch for: the model occasionally over-corrects rule 2
  by spelling out numbers inside lab values that should remain numerical.
  We accept this since the simulator never voices vital-sign blocks
  verbatim.

## Prompt body (verbatim)

```text
다음 LLM 기반 모의환자 구현용 임상시나리오를 다듬고 싶습니다. 내용과 순서는 고치지 말고, 몇가지 수정사항을 반영하여 시나리오를 다시 작성합니다.

1) 모든 글은 소리내어 읽었을 때 자연스러운 형태여야 합니다.
2) 아라비아 숫자는 모두 글로 작성합니다. 20->이십, 30->삼십, 5->오 와 같이 글로 바꾸어주고, "1주일" -> "일주일", "2kg" -> "이 키로그람", "5~6회" -> "오에서 육회" 등으로 읽을 수 있는 형태로 변경합니다.
3) 각 문장은 평서문 형태로 작성되어야 하고, 문장 그대로 모의 환자의 답변으로 사용될 수 있을 정도로 쉽고 읽히기 쉬우며 간결해야 합니다.
4) 각 문장은 간결히 작성되어야 해. 예를들어 "모의환자는 평소 건강한 편이었고, 특별한 만성질환이나 신장 질환을 진단받은 적이 없다." 는 "모의환자는 평소 건강한 편이었다. 만성 질환이나  신장 질환이 있다고 들은 적은 없다"와 같이 모든 문장은 독립적이고 간결하게 한 두가지 내용만을 포함하는 것이 좋습니다.
5) 복용한 약이 있거나, 특정한 이벤트가 있었을 경우, 가급적 언제부터 복용했고 언제부터 시작되었는지를 문장에 포함합니다.
6) 자기소개/증상관련언급/약제력및사회력관련언급/그외로 4~5개 문단으로 줄바꿈을 사용하여 나누어 줍니다.
7) 의사가 쓸법한 단어나 문장은 일반인이 사용하는 말로 가급적 바꾸어 줍니다. 예를들어 "편도" -> "목 안쪽", "농가진" -> "농" 등으로 고쳐주고, 마찬가지로 한글로 읽었을 때 어색하지 않도록 수정해주었으면 합니다.
8) 부연설명 없이 바로 작성합니다.

이제 아래에 수정할 시나리오를 제시합니다. 위 원칙들에 따라 시나리오를 수정합니다.

## 수정해야할 시나리오:
{scenario}

## 수정된 시나리오:
```

## English summary of the prompt

> Polish the draft scenario into a voice-ready Korean script. Preserve
> content and order; rewrite the surface form. Spell out numerals,
> atomise sentences, replace medical jargon with lay language, split into
> four or five paragraphs (intro / symptoms / meds + social / other),
> include onset and duration whenever a medication or event is mentioned.
> Output the rewritten scenario only.
