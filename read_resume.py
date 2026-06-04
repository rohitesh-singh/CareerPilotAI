import pdfplumber
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

pdf_path = "/Users/rohitesh/Desktop/Rohitesh_Resume_03.pdf"

all_text = ""

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            all_text += text + "\n"

response = supabase.table("resumes").insert({
    "user_id": "1fe4b438-9257-4258-83da-1c33f9fbd190",
    "resume_text": all_text
}).execute()

print("Resume saved successfully!")