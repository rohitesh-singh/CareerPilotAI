from docx import Document
import os


def create_resume_docx(
    resume_content,
    resume_filename
):

    os.makedirs(
        "generated_resumes",
        exist_ok=True
    )

    output_file = (
        f"generated_resumes/{resume_filename}.docx"
    )

    doc = Document()

    for line in resume_content.split("\n"):

        doc.add_paragraph(line)

    doc.save(output_file)

    return output_file