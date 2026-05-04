"""Optional utility: export the per-patient OSCE checklists from
``all_disease_with_checklists.json`` to one ``.xlsx`` file per patient.

Output layout: ``data/seed/checklist_excel/<symptom>/<disease>_<age>.xlsx``.
"""

import json
import re
from pathlib import Path

import pandas as pd


def sanitize_filename(filename):
    """Replace path-illegal characters and runs of whitespace so the string is
    usable as a filename on Windows and macOS."""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'\s+', '_', filename)
    return filename.strip()


def create_excel_from_checklist(checklist_data, output_path):
    """Write a single patient's checklist to an ``.xlsx`` file."""
    items = []

    if isinstance(checklist_data, list) and len(checklist_data) > 0:
        first_item = checklist_data[0]
        if 'patients' in first_item and isinstance(first_item['patients'], list):
            for item in first_item['patients']:
                if isinstance(item, dict) and 'interview_item' in item:
                    items.append({
                        'Interview item': item.get('interview_item', ''),
                        'Purpose': item.get('purpose', ''),
                    })

    if items:
        df = pd.DataFrame(items)
        df.index = df.index + 1  # 1-based index
        df.to_excel(output_path, index=True, index_label='No.')
        print(f"Wrote {output_path}")
    else:
        print(f"No checklist data for {output_path}")


def main():
    input_path = Path('data/seed/all_disease_with_checklists.json')
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    base_output_dir = Path('data/seed/checklist_excel')
    base_output_dir.mkdir(parents=True, exist_ok=True)

    diseases_data = data['diseases']
    print(f"Processing {len(diseases_data)} symptoms...")

    for symptom_data in diseases_data:
        symptom = symptom_data['symptom']
        patients = symptom_data['patients']

        symptom_folder = base_output_dir / sanitize_filename(symptom)
        symptom_folder.mkdir(exist_ok=True)

        print(f"\nSymptom: {symptom} ({len(patients)} patients)")

        for patient in patients:
            disease = patient['disease']
            age = patient['age']

            filename = f"{sanitize_filename(disease)}_{age}.xlsx"
            output_path = symptom_folder / filename

            if 'checklist' in patient and 'diseases' in patient['checklist']:
                checklist_data = patient['checklist']['diseases']
                create_excel_from_checklist(checklist_data, output_path)
            else:
                print(f"No checklist for {disease} (age {age})")


if __name__ == "__main__":
    main()
