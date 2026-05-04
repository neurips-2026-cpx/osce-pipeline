"""Stage 1: Generate synthetic patient cohorts from per-symptom textbook chapters.

Reads every ``*.txt`` file under ``data/seed/`` (one file per chief complaint),
prompts gpt-4.1 with the chapter as reference knowledge, and writes a JSON file
of five fictional patients with disease, name, age, gender, and vital signs to
``data/seed/results/{symptom}_diseases.json``. The consolidated output is
``data/seed/results/all_diseases.json``.
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from src.prompts import generate_disease_list_0, generate_disease_list_0_en

# Language switch: ``OSCE_LANG=en`` selects the English prompt; default is Korean.
if os.getenv("OSCE_LANG") == "en":
    generate_disease_list_0 = generate_disease_list_0_en
from src.utils import trimAndLoadJson
from src.logging_utils import (
    setup_logging,
    log_llm_interaction,
    log_error,
    log_step_start,
    log_step_end,
)


SCRIPT_NAME = "stage1_process_disease_list.py"
SEED_DIR = Path("data/seed")
RESULTS_DIR = SEED_DIR / "results"


def main() -> None:
    setup_logging()
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set. Copy .env.example to .env and fill it in.")

    if not SEED_DIR.exists():
        sys.exit(
            f"Seed directory '{SEED_DIR}' is missing. "
            "Place one '<chief complaint>.txt' file per symptom there. "
            "See data/README.md."
        )

    txt_files = sorted(SEED_DIR.glob("*.txt"))
    if not txt_files:
        sys.exit(f"No .txt files found under '{SEED_DIR}'.")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    llm = ChatOpenAI(model="gpt-4.1", temperature=0.2, seed=42)
    prompt = PromptTemplate(
        template=generate_disease_list_0,
        input_variables=["symptom", "book_content"],
    )
    chain = prompt | llm

    all_results: dict = {}
    successful_count = 0
    failed_count = 0

    for file_path in txt_files:
        symptom = file_path.stem
        print(f"\nProcessing: {symptom}")
        log_step_start(SCRIPT_NAME, "generate_disease_list", f"symptom: {symptom}")

        try:
            book_content = file_path.read_text(encoding="utf-8")

            input_data = {"symptom": symptom, "book_content": book_content}
            formatted_prompt = prompt.format(**input_data)
            response = chain.invoke(input_data)
            response_text = response.content

            log_llm_interaction(
                SCRIPT_NAME,
                f"generate_disease_list - {symptom}",
                {"formatted_prompt": formatted_prompt, "input_data": input_data},
                response_text,
            )

            parsed_json = trimAndLoadJson(response_text)

            result_file = RESULTS_DIR / f"{symptom.replace(' ', '_')}_diseases.json"
            result_file.write_text(
                json.dumps(parsed_json, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            all_results[symptom] = parsed_json
            log_step_end(SCRIPT_NAME, f"generate_disease_list - {symptom}", True, str(result_file))
            successful_count += 1
            print(f"OK: {symptom} -> {result_file}")

        except Exception as exc:
            log_error(SCRIPT_NAME, f"generate_disease_list - {symptom}", str(exc))
            log_step_end(SCRIPT_NAME, f"generate_disease_list - {symptom}", False, str(exc))
            failed_count += 1
            print(f"FAIL: {symptom}: {exc}")

    consolidated = RESULTS_DIR / "all_diseases.json"
    consolidated.write_text(
        json.dumps(all_results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\nSummary:")
    print(f"  succeeded: {successful_count}")
    print(f"  failed:    {failed_count}")
    print(f"  output:    {consolidated}")


if __name__ == "__main__":
    main()
