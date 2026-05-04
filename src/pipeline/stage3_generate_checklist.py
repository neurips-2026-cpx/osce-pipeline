"""Stage 3: Generate OSCE-style interview checklists for each patient.

Reads ``data/seed/all_diseases.json`` (output of stage 2, shape
``{"diseases": [{"symptom", "patients": [...]}, ...]}``), prompts gpt-4.1 with
the per-symptom textbook chapter as reference, and writes
``data/seed/all_disease_with_checklists.json`` with a ``checklist`` field added
to every patient.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from src.prompts import generate_checklist_1, generate_checklist_1_en

# Language switch: ``OSCE_LANG=en`` selects the English prompt; default is Korean.
if os.getenv("OSCE_LANG") == "en":
    generate_checklist_1 = generate_checklist_1_en
from src.utils import trimAndLoadJson
from src.logging_utils import (
    setup_logging,
    log_llm_interaction,
    log_error,
    log_step_start,
    log_step_end,
)


SCRIPT_NAME = "stage3_generate_checklist.py"
SEED_DIR = Path("data/seed")
INPUT_FILE = SEED_DIR / "all_diseases.json"


def load_book_content(symptom: str) -> str:
    """Read the textbook chapter for ``symptom`` from ``data/seed/{symptom}.txt``."""
    file_path = SEED_DIR / f"{symptom}.txt"
    if not file_path.exists():
        return f"Reference textbook content for '{symptom}' was not found."
    return file_path.read_text(encoding="utf-8")


def main() -> None:
    setup_logging()
    load_dotenv()

    parser = argparse.ArgumentParser(description="Generate OSCE checklists.")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test mode: process only the first 2 patients per symptom.",
    )
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set. Copy .env.example to .env and fill it in.")

    if not INPUT_FILE.exists():
        sys.exit(f"'{INPUT_FILE}' is missing. Run stages 1 and 2 first.")

    disease_data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    if "diseases" not in disease_data:
        sys.exit(f"'{INPUT_FILE}' has unexpected shape; expected key 'diseases'.")

    template = PromptTemplate.from_template(generate_checklist_1)
    llm = ChatOpenAI(model="gpt-4.1", temperature=0.2, seed=42)
    chain = template | llm

    output_file = (
        SEED_DIR / ("all_disease_test.json" if args.test else "all_disease_with_checklists.json")
    )

    print("Generating OSCE checklists...")
    for symptom_entry in disease_data["diseases"]:
        symptom = symptom_entry["symptom"]
        print(f"\nSymptom: {symptom}")
        log_step_start(SCRIPT_NAME, "generate_checklist", f"symptom: {symptom}")

        book_content = load_book_content(symptom)
        patients = symptom_entry["patients"][:2] if args.test else symptom_entry["patients"]

        for patient in patients:
            if "checklist" in patient:
                print(f"  skip {patient['disease']} (checklist already present)")
                continue

            disease = patient["disease"]
            input_data = {
                "symptom": symptom,
                "patient_name": patient["name"],
                "patient_age": patient["age"],
                "sex": patient["gender"],
                "vital_sign": patient.get("vital_sign", ""),
                "book_content": book_content,
                "disease": disease,
            }

            try:
                formatted_prompt = template.format(**input_data)
                result = chain.invoke(input_data)

                log_llm_interaction(
                    SCRIPT_NAME,
                    f"generate_checklist - {symptom} - {disease}",
                    {"formatted_prompt": formatted_prompt, "input_data": input_data},
                    result,
                )

                try:
                    patient["checklist"] = trimAndLoadJson(result.content)
                    print(f"  OK: {disease}")
                    log_step_end(SCRIPT_NAME, f"generate_checklist - {disease}", True, "checklist generated")
                except Exception as exc:
                    print(f"  JSON parse error ({disease}): {exc}")
                    patient["checklist_raw"] = result.content
                    log_error(SCRIPT_NAME, f"json_parse - {disease}", str(exc), result.content[:500])

                time.sleep(1)

            except Exception as exc:
                print(f"  generate error ({disease}): {exc}")
                log_error(SCRIPT_NAME, f"generate_checklist - {disease}", str(exc))

    output_file.write_text(
        json.dumps(disease_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nDone. Output: {output_file}")


if __name__ == "__main__":
    main()
