from typing import Literal, Optional
from pydantic import BaseModel


class PatientData(BaseModel):
    name: str
    age: int
    gender: str
    chief_complaint: str
    disease: str
    vital_sign: str = ""
    prompt: str = ""


class Message(BaseModel):
    sender_type: Literal["user", "patient"]
    text: str


class ChecklistItem(BaseModel):
    question: str
    purpose: str
    order: int
    asked: Optional[int] = None


class RelationshipScore(BaseModel):
    metric_id: str
    score: int
    reason: str


class GradingResult(BaseModel):
    checklist_items: list[ChecklistItem]
    relationship_scores: list[RelationshipScore]
    checklist_score: float
    relationship_mean: float
    total_score: float
    grade: str
    feedback: str
