import json
import re

from services.groq_service import get_groq_client


def recommend_roles(resume_text):

    client = get_groq_client()

    prompt = f"""
You are an experienced executive career coach.

Analyze this resume and determine:

1. Career level
2. Core skills
3. Top 10 recommended roles
4. Adjacent opportunities
5. Suitable industries

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

        try:

            json_match = re.search(
                r"\{.*\}",
                content,
                re.DOTALL
            )

            if json_match:

                return json.loads(
                    json_match.group()
                )

        except Exception:

            pass

    print(content)

    return {
        "career_level": "Unknown",
        "core_skills": [],
        "recommended_roles": [],
        "adjacent_roles": [],
        "industries": []
    }