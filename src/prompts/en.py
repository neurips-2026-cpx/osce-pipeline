"""English prompt templates.

Mirror of ``ko.py`` — same eight templates, identical placeholder variables
({symptom}, {disease}, {patient_name}, ...), so the same engine code works
in either language with no other changes.
"""

GENERATE_DISEASE_LIST = """Generate fictional patient information in JSON based on a chief complaint. Diseases must be drawn from the reference knowledge below. Generate exactly five patients.
Each patient entry must include:

symptom: the given chief complaint
disease: a major disease for that complaint, grounded in the reference knowledge
name: a plausible patient name (avoid generic placeholders like "John Doe" or "Jane Doe")
age: an age statistically appropriate for the disease
gender: a gender consistent with the disease's epidemiology

## Reference knowledge:
{book_content}

## Output format (JSON example):
```json
{{
  "symptom": "cough",
  "patients": [
    {{
      "disease": "Pneumonia",
      "name": "Robert Hayes",
      "age": 65,
      "gender": "male",
      "vital_sign": "BP: 130/85 mmHg\\nHR: 95 bpm\\nRR: 24/min\\nTemp: 38.3°C"
    }},
    {{
      "disease": "Acute bronchitis",
      "name": "Emily Chen",
      "age": 34,
      "gender": "female",
      "vital_sign": "BP: 118/76 mmHg\\nHR: 88 bpm\\nRR: 20/min\\nTemp: 37.8°C"
    }},
    {{
      "disease": "Common cold",
      "name": "Daniel Park",
      "age": 27,
      "gender": "male",
      "vital_sign": "BP: 120/80 mmHg\\nHR: 80 bpm\\nRR: 18/min\\nTemp: 37.5°C"
    }}
  ]
}}
```

## Patient information:
symptom: {symptom}

Answer:"""


CHECKLIST_PROMPT_TEMPLATE_DATAGEN = """We are building a question checklist that will serve as the OSCE (Objective Structured Clinical Examination) scoring rubric. The checklist must include the most important history-taking questions about the chief complaint, important questions about social history, past medical history, and family history, and patient education/instructions to deliver in the clinic.

## Patient information:
Name: {patient_name}
Age: {patient_age}
Sex: {sex}
Symptom: {symptom}
Disease: {disease}
Vital signs: {vital_sign}

### Reference knowledge:
{book_content}

Below is an example checklist actually used in a hematuria OSCE station. Following the same format, write at least 20 list-style questions that should be asked in the OSCE for a "{disease}" patient presenting with the chief complaint "{symptom}". Each question should ask about a single thing wherever possible. The checklist must include the questions that allow the examinee to arrive at "{disease}".
Return JSON.

### Example checklist:
{{
  "diseases": [
    {{
      "symptom": "blood in urine",
      "patients": [
        {{
          "interview_item": "Asked about the colour of the red urine, presence of blood clots, and timing (initial/terminal).",
          "purpose": "Characterise the haematuria; localise the lesion."
        }},
        {{
          "interview_item": "Asked whether the patient has had haematuria before or any prior abnormal urinalysis.",
          "purpose": "Recurrence and underlying disease."
        }},
        {{
          "interview_item": "Asked about precipitating factors such as exercise, fever, or infection.",
          "purpose": "Differentiate exertional/infectious haematuria."
        }},
        {{
          "interview_item": "Asked whether the patient had flank pain.",
          "purpose": "Differentiate urolithiasis or pyelonephritis."
        }},
        {{
          "interview_item": "Asked whether the patient had oedema.",
          "purpose": "Nephrotic syndrome or renal dysfunction."
        }},
        {{
          "interview_item": "Asked about at least one of skin rash or joint pain.",
          "purpose": "Screen for systemic disease such as vasculitis."
        }},
        {{
          "interview_item": "Asked whether urination was uncomfortable or painful.",
          "purpose": "Lower urinary tract infection such as cystitis."
        }},
        {{
          "interview_item": "Asked about at least two of frequency, residual urine, urgency, or nocturia.",
          "purpose": "Lower urinary tract irritative symptoms."
        }},
        {{
          "interview_item": "Asked whether there was foamy urine.",
          "purpose": "Concomitant proteinuria — suspect glomerular disease."
        }},
        {{
          "interview_item": "Asked about medications, especially aspirin and anticoagulants.",
          "purpose": "Drug-related bleeding."
        }},
        {{
          "interview_item": "Asked whether the patient has a history of urinary tract infection or kidney disease.",
          "purpose": "Underlying disease."
        }},
        {{
          "interview_item": "Asked whether the family has at least two of haematuria, kidney disease, or genitourinary cancer.",
          "purpose": "Differentiate hereditary disease."
        }},
        {{
          "interview_item": "Asked about both alcohol consumption and smoking.",
          "purpose": "Risk factors for bladder and renal cancer."
        }},
        {{
          "interview_item": "Took a sexual history including any recent unfamiliar partners.",
          "purpose": "Differentiate STI-related urinary infection."
        }},
        {{
          "interview_item": "(Male) Asked about weak urinary stream or straining.",
          "purpose": "Evaluate benign prostatic hyperplasia."
        }},
        {{
          "interview_item": "Explained possible causes such as glomerulonephritis or IgA nephropathy.",
          "purpose": "Share suspected diagnosis and educate."
        }},
        {{
          "interview_item": "Explained that a renal biopsy may be needed to identify the cause.",
          "purpose": "Explain the need for further work-up."
        }},
        {{
          "interview_item": "Explained that smoking may be related to haematuria and recommended cessation.",
          "purpose": "Health-maintenance counselling."
        }}
      ]
    }}
  ]
}}

{disease} checklist:"""


SCENARIO_PROMPT_TEMPLATE_1 = """We are building an OSCE scenario. The scenario must describe the chief complaint in detail and cover related symptoms, family history, social history, past medical history, and medication history. It must also let the patient answer every item on the checklist. Use the reference knowledge. Match the example format. Do not use markdown. When expressing date ranges, use ~ instead of -. Write in casual register. Length must be between 2,000 and 2,500 characters. Output the scenario directly with no preamble. Do not repeat the '## Checklist' or '## Patient information' headings inside the scenario.

## Checklist
{checklist}

## Reference knowledge
{book_content}

## Scenario example 1:

Robert Hayes is a 28-year-old male. Robert came to the hospital because of red urine that started 3 days ago. He had cold symptoms beginning 7 days ago, and the day before the red urine appeared he ran a fever up to 39 degrees with myalgia. The myalgia and fever peaked the evening 4 days ago, and the next morning, 3 days ago, he started seeing red urine. The colour was a deep reddish-brown that started very dark and gradually faded to a deep amber today. Robert has never been told he had haematuria, proteinuria, or kidney disease before. He is not taking any prescription drugs, herbal medicine, or supplements. He has been told that his blood pressure runs high, but he never thought it serious enough to see a doctor and does not remember the exact numbers. This is the first time his urine has looked unusual. There was no abdominal, flank, or distal urethral pain when passing the red urine. He thinks there may have been a small amount of foam in the urine, though he is not sure.

Otherwise he had no generalised weakness. There was no weight gain or loss. He had no headache. He was not dizzy. He had no fever today. He was not chilled or shivery. He had no muscle pain today. He had no night sweats. He had no cough. He had no sputum. He had no rhinorrhoea. He had no chest pain. He was not short of breath. He had no palpitations. He was not short of breath on exertion. He had no abdominal pain. His appetite was normal. He had no nausea. He did not vomit. He had no diarrhoea. He had no constipation. He had not vomited blood. His stool was not black. He had not passed bloody stool.

The first time he saw the haematuria, his cold symptoms had peaked the evening 4 days ago; he took an antipyretic, slept, and went to the bathroom in the morning, where he noticed the urine looked strange — a reddish-brown colour. He recalls buying Tylenol over the counter as the antipyretic. The next time he urinated he watched carefully from the start, and the urine was still deep red. He thought it was strange because there was no abdominal or pelvic pain when urinating. The day after that the colour was a slightly lighter red.

Robert has considered himself healthy and has essentially never been to a hospital. The check-ups he had during military service in his early twenties and at his workplace last year showed nothing unusual aside from slightly elevated blood pressure. He has smoked roughly one pack a day since military service. He drinks beer only at company gatherings, perhaps one or two glasses. He has worked an office job for the past 2 years and has annual workplace check-ups. He works out daily for an hour at the gym after work, but stopped going one week ago when the cold started. His diet leans towards meat and is on the salty side. He does not drink much water. Robert is an office worker who joined his current company 2 years ago. He typically works 9 to 6 and lives close by with his family. He has a girlfriend, has sex about once a week on average, and consistently uses a condom. He graduated from a four-year university and served in the military during his second year of college. He went straight to his current company after graduation. His father has high blood pressure and takes blood-pressure medication. He has one older brother; his mother and brother have no notable health issues.

Robert is worried about the red urine; he searched online, found the term "haematuria", and read that it can be associated with stones or cancer. He is anxious that he might have a serious illness. He wonders whether he can get tested today and see results, and whether admission or further work-up will be needed.

## Patient information
Name: {patient_name}
Age: {patient_age}
Sex: {sex}
Symptom: {symptom}
Disease: {disease}
Vital signs:\\n{vital_sign}

## {disease} scenario:"""


SCENARIO_PROMPT_TEMPLATE_2 = """I want to polish the following clinical scenario for an LLM-based simulated patient. Do not change content or order; rewrite the surface form to satisfy the rules below.

1) Every line must read naturally when spoken aloud.
2) Spell out numerals in words (e.g. 20 -> twenty, 30 -> thirty, "1 week" -> "one week", "2kg" -> "two kilograms", "5~6 times" -> "five or six times").
3) Each sentence must be a simple declarative, short enough to be spoken verbatim by the simulated patient.
4) Atomise sentences. For example, "The simulated patient was generally healthy and had not been diagnosed with any chronic disease or kidney disease" becomes "The simulated patient was generally healthy. He had not been told he has any chronic or kidney disease." Each sentence should be independent and concise, carrying only one or two facts.
5) Whenever a medication or specific event is mentioned, include both onset and duration.
6) Split into 4–5 paragraphs separated by blank lines: self-introduction / symptoms / medication and social history / other.
7) Replace medical jargon with lay terms where possible (e.g. "tonsil" -> "back of the throat", "impetigo" -> "skin pus") and keep wording natural when read aloud.
8) Output the rewritten scenario directly with no preamble.

Below is the scenario to revise. Rewrite it according to the rules above.

## Scenario to revise:
{scenario}

## Revised scenario:"""


CHECKLIST_PROMPT_TEMPLATE = """
You are designing a question checklist that will serve as the scoring rubric for an OSCE (Objective Structured Clinical Examination), Korea's standardized clinical-skills exam. The checklist must include the essential history-taking questions for the chief complaint, key questions covering social history, past medical history, and family history, as well as patient-education and counseling items the student should deliver in the consultation room.

Below is an example checklist actually used in the "hematuria" OSCE station. Following the same format, write a list of 20+ key questions that should be asked at the OSCE station for a "{disease}" patient who presents with the chief complaint "{symptom}". Each list item should ask only one thing. The checklist must include the questions necessary to reach a "{disease}" diagnosis.

### Example checklist:
```json
{{
  "diseases": [
    {{
      "symptom": "I have blood in my urine",
      "patients": [
        {{
          "question": "Asked about the color of the red urine, presence of clots, and timing (initial / terminal)",
          "purpose": "Characterize hematuria pattern; localize source",
          "order": 1
        }},
        {{
          "question": "Asked whether the patient has had hematuria before, or has ever been told of an abnormal urinalysis",
          "purpose": "Recurrence and underlying disease",
          "order": 2
        }},
        {{
          "question": "Asked about hematuria triggers such as exercise, fever, or infection",
          "purpose": "Differentiate exertional / infectious hematuria",
          "order": 3
        }},
        {{
          "question": "Asked about flank pain",
          "purpose": "Differentiate urolithiasis / pyelonephritis",
          "order": 4
        }},
        {{
          "question": "Asked about edema",
          "purpose": "Nephrotic syndrome / impaired renal function",
          "order": 5
        }},
        {{
          "question": "Asked about at least one of skin rash or joint pain",
          "purpose": "Differentiate systemic disease (e.g. vasculitis)",
          "order": 6
        }},
        {{
          "question": "Asked whether there was discomfort or pain on voiding",
          "purpose": "Lower urinary tract infection (e.g. cystitis)",
          "order": 7
        }},
        {{
          "question": "Asked about at least two of frequency, residual urine sensation, urgency, or nocturia",
          "purpose": "Lower urinary tract irritative symptoms",
          "order": 8
        }},
        {{
          "question": "Asked about foamy urine",
          "purpose": "Co-existing proteinuria — suspect glomerular disease",
          "order": 9
        }},
        {{
          "question": "Asked about medication use (especially aspirin, anticoagulants, etc.)",
          "purpose": "Identify drug-induced bleeding",
          "order": 10
        }},
        {{
          "question": "Asked about prior history of urinary tract infection or kidney disease",
          "purpose": "Underlying disease",
          "order": 11
        }},
        {{
          "question": "Asked about at least two of family history of hematuria, kidney disease, or urologic cancer",
          "purpose": "Differentiate hereditary disease",
          "order": 12
        }},
        {{
          "question": "Asked about both alcohol use and smoking",
          "purpose": "Risk factors for bladder and renal cancer",
          "order": 13
        }},
        {{
          "question": "Took a sexual history including recent intercourse with new partners",
          "purpose": "Differentiate STI-related urinary tract infection",
          "order": 14
        }},
        {{
          "question": "(Male) Asked about weak urinary stream or straining to void",
          "purpose": "Assess for benign prostatic hyperplasia",
          "order": 15
        }},
        {{
          "question": "Explained possible causes of hematuria such as glomerulonephritis or IgA nephropathy",
          "purpose": "Share differential and educate the patient",
          "order": 16
        }},
        {{
          "question": "Explained that a renal biopsy may be needed to identify the cause",
          "purpose": "Explain need for further testing",
          "order": 17
        }},
        {{
          "question": "Explained that smoking may be related to hematuria and recommended cessation",
          "purpose": "Health-behavior counseling",
          "order": 18
        }}
      ]
    }}
  ]
}}
```


Below are the patient information for the "{symptom}" station and the reference knowledge (excerpt from the OSCE textbook). Use the reference knowledge to construct an OSCE-grade checklist.

## Patient Information
Chief complaint: {symptom}
Patient name: {patient_name}
Age: {patient_age}
Sex: {sex}
Vital signs: {vital_sign}
Disease: {disease}

## Reference Knowledge
{book_content}

{disease} checklist JSON:
"""


CHATBOT_SYSTEM_PROMPT = """The block delimited by <patient_information></patient_information> contains the prior medical information for a simulated patient who is presenting with "{symptom}" as their chief complaint at an OSCE clinical-skills exam. You are now playing the role of the simulated patient, {patient_name}. Holding the prior medical information below, follow the <behavior_guidelines></behavior_guidelines> and <response_style></response_style> sections, and respond naturally to the student doctor's questions:

<patient_information>
{prompt}
</patient_information>

<behavior_guidelines>
- Answer the student doctor's questions concisely, in 25 words or fewer.
- Do not volunteer information from the prior medical information that the student has not asked about.
- Never reveal the diagnosis to the student doctor. If the student asks for the diagnosis name, reply "I'm not sure."
- Express your symptoms in everyday lay language. (For example, instead of "dyspnea, chest pain", say "I'm short of breath and my chest hurts.")
- Avoid giving exact numerical values; give approximate values in colloquial form.
- If the student doctor uses technical terms a layperson would not understand, you may ask "What does that mean?"
- Never volunteer medical reasoning or a diagnosis on your own initiative.
- Begin every response with the prefix "Simulated patient {patient_name}: ".
</behavior_guidelines>

<response_style>
- Use everyday expressions instead of technical medical terms or precise numbers.
- Do not answer questions that were not asked, and do not volunteer prior information.
- Use a natural, conversational tone.
</response_style>"""


GRADING_CHECKLIST_ASSISTANT_PROMPT = """
The markdown-formatted dialogue below is a conversation between a student doctor and a {disease} patient '{patient_name}' at an OSCE clinical-skills exam.

<conversation>
{conversation}
</conversation>

<checklist>
{checklist_json}
</checklist>


The checklist above is the OSCE scoring rubric for taking a history from a patient presenting with {disease}. Based on this rubric, decide whether the student doctor asked each of the listed key questions.
Mark 1 if asked and 0 if not asked, and return the result as JSON. Each judgment must be based on the dialogue between the student doctor and patient {patient_name}.
Even if the conversation is very short or unusual, you must still respond in valid JSON.

### Example checklist evaluation:
```json
{{
  "diseases": [
    {{
      "symptom": "I have blood in my urine",
      "patients": [
        {{
          "question": "Asked about the color of the red urine, presence of clots, and timing (initial / terminal)",
          "purpose": "Characterize hematuria pattern; localize source",
          "order": 1,
          "asked": 1
        }},
        {{
          "question": "Asked whether the patient has had hematuria before, or has ever been told of an abnormal urinalysis",
          "purpose": "Recurrence and underlying disease",
          "order": 2,
          "asked": 0
        }}
      ]
    }}
  ]
}}
```

Checklist evaluation:
"""


GRADING_SCORE_ASSISTANT_PROMPT = """
For the dialogue between the student doctor and "patient {patient_name}", score the following patient-doctor relationship items.
Each item is scored on a 1-5 scale. State which parts of the student doctor's questions you used as evidence for the score.
Your evaluation must be grounded in the dialogue between the student doctor and patient {patient_name}.
Even if the conversation is very short or unusual, you must still respond in valid JSON.

<conversation>
{conversation}
</conversation>

1. The student doctor questioned "patient {patient_name}" efficiently — using open-ended questions, mid-conversation summaries, and confirmation of answers.
2. The student doctor listened well to "patient {patient_name}" — using verbal acknowledgments and an attentive tone.
3. The student doctor tried to understand "patient {patient_name}'s" perspective — using empathic statements and questions about the patient's current situation.
4. The student doctor explained things in a way that was easy for "patient {patient_name}" to understand — using clear concise explanations, opportunities for questions, and simple word choice.
5. The student doctor tried to build rapport with "patient {patient_name}" — using greetings, self-introduction, polite register, and a respectful tone.

```json
{{
 "patient_doctor_relationship_evaluation": {{
   "1_efficient_questioning": {{
     "reason": "The student doctor relied mostly on closed-ended questions. Yes/no questions such as 'Do you have a fever?' and 'Are you coughing?' dominated, while open-ended questions like 'Could you describe your symptoms in more detail?' were rare. There were also no mid-conversation summaries or confirmations, so information gathering was inefficient.",
     "score": 2
   }},
   "2_active_listening": {{
     "reason": "The student doctor barely listened to the patient. When the patient said 'Since yesterday my throat has hurt and I've had a fever,' the student moved to the next question without even a minimal acknowledgment such as 'I see' or 'Got it.' There was no response to the patient's emotions or concerns, indicating very poor listening.",
     "score": 1
   }},
   "3_empathy_and_understanding": {{
     "reason": "The student doctor showed some understanding and empathy for the patient's situation, using empathic phrases like 'That must have been uncomfortable' and 'Is it interfering with your daily life?', and made an effort to grasp the patient's current state. However, deeper emotional support and a concrete response to the patient's worries were lacking.",
     "score": 4
   }},
   "4_clear_explanation": {{
     "reason": "The student doctor gave very clear, easy-to-understand explanations. They used everyday language rather than jargon — for example, 'It looks like a common cold; rest and fluids are important' — and offered the patient an opportunity to ask questions: 'Do you have anything you'd like to ask?' Medication instructions were given concretely and clearly, e.g. 'Three times a day, 30 minutes after meals.'",
     "score": 5
   }},
   "5_rapport_building": {{
     "reason": "The student doctor was basically polite but did not actively work to build rapport. They said 'Hello' but did not introduce themselves; they used the formal register but did not address the patient by name or use any warmer phrasing to build closeness. The conversation felt somewhat businesslike and distant.",
     "score": 3
   }}
 }}
}}
```

Patient-doctor relationship evaluation JSON:
"""


GRADING_FEEDBACK_ASSISTANT_PROMPT = """
Now write feedback to the student doctor based on the rubric. Below is the OSCE dialogue the student doctor produced.

<conversation>
{conversation}
</conversation>

First, check whether the dialogue is too short. If it is shorter than 10 sentences and you judge the exam was not properly performed, add the line "The exam could not be properly evaluated due to too few questions."
If the student gave a proper greeting, took an appropriate symptom-focused history, and explained things to the patient, write the student-facing feedback. Avoid quoting the exact wording of the checklist. Below are the general goals the student doctor should achieve at a {disease} OSCE station.

<learning outcomes>
1. Can ask the questions needed to differentiate the underlying causes of {symptom}.
2. Can infer the pathophysiologic factors from the pattern of {symptom}.
3. Can perform the systematic history-taking — including family history, social history, and past medical history — needed to differentiate the diagnosis of {disease}.
4. Can reason from the history to a working differential including the leading diagnosis, and explain the working diagnosis and the patient's condition in terms the patient can understand.
5. Can select the appropriate tests, and explain the diagnostic plan, treatment plan, and necessary lifestyle education in terms the patient can understand.
</learning outcomes>

Write the feedback in the following three sections:

### History-taking performance
Briefly note whether the student covered the key checklist items. If most items were asked, give credit; if there are gaps, mention 1-2 categories indirectly (for example: if the student did not ask about smoking, write "Social history was not adequately taken"; if the student did not ask about pain severity, write "Pain severity was not asked"). Keep it to a few targeted points.

### Patient-doctor relationship
Focus on the lowest-scoring relationship dimensions. Briefly explain — with one or two examples from the questions — where the student fell short.

### Overall assessment and improvement points
Comment on the total number of questions (around 30-40 sentences is appropriate given the checklist length; over 50 may be too many), the positives (e.g. covering most of the checklist, asking good relationship-building questions), and the negatives. If the working diagnosis was wrong, phrase it as e.g. "There were issues in reasoning toward the simulated patient's diagnosis." Do not reveal the actual diagnosis. Avoid generic closing lines such as "If you continue to develop your explanatory skills and clinical reasoning you will grow into an excellent clinician" — focus only on the evaluation of this particular OSCE case.

Write the feedback in OSCE-evaluation format, within 350 words total.

Feedback:
"""
