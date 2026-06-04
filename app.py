import streamlit as st

st.set_page_config(
    page_title="CareerPilotAI",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 CareerPilotAI")

st.markdown("""
### AI-Powered Career Operating System

Optimize resumes, match jobs, generate tailored resumes,
track applications and accelerate your job search.
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Applications",
        "0"
    )

with col2:
    st.metric(
        "Interviews",
        "0"
    )

with col3:
    st.metric(
        "Offers",
        "0"
    )

with col4:
    st.metric(
        "Average Match Score",
        "0%"
    )

st.divider()

st.subheader("Quick Actions")

col1, col2 = st.columns(2)

with col1:
    st.info(
        "Upload a resume and analyze a job description."
    )

with col2:
    st.info(
        "Generate ATS-optimized resumes for target roles."
    )