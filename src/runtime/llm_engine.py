"""LLM engine for the OSCE simulated-patient system.

Six methods, all backed by gpt-4o:

1. ``chat_with_patient``         — streaming, conversational simulated patient.
2. ``generate_checklist``        — produce a fresh OSCE checklist for a patient.
3. ``generate_scenario``         — produce + polish a 2,000-character scenario.
4. ``evaluate_checklist``        — grade which rubric items the student asked.
5. ``evaluate_relationship``     — score the five 1-5 relationship dimensions.
6. ``generate_feedback``         — write an OSCE-evaluation-format report.

Dependencies: langchain-openai>=1.2, langchain-core, pydantic, python-dotenv.
Environment:  OPENAI_API_KEY (loaded via .env).
"""
import json
import re
from typing import Any, AsyncGenerator

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from src.prompts import get_prompts
from src.runtime.schemas import PatientData


class LLMEngine:
    def __init__(self, model: str = "gpt-4o", lang: str = "ko", seed: int | None = 42):
        load_dotenv()
        self.P = get_prompts(lang)
        self.lang = lang
        # Deterministic LLM for structured tasks (checklist, scenario, grading).
        self.llm = ChatOpenAI(model=model, temperature=0, seed=seed)
        # Conversational LLM for the simulated-patient chat (some variation
        # is desirable so the patient does not give identical replies).
        self.streaming_llm = ChatOpenAI(
            model=model, temperature=0.5, streaming=True, seed=seed,
        )
        # Per-session conversation history, keyed by session_id.
        # Each entry is a list of {"role": "user"|"assistant", "content": str}.
        self.memories: dict[int, list[dict[str, str]]] = {}

    def _history(self, session_id: int) -> list[dict[str, str]]:
        if session_id not in self.memories:
            self.memories[session_id] = []
        return self.memories[session_id]

    @staticmethod
    def _parse_json(text: str) -> dict[str, Any]:
        m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        body = m.group(1) if m else text.strip()
        body = body.strip().lstrip("```").lstrip("json").rstrip("```").strip()
        return json.loads(body)

    async def chat_with_patient(
        self,
        session_id: int,
        user_message: str,
        patient: PatientData,
    ) -> AsyncGenerator[str, None]:
        system_prompt = self.P.CHATBOT_SYSTEM_PROMPT.format(
            symptom=patient.chief_complaint,
            prompt=patient.prompt,
            patient_name=patient.name,
        )
        history = self._history(session_id)
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "Student doctor: {question}" if self.lang == "en" else "학생 의사: {question}"),
        ])
        chain = (
            RunnablePassthrough.assign(chat_history=lambda _: list(history))
            | prompt
            | self.streaming_llm
        )

        full = ""
        async for chunk in chain.astream({"question": user_message}):
            content = getattr(chunk, "content", "") or ""
            full += content
            yield content

        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": full})

    async def generate_checklist(self, patient: PatientData, book_content: str = "") -> dict:
        chain = PromptTemplate.from_template(self.P.CHECKLIST_PROMPT_TEMPLATE) | self.llm
        response = await chain.ainvoke({
            "symptom": patient.chief_complaint,
            "patient_name": patient.name,
            "patient_age": patient.age,
            "sex": patient.gender,
            "vital_sign": patient.vital_sign,
            "disease": patient.disease,
            "book_content": book_content,
        })
        return self._parse_json(response.content)

    async def generate_scenario(
        self,
        patient: PatientData,
        checklist: dict,
        book_content: str = "",
    ) -> str:
        checklist_md = self._checklist_to_markdown(checklist)
        chain1 = PromptTemplate.from_template(self.P.SCENARIO_PROMPT_TEMPLATE_1) | self.llm
        chain2 = PromptTemplate.from_template(self.P.SCENARIO_PROMPT_TEMPLATE_2) | self.llm

        draft = await chain1.ainvoke({
            "patient_name": patient.name,
            "patient_age": patient.age,
            "sex": patient.gender,
            "symptom": patient.chief_complaint,
            "disease": patient.disease,
            "vital_sign": patient.vital_sign,
            "checklist": checklist_md,
            "book_content": book_content,
        })
        polished = await chain2.ainvoke({"scenario": draft.content})
        return polished.content

    async def evaluate_checklist(
        self, conversation: str, checklist_json: str, disease: str, patient_name: str
    ) -> dict:
        chain = PromptTemplate.from_template(self.P.GRADING_CHECKLIST_ASSISTANT_PROMPT) | self.llm
        response = await chain.ainvoke({
            "conversation": conversation,
            "checklist_json": checklist_json,
            "disease": disease,
            "patient_name": patient_name,
        })
        return self._parse_json(response.content)

    async def evaluate_relationship(self, conversation: str, patient_name: str) -> dict:
        chain = PromptTemplate.from_template(self.P.GRADING_SCORE_ASSISTANT_PROMPT) | self.llm
        response = await chain.ainvoke({
            "conversation": conversation,
            "patient_name": patient_name,
        })
        return self._parse_json(response.content)

    async def generate_feedback(self, conversation: str, disease: str, symptom: str) -> str:
        chain = PromptTemplate.from_template(self.P.GRADING_FEEDBACK_ASSISTANT_PROMPT) | self.llm
        response = await chain.ainvoke({
            "conversation": conversation,
            "disease": disease,
            "symptom": symptom,
        })
        return response.content

    @staticmethod
    def _checklist_to_markdown(checklist: dict) -> str:
        lines: list[str] = []
        for disease in checklist.get("diseases", []):
            if "symptom" in disease:
                lines.append(f"## {disease['symptom']}")
            for i, item in enumerate(disease.get("patients", []), 1):
                lines.append(f"{i}. {item.get('question', '')}")
                if item.get("purpose"):
                    lines.append(f"   - purpose: {item['purpose']}")
        return "\n".join(lines)
