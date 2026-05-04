"""Stage 4: Two-step scenario generation (draft + polish) for each patient.

Reads ``data/seed/all_disease_with_checklists.json``, then for each patient:
  1. Generates a 2,000–2,500-character draft scenario grounded in the
     checklist and the per-symptom textbook chapter (``generate_scenario_2``).
  2. Polishes the draft to read naturally aloud for a standardized-patient
     simulator: spells out numerals, simplifies jargon, breaks into 4–5
     paragraphs (``generate_scenario_3``).

The polished string is attached to each patient under the ``prompt`` field, and
the result is written to ``data/seed/all_disease_with_scenarios.json``.

Patients are processed in async batches; ``--batch-size`` controls fan-out.
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from src.prompts import (
    generate_scenario_2,
    generate_scenario_2_en,
    generate_scenario_3,
    generate_scenario_3_en,
)

# Language switch: ``OSCE_LANG=en`` selects English prompts; default is Korean.
if os.getenv("OSCE_LANG") == "en":
    generate_scenario_2 = generate_scenario_2_en
    generate_scenario_3 = generate_scenario_3_en
from src.utils import checklist_to_markdown
from src.logging_utils import (
    setup_logging,
    log_llm_interaction,
    log_error,
    log_step_start,
    log_step_end,
)


SCRIPT_NAME = "stage4_generate_scenario.py"
SEED_DIR = Path("data/seed")
INPUT_FILE = SEED_DIR / "all_disease_with_checklists.json"
OUTPUT_FILE = SEED_DIR / "all_disease_with_scenarios.json"


def load_book_content(symptom: str) -> str:
    file_path = SEED_DIR / f"{symptom}.txt"
    if not file_path.exists():
        return f"Reference textbook content for '{symptom}' was not found."
    return file_path.read_text(encoding="utf-8")


async def generate_draft(chain, template, patient, checklist_md, book_content):
    input_data = {
        "patient_name": patient.get("name", ""),
        "patient_age": patient.get("age", ""),
        "sex": patient.get("gender", ""),
        "symptom": patient.get("symptom", ""),
        "disease": patient.get("disease", ""),
        "vital_sign": patient.get("vital_sign", ""),
        "checklist": checklist_md,
        "book_content": book_content,
    }
    formatted_prompt = template.format(**input_data)
    response = await chain.ainvoke(input_data)
    log_llm_interaction(
        SCRIPT_NAME,
        f"scenario_draft - {patient.get('symptom')} - {patient.get('disease')}",
        {"formatted_prompt": formatted_prompt, "input_data": input_data},
        response,
    )
    return response.content


async def polish_scenario(chain, template, patient, draft):
    input_data = {"scenario": draft}
    formatted_prompt = template.format(**input_data)
    response = await chain.ainvoke(input_data)
    log_llm_interaction(
        SCRIPT_NAME,
        f"scenario_polish - {patient.get('symptom')} - {patient.get('disease')}",
        {"formatted_prompt": formatted_prompt, "input_data": input_data},
        response,
    )
    return response.content


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


async def process_batches(draft_chain, polish_chain, draft_tpl, polish_tpl, patients_data, book_content, batch_size):
    """Run draft and polish stages concurrently in batches of ``batch_size``."""
    results = []
    n_batches = (len(patients_data) + batch_size - 1) // batch_size

    for batch_idx, batch in enumerate(chunks(patients_data, batch_size)):
        print(f"  batch {batch_idx + 1}/{n_batches} ({len(batch)} patients)")

        draft_results = await asyncio.gather(
            *[generate_draft(draft_chain, draft_tpl, p, c, book_content) for p, c in batch],
            return_exceptions=True,
        )

        polish_tasks = []
        for (patient, _), draft in zip(batch, draft_results):
            if isinstance(draft, Exception):
                polish_tasks.append(asyncio.create_task(asyncio.sleep(0)))
            else:
                polish_tasks.append(polish_scenario(polish_chain, polish_tpl, patient, draft))

        polish_results = await asyncio.gather(*polish_tasks, return_exceptions=True)

        for (patient, _), draft, polished in zip(batch, draft_results, polish_results):
            if isinstance(draft, Exception):
                results.append((patient, draft))
            elif isinstance(polished, Exception):
                results.append((patient, polished))
            else:
                results.append((patient, polished))
                print(f"    OK: {patient.get('disease')} ({patient.get('name')})")

    return results


async def main() -> None:
    parser = argparse.ArgumentParser(description="Generate OSCE patient scenarios.")
    parser.add_argument("--symptom-limit", type=int, default=None, help="Cap on number of symptoms.")
    parser.add_argument("--disease-limit", type=int, default=None, help="Cap on patients per symptom.")
    parser.add_argument("--batch-size", type=int, default=5, help="Concurrency per batch.")
    args = parser.parse_args()

    setup_logging()
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is not set. Copy .env.example to .env and fill it in.")

    if not INPUT_FILE.exists():
        sys.exit(f"'{INPUT_FILE}' is missing. Run stages 1-3 first.")

    data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    if "diseases" not in data:
        sys.exit(f"'{INPUT_FILE}' has unexpected shape; expected key 'diseases'.")
    all_diseases = data["diseases"]

    if args.symptom_limit:
        all_diseases = all_diseases[: args.symptom_limit]
        print(f"symptom-limit applied: {args.symptom_limit}")

    draft_tpl = PromptTemplate.from_template(generate_scenario_2)
    polish_tpl = PromptTemplate.from_template(generate_scenario_3)
    llm = ChatOpenAI(model="gpt-4.1", temperature=0.2, seed=42)
    draft_chain = draft_tpl | llm
    polish_chain = polish_tpl | llm

    output = {"diseases": []}

    for symptom_idx, symptom_data in enumerate(all_diseases):
        symptom = symptom_data.get("symptom", "")
        print(f"\nSymptom {symptom_idx + 1}/{len(all_diseases)}: {symptom}")
        log_step_start(SCRIPT_NAME, "generate_scenario", f"symptom: {symptom}")

        book_content = load_book_content(symptom)
        patients = symptom_data.get("patients", [])
        if args.disease_limit:
            patients = patients[: args.disease_limit]

        prepared = []
        for patient in patients:
            patient["symptom"] = symptom
            checklist_items = []
            checklist = patient.get("checklist", {})
            for disease_block in checklist.get("diseases", []):
                checklist_items.extend(disease_block.get("patients", []))
            checklist_md = checklist_to_markdown(checklist_items)
            prepared.append((patient, checklist_md))

        new_symptom_data = {"symptom": symptom, "patients": []}

        try:
            results = await process_batches(
                draft_chain, polish_chain, draft_tpl, polish_tpl,
                prepared, book_content, args.batch_size,
            )
            for patient, scenario in results:
                if isinstance(scenario, Exception):
                    log_error(SCRIPT_NAME, f"scenario - {patient.get('disease')}", str(scenario))
                    new_symptom_data["patients"].append(patient)
                else:
                    enriched = {**patient, "prompt": scenario}
                    new_symptom_data["patients"].append(enriched)
                    log_step_end(SCRIPT_NAME, f"scenario - {patient.get('disease')}", True, "")
        except Exception as exc:
            log_error(SCRIPT_NAME, f"batch - {symptom}", str(exc))
            for patient, _ in prepared:
                new_symptom_data["patients"].append(patient)

        output["diseases"].append(new_symptom_data)
        log_step_end(SCRIPT_NAME, f"symptom - {symptom}", True, f"{len(new_symptom_data['patients'])} patients")

    OUTPUT_FILE.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    total_patients = sum(len(s["patients"]) for s in output["diseases"])
    print(f"\nDone. Output: {OUTPUT_FILE}")
    print(f"  symptoms: {len(output['diseases'])}")
    print(f"  patients: {total_patients}")


if __name__ == "__main__":
    asyncio.run(main())
