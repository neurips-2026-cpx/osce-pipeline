"""End-to-end interactive demo of the OSCE simulated-patient system.

Usage (from repo root):
    python -m src.runtime.main [--lang ko|en] [--patient PATH]

Loads a patient JSON, runs an interactive history-taking session in the
terminal, and prints the auto-graded result on `exit`. The default patient
is the one shipped under ``data/samples/patient/example_patient.json``.
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

from src.grading import grade_session, parse_evaluated_checklist
from src.runtime.llm_engine import LLMEngine
from src.runtime.schemas import Message, PatientData

DEFAULT_PATIENT = Path("data/samples/patient/example_patient.json")


async def run(lang: str, patient_path: Path) -> None:
    with patient_path.open(encoding="utf-8") as f:
        patient = PatientData(**json.load(f))

    engine = LLMEngine(lang=lang)
    messages: list[Message] = []
    session_id = 1

    user_label = "학생 의사" if lang == "ko" else "Student doctor"
    exit_hint = "(exit 입력 시 종료)" if lang == "ko" else "(type 'exit' to finish)"
    print(f"=== OSCE simulation: {patient.disease} / {patient.chief_complaint} ===")
    print(exit_hint)

    while True:
        try:
            user_msg = input(f"\n{user_label}> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_msg:
            continue
        if user_msg.lower() == "exit":
            break

        messages.append(Message(sender_type="user", text=user_msg))
        print(f"{patient.name}: ", end="", flush=True)
        buf = ""
        async for ch in engine.chat_with_patient(session_id, user_msg, patient):
            sys.stdout.write(ch)
            sys.stdout.flush()
            buf += ch
        print()
        messages.append(Message(sender_type="patient", text=buf))

    if not messages:
        return

    print("\n=== Generating checklist & grading ===")
    raw_checklist = await engine.generate_checklist(patient)
    checklist_items = parse_evaluated_checklist(raw_checklist)
    result = await grade_session(engine, messages, checklist_items, patient)

    print(f"\nChecklist score    : {result.checklist_score:.1f}%")
    print(f"Relationship mean  : {result.relationship_mean:.2f} / 5")
    print(f"Total score        : {result.total_score:.1f} / 100")
    print(f"Grade              : {result.grade}")
    print("\n--- Feedback ---")
    print(result.feedback)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["ko", "en"], default="ko")
    parser.add_argument(
        "--patient",
        type=Path,
        default=DEFAULT_PATIENT,
        help="Path to a patient JSON. Defaults to the sample patient.",
    )
    args = parser.parse_args()
    asyncio.run(run(args.lang, args.patient))


if __name__ == "__main__":
    main()
