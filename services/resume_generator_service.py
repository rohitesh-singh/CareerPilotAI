from services.groq_service import get_groq_client


def generate_resume(
    resume_text,
    job_description
):

    client = get_groq_client()

    prompt = f"""
You are an elite executive resume writer and career strategist.

Your objective is to create a highly competitive, ATS-optimized resume tailored to the target job description.

The resume should be suitable for candidates at any level including:
- Entry-level
- Associate
- Individual Contributor
- Senior Professional
- Manager
- Director
- Vice President
- Executive Leadership

Rules:

1. Never invent experience, companies, projects, certifications, education, or achievements.
2. Preserve factual accuracy from the original resume.
3. Optimize the resume specifically for the target job description.
4. Prioritize relevant keywords naturally.
5. Improve clarity, readability, and ATS compatibility.
6. Strengthen accomplishment statements using available evidence from the resume.
7. Remove redundancy and weak language.
8. Create a compelling professional summary aligned with the target role.
9. Highlight measurable business impact wherever possible.
10. Use concise and professional language.
11. Focus on outcomes, ownership, responsibilities, and achievements.
12. Ensure the final resume appears professionally written by a premium resume writing service.
13. Return ONLY the optimized resume.
14. Use markdown formatting.

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