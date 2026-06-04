from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import (
    getSampleStyleSheet
)
import os


def create_resume_pdf(
    resume_content,
    resume_filename
):

    os.makedirs(
        "generated_resumes",
        exist_ok=True
    )

    output_file = (
        f"generated_resumes/{resume_filename}.pdf"
    )

    doc = SimpleDocTemplate(
        output_file
    )

    styles = getSampleStyleSheet()

    content = []

    for line in resume_content.split("\n"):

        if line.strip():

            content.append(
                Paragraph(
                    line.replace("<", "&lt;").replace(">", "&gt;"),
                    styles["BodyText"]
                )
            )

            content.append(
                Spacer(1, 6)
            )

    doc.build(content)

    return output_file