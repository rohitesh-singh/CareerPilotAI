import os
import json
import pdfplumber

from dotenv import load_dotenv
from groq import Groq
from supabase import create_client

# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()

# ==========================================
# SUPABASE CLIENT
# ==========================================

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# ==========================================
# GROQ CLIENT
# ==========================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ==========================================
# READ RESUME PDF
# ==========================================

pdf_path = "/Users/rohitesh/Desktop/Rohitesh_Resume_03.pdf"

resume_text = ""

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            resume_text += text + "\n"

# ==========================================
# READ JOB DESCRIPTION
# ==========================================

with open("job_description.txt", "r", encoding="utf-8") as f:
    job_description = f.read()

# ==========================================
# PROMPT
# ==========================================

prompt = f"""
You are an expert recruiter, ATS reviewer, hiring manager,
career coach and resume writer.

Analyze the candidate resume against the job description.

Return ONLY valid JSON.

Format:

{{
  "match_score": 0,

  "strengths": [],

  "missing_keywords": [],

  "keyword_explanations": [
    {{
      "keyword": "",
      "why_important": "",
      "where_to_add": ""
    }}
  ],

  "summary_rewrite": "",

  "bullet_improvements": [
    {{
      "current": "",
      "suggested": ""
    }}
  ],

  "ats_recommendations": [],

  "interview_questions": [],

  "interview_probability": "",

  "apply_recommendation": ""
}}

Rules:

1. Do NOT invent experience.
2. Rewrite existing experience only.
3. Suggest ATS-friendly keywords.
4. Explain WHY every missing keyword matters.
5. Explain WHERE the keyword should be added.
6. Focus on Program Manager, Technical Program Manager, PMO Manager, Delivery Manager and Scrum Master roles.
7. Suggest realistic improvements.
8. Generate interview questions based on the job description.
9. Never use:
   - Results-driven
   - Dynamic
   - Proven track record
   - Seasoned
   - Highly motivated
   - Strategic thinker

10. Write recommendations like an experienced recruiter reviewing a real candidate's resume.
11. Prioritize clarity and credibility over marketing language.
12. Return ONLY JSON.
13. No markdown.

Resume:

{resume_text}

Job Description:

{job_description}
"""

# ==========================================
# CALL GROQ
# ==========================================

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2
)

# ==========================================
# PARSE JSON RESPONSE
# ==========================================

content = response.choices[0].message.content

try:
    analysis = json.loads(content)

except Exception as e:
    print("\nERROR PARSING JSON:\n")
    print(content)
    raise e

# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n")
print("=" * 60)
print("RESUME OPTIMIZATION REPORT")
print("=" * 60)
print("\n")

print(json.dumps(
    analysis,
    indent=2
))

# ==========================================
# SAVE TO SUPABASE
# ==========================================

try:

    supabase.table("job_analyses").insert({
        "company": "Unknown",
        "role": "Unknown",
        "match_score": analysis.get("match_score", 0),
        "analysis": analysis
    }).execute()

    print("\n✅ Analysis saved successfully!")

except Exception as e:

    print("\n❌ Failed to save analysis:")
    print(e)