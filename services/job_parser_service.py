import json
import re

from services.groq_service import get_groq_client


def extract_job_details(job_description):

    client = get_groq_client()

    prompt = f"""
Extract the following information from this job description:

1. Company Name
2. Job Title / Role

Return ONLY valid JSON.

Example:

{{
    "company": "Google",
    "role": "Technical Program Manager"
}}

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

    return {
        "company": "",
        "role": ""
    }