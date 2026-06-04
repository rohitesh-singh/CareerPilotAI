import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

candidate_profile = """
{
  "name":"Rohitesh Kumar Singh",
  "years_experience":"7+",
  "roles":["Program Manager III","Program Manager"],
  "skills":[
    "Program Management",
    "Agile",
    "Scrum",
    "Stakeholder Management"
  ]
}
"""

job_description = """
Required Skills & Qualifications

* Bachelor's degree in Engineering, Business Administration, Management, or related field.
* 8–10 years of experience in PMO, program management, or project governance roles.
* Strong understanding of project management methodologies (Agile, Scrum, Waterfall, Hybrid).
* Experience managing enterprise-scale transformation or technology programs.
* Excellent stakeholder management and communication skills.
* Strong analytical, problem-solving, and decision-making abilities.

Preferred Qualifications

* Experience in IT, Digital Transformation, Healthcare, BFSI, Telecom, or Consulting domains is an advantage.
* Exposure to governance reporting for leadership and CXO stakeholders.
* Experience working in global or matrix organizations.

Key Competencies

* Leadership & Team Collaboration
* Strategic Thinking
* Execution Excellence
* Risk Management
* Communication & Presentation Skills
* Stakeholder Influencing
"""

prompt = f"""
Compare this candidate profile against this job description.

Return ONLY JSON.

Format:

{{
  "overall_score": 0,
  "experience_score": 0,
  "skills_score": 0,
  "leadership_score": 0,
  "strengths": [],
  "gaps": [],
  "recommendation": ""
}}

Candidate:
{candidate_profile}

Job:
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

print(response.choices[0].message.content)