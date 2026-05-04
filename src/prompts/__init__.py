"""Bilingual prompt module.

The pipeline (stages 1–4) and the runtime simulator + grader all draw their
prompts from the same module so language switching is a single argument.

Usage:
    from src.prompts import get_prompts
    P = get_prompts("ko")     # or "en"
    template_str = P.CHECKLIST_PROMPT_TEMPLATE
    template_str = P.GENERATE_DISEASE_LIST  # only available in `ko`/`en`

For backwards compatibility with the data-generation pipeline, the four
templates that pipeline scripts originally imported by name are also
re-exported below in their canonical Korean form.
"""

from . import en, ko

_LANGS = {"ko": ko, "en": en}


def get_prompts(lang: str = "ko"):
    """Return the prompt module for the given language code."""
    if lang not in _LANGS:
        raise ValueError(f"Unsupported language: {lang}. Choose from {list(_LANGS)}.")
    return _LANGS[lang]


# Backwards-compatible re-exports for the data-generation pipeline (stages 1-4).
# These point at the Korean originals, which is what the experiment used.
generate_disease_list_0 = ko.GENERATE_DISEASE_LIST
generate_checklist_1 = ko.CHECKLIST_PROMPT_TEMPLATE_DATAGEN
generate_scenario_2 = ko.SCENARIO_PROMPT_TEMPLATE_1
generate_scenario_3 = ko.SCENARIO_PROMPT_TEMPLATE_2

generate_disease_list_0_en = en.GENERATE_DISEASE_LIST
generate_checklist_1_en = en.CHECKLIST_PROMPT_TEMPLATE_DATAGEN
generate_scenario_2_en = en.SCENARIO_PROMPT_TEMPLATE_1
generate_scenario_3_en = en.SCENARIO_PROMPT_TEMPLATE_2
