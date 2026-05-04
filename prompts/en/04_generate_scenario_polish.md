# Prompt 4 (English) — `generate_scenario_3_en` (polish)

| | |
|---|---|
| **Source** | [`src/prompts/en.py`](../../src/prompts/en.py) |
| **Used by** | [`src/pipeline/stage4_generate_scenario.py`](../../src/pipeline/stage4_generate_scenario.py), step 2 of 2 |
| **Model** | gpt-4.1, temperature 0.2, seed 42 |
| **Output format** | free-form English prose |
| **Korean original** | [`../04_generate_scenario_polish.md`](../04_generate_scenario_polish.md) |

## Purpose

Take the draft scenario from prompt 3 and rewrite it as a clean,
voice-ready English script for the simulated patient. Order and content
are preserved; only the surface form changes.

## Inputs

| Variable | Type | Source |
|---|---|---|
| `{scenario}` | string | the draft produced by prompt 3 |

## The eight rewrite rules

1. Every sentence must read naturally aloud.
2. Arabic numerals are spelled out (`20` → `twenty`, `1 week` → `one week`,
   `2kg` → `two kilograms`, `5~6 times` → `five or six times`).
3. Each sentence is a simple declarative, short enough to be spoken
   verbatim by the simulated patient.
4. Sentences are atomised — one or two facts each.
5. Where medications or events are mentioned, include both onset and
   duration.
6. The narrative is split into 4–5 paragraphs: self-introduction →
   symptoms → meds + social history → other.
7. Medical jargon is replaced with lay vocabulary (`tonsil` →
   `back of the throat`, `impetigo` → `skin pus`).
8. No preamble — emit the rewritten scenario directly.

## Prompt body (verbatim)

```text
I want to polish the following clinical scenario for an LLM-based simulated patient. Do not change content or order; rewrite the surface form to satisfy the rules below.

1) Every line must read naturally when spoken aloud.
2) Spell out numerals in words (e.g. 20 -> twenty, 30 -> thirty, "1 week" -> "one week", "2kg" -> "two kilograms", "5~6 times" -> "five or six times").
3) Each sentence must be a simple declarative, short enough to be spoken verbatim by the simulated patient.
4) Atomise sentences. For example, "The simulated patient was generally healthy and had not been diagnosed with any chronic disease or kidney disease" becomes "The simulated patient was generally healthy. He had not been told he has any chronic or kidney disease." Each sentence should be independent and concise, carrying only one or two facts.
5) Whenever a medication or specific event is mentioned, include both onset and duration.
6) Split into 4–5 paragraphs separated by blank lines: self-introduction / symptoms / medication and social history / other.
7) Replace medical jargon with lay terms where possible (e.g. "tonsil" -> "back of the throat", "impetigo" -> "skin pus") and keep wording natural when read aloud.
8) Output the rewritten scenario directly with no preamble.

Below is the scenario to revise. Rewrite it according to the rules above.

## Scenario to revise:
{scenario}

## Revised scenario:
```
