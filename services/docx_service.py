from docx import Document
import os


def create_resume_docx(
    resume_content,
    output_file="generated_resumes/optimized_resume.docx"
):

    # Create folder if it doesn't exist
    os.makedirs("generated_resumes", exist_ok=True)

    doc = Document()

    for line in resume_content.split("\n"):
        doc.add_paragraph(line)

    doc.save(output_file)

    return output_file