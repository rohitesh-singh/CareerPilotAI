from services.groq_service import get_groq_client


def generate_resume(
    resume_text,
    job_description
):

    client = get_groq_client()

    prompt = f"""
You are an expert executive resume writer.

Your task is to rewrite and optimize the resume for the target job.

Rules:

1. Write naturally like a recruiter.
2. Keep achievements realistic.
3. Do not invent experience.
4. Keep facts from the original resume.
5. Improve ATS compatibility.
6. Prioritize keywords from the job description.
7. Use concise professional language.
8. Never use:
   - Results-driven
   - Dynamic
   - Proven track record
   - Seasoned
   - Highly motivated
   - Strategic thinker
9. Return ONLY the optimized resume.
10. Use markdown formatting.

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
        temperature=0.2
    )

    return response.choices[0].message.content