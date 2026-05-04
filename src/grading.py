"""
Two-stage grading pipeline for an OSCE simulated-patient session.

Stage 1: per-checklist-item binary scoring (asked / not asked).
Stage 2: 5 patient-doctor relationship metrics, each scored 1-5.
Final score = ((checklist_sum + relationship_sum) / (n_items + 5)) * 100.
"""
import json
from typing import Iterable

from src.runtime.llm_engine import LLMEngine
from src.runtime.schemas import (
    ChecklistItem,
    GradingResult,
    Message,
    PatientData,
    RelationshipScore,
)


def calculate_grade(total_score: float) -> str:
    if total_score >= 80:
        return "A"
    if total_score >= 70:
        return "B"
    if total_score >= 60:
        return "C"
    if total_score >= 50:
        return "D"
    return "F"


def format_conversation(messages: Iterable[Message], lang: str = "ko") -> str:
    user_label = "학생 의사" if lang == "ko" else "Student doctor"
    lines: list[str] = []
    for msg in messages:
        if msg.sender_type == "user":
            lines.append(f"{user_label}: {msg.text}")
        else:
            lines.append(msg.text)
    return "\n".join(lines)


def checklist_to_json(items: list[ChecklistItem], symptom: str) -> str:
    payload = {
        "diseases": [{
            "symptom": symptom,
            "patients": [
                {"question": it.question, "purpose": it.purpose, "order": it.order}
                for it in items
            ],
        }]
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def parse_evaluated_checklist(evaluation: dict) -> list[ChecklistItem]:
    items: list[ChecklistItem] = []
    for disease in evaluation.get("diseases", []):
        for entry in disease.get("patients", []):
            items.append(ChecklistItem(
                question=entry.get("question", ""),
                purpose=entry.get("purpose", ""),
                order=entry.get("order", 0),
                asked=entry.get("asked", 0),
            ))
    return items


def parse_relationship_scores(evaluation: dict) -> list[RelationshipScore]:
    metrics = evaluation.get("patient_doctor_relationship_evaluation", {})
    return [
        RelationshipScore(metric_id=mid, score=info.get("score", 0), reason=info.get("reason", ""))
        for mid, info in metrics.items()
    ]


async def grade_session(
    engine: LLMEngine,
    messages: list[Message],
    checklist: list[ChecklistItem],
    patient: PatientData,
) -> GradingResult:
    conversation = format_conversation(messages, lang=engine.lang)
    checklist_json = checklist_to_json(checklist, patient.chief_complaint)

    checklist_eval = await engine.evaluate_checklist(
        conversation, checklist_json, patient.disease, patient.name
    )
    relationship_eval = await engine.evaluate_relationship(conversation, patient.name)
    feedback = await engine.generate_feedback(
        conversation, patient.disease, patient.chief_complaint
    )

    scored_items = parse_evaluated_checklist(checklist_eval)
    scored_relations = parse_relationship_scores(relationship_eval)

    n_items = max(len(scored_items), 1)
    n_relations = max(len(scored_relations), 1)
    checklist_sum = sum(it.asked or 0 for it in scored_items)
    relationship_sum = sum(r.score for r in scored_relations)

    checklist_score = checklist_sum / n_items * 100.0
    relationship_mean = relationship_sum / n_relations
    total_score = (checklist_sum + relationship_sum) / (n_items + n_relations) * 100.0

    return GradingResult(
        checklist_items=scored_items,
        relationship_scores=scored_relations,
        checklist_score=checklist_score,
        relationship_mean=relationship_mean,
        total_score=total_score,
        grade=calculate_grade(total_score),
        feedback=feedback,
    )
