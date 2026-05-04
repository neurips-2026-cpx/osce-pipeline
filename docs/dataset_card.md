# Dataset Card

A short NeurIPS-style dataset card. Replace the placeholders with concrete
numbers from your final release before submission.

## Motivation

Korean OSCE training materials are scarce, expensive to author by hand,
and rarely available in machine-readable form. This dataset provides
structured patient cohorts, OSCE-style interview checklists, and
voice-ready standardised-patient scripts that can drive an LLM-based mock
patient simulator. The intended consumers are medical educators, OSCE
researchers, and developers building Korean clinical-skills tutors.

## Composition

Each row in the final release is one fictional patient and contains:

- chief complaint (`symptom`)
- diagnosis (`disease`)
- demographic + vital block (`name`, `age`, `gender`, `vital_sign`)
- structured OSCE checklist (`checklist`) — list of `(interview_item,
  purpose)` pairs, ≥ 20 items
- standardised-patient script (`prompt`) — 4–5 paragraph Korean monologue,
  voice-ready (numerals spelled out, lay vocabulary)

Approximate scale at release time: **TODO — fill in symptoms, patients,
total tokens once frozen.**

## Collection process

Synthesised end-to-end with `gpt-4.1` from a per-symptom reference corpus
(medical-education chapters). The four-stage pipeline is the entire
"collection" process — there is no separate human authoring step. See
[`pipeline.md`](pipeline.md) and the prompt documentation under
[`../prompts/`](../prompts/).

The runtime + grading path used `gpt-4o`. The auto-grader's calibration
references and the simulator system prompt are documented in
[`runtime.md`](runtime.md) and prompts 5–9 under [`../prompts/`](../prompts/).

## Preprocessing

- Stage 1 outputs are validated against a JSON schema by
  `src.utils.trimAndLoadJson`, which is tolerant of trailing commas and
  control characters that appear occasionally in LLM JSON output.
- Stage 4 polish enforces voice-ready surface form: Arabic numerals
  expanded, medical jargon replaced with lay vocabulary, sentences
  atomised.

## Recommended uses

- Training and evaluating LLM-based standardised-patient simulators.
- Benchmarking automated OSCE scoring against checklist rubrics.
- Augmenting Korean medical-dialogue corpora.

## Limitations and risks

- All patients, names, and case details are **synthetic**. They are not
  drawn from real clinical encounters.
- The reference corpus is a closed Korean medical-education set; coverage
  reflects what that corpus emphasises. Expect over-representation of
  conditions covered in undergraduate OSCE curricula and
  under-representation of rarer specialties.
- Both gpt-4.1 (data-gen) and gpt-4o (runtime + grader) occasionally
  fabricate plausible-sounding but clinically marginal items. Do not use
  these artifacts for clinical decision support; use only for
  *educational simulation*.
- Korean-only canonical release; English variants ship as alternative
  prompts but were not used in the experiment.

## Distribution

- Code and prompts: this repository, MIT licensed.
- Generated artifacts: distributed separately. **TODO — link the release
  / HuggingFace dataset URL and the artifact license once published.**

## Maintenance

Bug reports and reproduction questions: open an issue against this
repository. The seed corpus is closed; contributions to the *pipeline*
(prompts, post-processing, evaluation harnesses) are welcome.
