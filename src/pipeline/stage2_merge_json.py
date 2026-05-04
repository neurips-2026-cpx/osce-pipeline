"""Stage 2: Merge per-symptom JSON files into one consolidated dataset.

Reads ``data/seed/results/*_diseases.json`` (output of stage 1) and writes the
union as ``data/seed/all_diseases.json`` with shape ``{"diseases": [...]}``,
which is the input contract expected by stage 3.
"""

import json
import sys
from pathlib import Path

from src.logging_utils import setup_logging, log_step_start, log_step_end


SCRIPT_NAME = "stage2_merge_json.py"
SEED_DIR = Path("data/seed")
RESULTS_DIR = SEED_DIR / "results"
OUTPUT_FILE = SEED_DIR / "all_diseases.json"


def main() -> None:
    setup_logging()
    log_step_start(SCRIPT_NAME, "merge_json", f"merging {RESULTS_DIR}/*_diseases.json")

    if not RESULTS_DIR.exists():
        sys.exit(f"'{RESULTS_DIR}' is missing. Run stage 1 first.")

    json_files = [
        p for p in sorted(RESULTS_DIR.glob("*_diseases.json"))
        if p.name != "all_diseases.json"
    ]
    if not json_files:
        sys.exit(f"No '*_diseases.json' files found under '{RESULTS_DIR}'.")

    diseases = []
    for file_path in json_files:
        data = json.loads(file_path.read_text(encoding="utf-8"))
        diseases.append({"symptom": data["symptom"], "patients": data["patients"]})

    OUTPUT_FILE.write_text(
        json.dumps({"diseases": diseases}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Merged {len(json_files)} files -> {OUTPUT_FILE}")
    log_step_end(SCRIPT_NAME, "merge_json", True, f"{len(json_files)} files merged into {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
