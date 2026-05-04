#!/usr/bin/env bash
# Interactive single-patient OSCE demo.
# Loads data/samples/patient/example_patient.json by default; pass --patient
# PATH to use a different patient JSON (with the same schema).
#
# Usage:
#   bash run_demo.sh                              # Korean (default)
#   bash run_demo.sh --lang en                    # English
#   bash run_demo.sh --patient mypatient.json     # custom patient

set -euo pipefail

python -m src.runtime.main "$@"
