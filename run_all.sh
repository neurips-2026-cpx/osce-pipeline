#!/usr/bin/env bash
# OSCE data-generation pipeline.
# Reads data/seed/<chief complaint>.txt files and produces, in order:
#   data/seed/results/<symptom>_diseases.json   (stage 1)
#   data/seed/all_diseases.json                  (stage 2)
#   data/seed/all_disease_with_checklists.json   (stage 3)
#   data/seed/all_disease_with_scenarios.json    (stage 4, final)

set -euo pipefail

start_time=$(date)
echo "========================================="
echo "OSCE data generation pipeline"
echo "  started: $start_time"
echo "========================================="

run_stage() {
    local label="$1"
    local module="$2"
    shift 2
    echo
    echo "----- $label -----"
    python -m "$module" "$@"
}

run_stage "stage 1: synthesise patient cohorts"      src.pipeline.stage1_process_disease_list
run_stage "stage 2: merge per-symptom JSONs"         src.pipeline.stage2_merge_json
run_stage "stage 3: generate OSCE checklists"        src.pipeline.stage3_generate_checklist
run_stage "stage 4: scenario draft + polish"         src.pipeline.stage4_generate_scenario

end_time=$(date)
echo
echo "========================================="
echo "Pipeline complete."
echo "  started:  $start_time"
echo "  finished: $end_time"
echo "========================================="
echo
echo "Outputs:"
echo "  data/seed/results/                          per-symptom stage 1 JSONs"
echo "  data/seed/all_diseases.json                 stage 2 merged"
echo "  data/seed/all_disease_with_checklists.json  stage 3"
echo "  data/seed/all_disease_with_scenarios.json   stage 4 (final)"
echo "  logging.txt                                 run log"
