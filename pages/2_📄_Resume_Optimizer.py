import streamlit as st

from services.pdf_services import extract_text_from_pdf
from services.resume_optimizer_service import analyze_resume
from services.supabase_service import get_supabase

supabase = get_supabase()

st.title("📄 Resume Optimizer")

company = st.text_input(
    "Company Name"
)

role = st.text_input(
    "Role"
)

job_url = st.text_input(
    "Job URL"
)

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

if st.button("Analyze Match"):

    if uploaded_resume and job_description:

        resume_text = extract_text_from_pdf(
            uploaded_resume
        )

        with st.spinner(
            "Analyzing resume..."
        ):

            result = analyze_resume(
                resume_text,
                job_description
            )

        st.session_state["analysis_result"] = result
        st.session_state["company"] = company
        st.session_state["role"] = role
        st.session_state["job_url"] = job_url

if "analysis_result" in st.session_state:

    result = st.session_state[
        "analysis_result"
    ]

    st.success(
        "Analysis Complete"
    )

    score = result.get(
        "match_score",
        0
    )

    st.metric(
        "Match Score",
        f"{score}%"
    )

    if score >= 80:

        st.success(
            "🎯 Strong match. Worth applying."
        )

    elif score >= 60:

        st.warning(
            "⚠️ Moderate match. Resume optimization recommended."
        )

    else:

        st.error(
            "❌ Low match. Significant resume tailoring needed."
        )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Strengths"
        )

        for item in result.get(
            "strengths",
            []
        ):

            st.write(
                f"✅ {item}"
            )

    with col2:

        st.subheader(
            "Missing Keywords"
        )

        for item in result.get(
            "missing_keywords",
            []
        ):

            st.write(
                f"❌ {item}"
            )

    st.subheader(
        "ATS Recommendations"
    )

    for item in result.get(
        "ats_recommendations",
        []
    ):

        st.write(
            f"• {item}"
        )

    st.subheader(
        "Interview Probability"
    )

    probability = result.get(
        "interview_probability",
        "Unknown"
    )

    st.info(
        probability
    )

    st.divider()

    st.subheader(
        "Save Application"
    )

    if st.button(
        "💾 Save To Application Tracker"
    ):

        try:

            supabase.table(
                "applications"
            ).insert(
                {
                    "company": st.session_state.get(
                        "company",
                        ""
                    ),
                    "role": st.session_state.get(
                        "role",
                        ""
                    ),
                    "job_url": st.session_state.get(
                        "job_url",
                        ""
                    ),
                    "match_score": score,
                    "status": "Saved"
                }
            ).execute()

            st.success(
                "Application saved successfully."
            )

        except Exception as e:

            st.error(
                str(e)
            )