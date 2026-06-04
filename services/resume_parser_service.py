import re


def extract_candidate_details(resume_text):

    result = {
        "name": "",
        "email": "",
        "phone": ""
    }

    # Extract email
    email_match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        resume_text
    )

    if email_match:
        result["email"] = email_match.group()

    # Extract phone number
    phone_match = re.search(
        r'(\+?\d[\d\s\-\(\)]{8,}\d)',
        resume_text
    )

    if phone_match:
        result["phone"] = phone_match.group().strip()

    # Candidate name
    lines = resume_text.split("\n")

    for line in lines[:15]:

        clean_line = line.strip()

        if not clean_line:
            continue

        if "@" in clean_line:
            continue

        if len(clean_line) > 50:
            continue

        words = clean_line.split()

        if 2 <= len(words) <= 4:

            if all(
                word.replace(".", "").isalpha()
                for word in words
            ):

                result["name"] = clean_line
                break

    if not result["name"]:
        result["name"] = "Candidate"

    return result
