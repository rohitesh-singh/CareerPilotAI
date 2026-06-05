from services.groq_service import get_groq_client


def generate_cover_letter(
    resume_text,
    job_description,
    company,
    role
):

    client = get_groq_client()

    prompt = f"""
You are an elite executive career coach and cover letter writer.

Create a tailored cover letter for the candidate.

Requirements:

1. Personalize for the company and role.
2. Use information from the candidate's resume.
3. Highlight the most relevant experience.
4. Keep the tone professional and authentic.
5. Avoid generic phrases and buzzwords.
6. Do not invent achievements or experience.
7. Suitable for all career levels:
   - Entry Level
   - Associate
   - Individual Contributor
   - Manager
   - Director
   - VP
   - Executive
8. Maximum one page.
9. ATS-friendly.
10. Return ONLY the cover letter.
11. Do not mention skills not present in the resume.
12. Do not sound generic or overly enthusiastic.
13. Match the seniority level of the candidate.
14. Focus on business impact and relevance.
15. Avoid clichés such as:
    - Passionate
    - Results-driven
    - Dynamic
    - Team player
    - Strategic thinker
16. Keep length between 250 and 400 words.
17. Use a modern professional tone.

Company:
{company}

Role:
{role}

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
        temperature=0.3
    )

    return response.choices[0].message.content