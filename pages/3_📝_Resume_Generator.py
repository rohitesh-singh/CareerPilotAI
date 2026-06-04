import streamlit as st

from services.pdf_services import extract_text_from_pdf
from services.resume_generator_service import generate_resume
from services.docx_service import create_resume_docx
from services.supabase_service import get_supabase

supabase = get_supabase()

st.title("📝 Resume Generator")

company = st.text_input(
    "Company Name"
)

role = st.text_input(
    "Role"
)

job_url = st.text_input(
    "Job URL (Optional)"
)

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

if st.button("Generate Optimized Resume"):

    if uploaded_resume and job_description:

        resume_text = extract_text_from_pdf(
            uploaded_resume
        )

        with st.spinner(
            "Generating optimized resume..."
        ):

            optimized_resume = generate_resume(
                resume_text,
                job_description
            )

        st.session_state[
            "generated_resume"
        ] = optimized_resume

        st.session_state[
            "company"
        ] = company

        st.session_state[
            "role"
        ] = role

        st.session_state[
            "job_url"
        ] = job_url

        st.success(
            "Resume Generated Successfully"
        )

    else:

        st.error(
            "Upload a resume and paste a job description."
        )

if "generated_resume" in st.session_state:

    optimized_resume = st.session_state[
        "generated_resume"
    ]

    docx_path = create_resume_docx(
        optimized_resume
    )

    with open(
        docx_path,
        "rb"
    ) as file:

        st.download_button(
            label="📥 Download DOCX Resume",
            data=file,
            file_name="optimized_resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Save Resume"
        ):

            try:

                supabase.table(
                    "generated_resumes"
                ).insert(
                    {
                        "company": st.session_state.get(
                            "company",
                            "Unknown"
                        ),
                        "role": st.session_state.get(
                            "role",
                            "Unknown"
                        ),
                        "job_url": st.session_state.get(
                            "job_url",
                            ""
                        ),
                        "resume_content": optimized_resume
                    }
                ).execute()

                st.success(
                    "Resume saved successfully."
                )

            except Exception as e:

                st.error(
                    str(e)
                )

    st.divider()

    st.subheader(
        "Generated Resume Preview"
    )

    st.markdown(
        optimized_resume
    )