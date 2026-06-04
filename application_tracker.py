import os

from dotenv import load_dotenv
from supabase import create_client

# ==========================================
# LOAD ENV
# ==========================================

load_dotenv()

# ==========================================
# SUPABASE
# ==========================================

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# ==========================================
# USER INPUT
# ==========================================

company = input("Company Name: ")
role = input("Role: ")
job_url = input("Job URL: ")

status = "Saved"

notes = ""

match_score = int(
    input("Match Score (0-100): ")
)

# ==========================================
# SAVE
# ==========================================

response = supabase.table(
    "applications"
).insert({
    "company": company,
    "role": role,
    "job_url": job_url,
    "status": status,
    "notes": notes,
    "match_score": match_score
}).execute()

print("\n✅ Application saved successfully!")