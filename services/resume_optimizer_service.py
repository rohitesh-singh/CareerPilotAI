import json
import re

from services.groq_service import get_groq_client


def analyze_resume(
    resume_text,
    job_description
):

    client = get_groq_client()

    prompt = f"""
You are a resume optimization engine.

Analyze the resume against the job description.

Return ONLY valid JSON.

Do NOT use markdown.
Do NOT use ```json.
Do NOT provide explanations.

Return exactly in this format:

{{
  "match_score": 0,
  "strengths": [],
  "missing_keywords": [],
  "ats_recommendations": [],
  "interview_probability": ""
}}

Resume:

{resume_text}

Job Description:

{job_description}
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

    content = response.choices[0].message.content

    print("\n========== GROQ RESPONSE ==========\n")
    print(content)
    print("\n===================================\n")

    content = re.sub(
        r"```json|```",
        "",
        content
    ).strip()

    try:
        return json.loads(content)

    except Exception:

        return {
            "match_score": 0,
            "strengths": [],
            "missing_keywords": [],
            "ats_recommendations": [
                "Unable to parse model response"
            ],
            "interview_probability": "Unknown",
            "raw_response": content
        }