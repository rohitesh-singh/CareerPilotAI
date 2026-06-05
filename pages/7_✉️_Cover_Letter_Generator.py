import streamlit as st

from services.pdf_services import extract_text_from_pdf
from services.cover_letter_service import (
    generate_cover_letter
)
from services.docx_service import create_resume_docx
from services.pdf_resume_service import create_resume_pdf

st.title("✉️ Cover Letter Generator")

company = st.text_input(
    "Company Name",
    value=st.session_state.get(
        "company",
        ""
    )
)

role = st.text_input(
    "Role",
    value=st.session_state.get(
        "role",
        ""
    )
)

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

if st.button(
    "Generate Cover Letter"
):

    if uploaded_resume and job_description:

        resume_text = extract_text_from_pdf(
            uploaded_resume
        )

        with st.spinner(
            "Generating cover letter..."
        ):

            cover_letter = (
                generate_cover_letter(
                    resume_text,
                    job_description,
                    company,
                    role
                )
            )

        st.session_state[
            "cover_letter"
        ] = cover_letter

        st.success(
            "Cover Letter Generated"
        )

    else:

        st.error(
            "Upload a resume and paste a job description."
        )

if "cover_letter" in st.session_state:

    cover_letter = st.session_state[
        "cover_letter"
    ]

    filename = (
        f"{role}_Cover_Letter"
    .replace("/", "_")
    .replace("-", "_")
    .replace(" ", "_")
        )
    

    docx_path = create_resume_docx(
        cover_letter,
        filename
    )

    pdf_path = create_resume_pdf(
        cover_letter,
        filename
    )

    col1, col2 = st.columns(2)

    with col1:

        with open(
            docx_path,
            "rb"
        ) as file:

            st.download_button(
                "📥 Download DOCX",
                file,
                file_name=f"{filename}.docx"
            )

    with col2:

        with open(
            pdf_path,
            "rb"
        ) as file:

            st.download_button(
                "📄 Download PDF",
                file,
                file_name=f"{filename}.pdf"
            )

    st.divider()

    st.subheader(
        "Cover Letter Preview"
    )

    st.markdown(
        cover_letter
    )

