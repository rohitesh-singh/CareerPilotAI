import pdfplumber
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

pdf_path = "/Users/rohitesh/Desktop/Rohitesh_Resume_03.pdf"

resume_text = ""

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            resume_text += text + "\n"

prompt = f"""
You are an expert recruiter, ATS reviewer and hiring manager.

Analyze the resume and return ONLY valid JSON.

Return this exact structure:

{{
  "name": "",
  "years_experience": 0,
  "current_role": "",
  "roles": [],
  "skills": [],
  "tools": [],
  "domains": [],
  "methodologies": [],
  "program_types": [],
  "stakeholder_types": [],
  "leadership_experience": [],
  "certifications": [],
  "strengths": [],
  "career_summary": ""
}}

Instructions:

- Return ONLY JSON.
- No markdown.
- No explanation.
- Infer years of experience if possible.
- Extract all relevant skills.
- Extract transferable skills.
- Extract leadership responsibilities.
- Extract stakeholder management experience.
- Extract program management experience.
- Extract technical skills.
- Extract business skills.
- Keep career_summary under 100 words.

Resume:

{resume_text}
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

print(response.choices[0].message.content)