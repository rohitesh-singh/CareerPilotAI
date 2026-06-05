from services.groq_service import get_groq_client
import json


def extract_job_details(
    job_description
):

    client = get_groq_client()

    prompt = f"""
Extract:

1. Company Name
2. Role

Return JSON only:

{{
    "company": "",
    "role": ""
}}

Job Description:

{job_description}
"""

    response = (
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )
    )

    return json.loads(
        response.choices[0].message.content
    )