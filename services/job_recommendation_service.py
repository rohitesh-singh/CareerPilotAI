import json

from services.groq_service import get_groq_client


def recommend_roles(resume_text):

    client = get_groq_client()

    prompt = f"""
You are an experienced career coach.

Analyze the resume and determine:

1. Estimated career level
2. Core skills
3. Top 10 suitable job titles
4. Adjacent career opportunities
5. Industries where the candidate is most competitive

Return ONLY valid JSON.

Format:

{{
    "career_level": "",
    "core_skills": [],
    "recommended_roles": [],
    "adjacent_roles": [],
    "industries": []
}}

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
        temperature=0.2
    )

    content = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    try:

        return json.loads(content)

    except Exception:

        return {
            "career_level": "Unknown",
            "core_skills": [],
            "recommended_roles": [],
            "adjacent_roles": [],
            "industries": []
        }
