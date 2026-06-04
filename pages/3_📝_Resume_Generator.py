import streamlit as st

from services.pdf_services import extract_text_from_pdf
from services.resume_generator_service import generate_resume
from services.docx_service import create_resume_docx
from services.supabase_service import get_supabase

supabase = get_supabase()

st.title("📝 Resume Generator")

first_name = st.text_input(
    "First Name"
)

last_name = st.text_input(
    "Last Name"
)

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

        st.session_state["generated_resume"] = optimized_resume

        st.session_state["first_name"] = first_name
        st.session_state["last_name"] = last_name
        st.session_state["company"] = company
        st.session_state["role"] = role
        st.session_state["job_url"] = job_url

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

    first_name = st.session_state.get(
        "first_name",
        "Candidate"
    )

    last_name = st.session_state.get(
        "last_name",
        ""
    )

    role = st.session_state.get(
        "role",
        "Resume"
    )

    existing = supabase.table(
        "generated_resumes"
    ).select(
        "resume_version"
    ).eq(
        "first_name",
        first_name
    ).eq(
        "last_name",
        last_name
    ).eq(
        "role",
        role
    ).execute()

    version = len(
        existing.data
    ) + 1

    safe_role = (
        role.strip()
        .replace(" ", "_")
    )

    resume_filename = (
        f"{first_name}_{last_name}_{safe_role}_V{version}"
    )

    docx_path = create_resume_docx(
        optimized_resume,
        resume_filename
    )

    with open(
        docx_path,
        "rb"
    ) as file:

        st.download_button(
            label="📥 Download DOCX Resume",
            data=file,
            file_name=f"{resume_filename}.docx",
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
                        "first_name": first_name,
                        "last_name": last_name,
                        "company": st.session_state.get(
                            "company",
                            "Unknown"
                        ),
                        "role": role,
                        "job_url": st.session_state.get(
                            "job_url",
                            ""
                        ),
                        "resume_content": optimized_resume,
                        "resume_version": version,
                        "resume_filename": resume_filename
                    }
                ).execute()

                st.success(
                    "Resume saved successfully."
                )

            except Exception as e:

                st.error(
                    str(e)
                )

    with col2:

        if st.button(
            "🚀 Apply & Save Application"
        ):

            try:

                supabase.table(
                    "applications"
                ).insert(
                    {
                        "company": st.session_state.get(
                            "company",
                            "Unknown"
                        ),
                        "role": role,
                        "job_url": st.session_state.get(
                            "job_url",
                            ""
                        ),
                        "match_score": 0,
                        "status": "Applied",
                        "resume_filename": resume_filename
                    }
                ).execute()

                st.success(
                    "Application saved successfully."
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