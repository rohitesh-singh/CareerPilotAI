import os
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

try:
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                resume_text += text + "\n"

except Exception as e:
    print(f"\n❌ Error reading resume: {e}")
    exit()

# ==========================================
# READ JOB DESCRIPTION
# ==========================================

try:
    with open("job_description.txt", "r", encoding="utf-8") as f:
        job_description = f.read()

except Exception as e:
    print(f"\n❌ Error reading job_description.txt: {e}")
    exit()

# ==========================================
# GENERATE RESUME PROMPT
# ==========================================

prompt = f"""
You are a senior executive resume writer who has written resumes for
Google, Microsoft, Amazon, Meta and Fortune 500 Program Managers.

Your task is to tailor the candidate's resume to the target job description.

CRITICAL RULES:

1. Do NOT invent experience.
2. Do NOT invent companies.
3. Do NOT invent achievements.
4. Do NOT invent certifications.
5. Only improve wording of existing experience.
6. Preserve all factual information.
7. Use natural human language.
8. Make the writing sound like it was written by an experienced recruiter.
9. Avoid generic AI phrases.
10. Avoid buzzwords such as:
   - Results-driven
   - Dynamic professional
   - Highly motivated
   - Proven track record
   - Visionary leader
   - Leverage synergies
   - Strategic thinker
   - Seasoned professional

11. Never use:
   - Results-driven
   - Dynamic
   - Proven track record
   - Seasoned
   - Highly motivated
   - Strategic thinker

12. Write in the style of a recruiter preparing a resume for a real candidate, not marketing copy.

13. Focus on clarity and impact.
14. Incorporate ATS keywords naturally.
15. Do not keyword stuff.
16. Keep bullet points concise.
17. Use strong action verbs.
18. Highlight:
    - Program Management
    - Technical Program Management
    - Stakeholder Management
    - Agile Delivery
    - Risk Management
    - Cross-functional Leadership
    - Delivery Excellence

19. Every bullet point should:
    - Start with an action verb
    - Explain what was done
    - Explain impact when available
    - Stay under 2 lines

20. Keep the tone professional and authentic.
21. Optimize for ATS and recruiter readability.
22. Return ONLY the finished resume.

OUTPUT FORMAT:

# PROFESSIONAL SUMMARY

# CORE SKILLS

# PROFESSIONAL EXPERIENCE

# EDUCATION

# CERTIFICATIONS

Candidate Resume:

{resume_text}

Target Job Description:

{job_description}
"""

# ==========================================
# GENERATE RESUME
# ==========================================

try:

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

    generated_resume = response.choices[0].message.content

except Exception as e:

    print(f"\n❌ Error generating resume: {e}")
    exit()

# ==========================================
# DISPLAY GENERATED RESUME
# ==========================================

print("\n")
print("=" * 70)
print("TAILORED RESUME")
print("=" * 70)
print("\n")

print(generated_resume)

# ==========================================
# SAVE LOCALLY
# ==========================================

try:

    with open(
        "generated_resume.md",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(generated_resume)

    print("\n✅ Resume saved as generated_resume.md")

except Exception as e:

    print(f"\n❌ Failed to save resume locally: {e}")

# ==========================================
# SAVE TO SUPABASE
# ==========================================

try:

    supabase.table("generated_resumes").insert({
        "role": "Unknown",
        "company": "Unknown",
        "resume_content": generated_resume
    }).execute()

    print("✅ Resume saved to Supabase")

except Exception as e:

    print(f"\n❌ Failed to save to Supabase: {e}")

print("\n🎉 Resume generation completed successfully!")