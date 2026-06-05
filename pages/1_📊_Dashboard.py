import streamlit as st
import pandas as pd

from services.supabase_service import get_supabase

st.title("📊 Dashboard")

supabase = get_supabase()

try:

    response = (
        supabase
        .table("applications")
        .select("*")
        .execute()
    )

    data = response.data

    if len(data) > 0:

        df = pd.DataFrame(data)

        total_applications = len(df)

        average_score = round(
            df["match_score"].mean(),
            1
        )

        saved_jobs = len(
            df[
                df["status"] == "Saved"
            ]
        )

        applied_jobs = len(
            df[
                df["status"] == "Applied"
            ]
        )

        interviews = len(
            df[
                df["status"].isin(
                    [
                        "Recruiter Screen",
                        "Interview Scheduled",
                        "Final Round"
                    ]
                )
            ]
        )

        offers = len(
            df[
                df["status"] == "Offer"
            ]
        )

        rejected = len(
            df[
                df["status"] == "Rejected"
            ]
        )

        top_score = df[
            "match_score"
        ].max()

        interview_rate = round(
            (
                interviews
                / total_applications
            ) * 100,
            1
        )

        offer_rate = round(
            (
                offers
                / total_applications
            ) * 100,
            1
        )

    else:

        total_applications = 0
        average_score = 0
        saved_jobs = 0
        applied_jobs = 0
        interviews = 0
        offers = 0
        rejected = 0
        top_score = 0
        interview_rate = 0
        offer_rate = 0

except Exception:

    total_applications = 0
    average_score = 0
    saved_jobs = 0
    applied_jobs = 0
    interviews = 0
    offers = 0
    rejected = 0
    top_score = 0
    interview_rate = 0
    offer_rate = 0

st.subheader(
    "Application Performance"
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Applications",
        total_applications
    )

with col2:

    st.metric(
        "Avg ATS Score",
        f"{average_score}%"
    )

with col3:

    st.metric(
        "Interviews",
        interviews
    )

with col4:

    st.metric(
        "Offers",
        offers
    )

st.divider()

col5, col6, col7, col8 = st.columns(4)

with col5:

    st.metric(
        "Saved Jobs",
        saved_jobs
    )

with col6:

    st.metric(
        "Applied Jobs",
        applied_jobs
    )

with col7:

    st.metric(
        "Interview Rate",
        f"{interview_rate}%"
    )

with col8:

    st.metric(
        "Offer Rate",
        f"{offer_rate}%"
    )

st.divider()

col9, col10 = st.columns(2)

with col9:

    st.metric(
        "Top ATS Score",
        f"{top_score}%"
    )

with col10:

    st.metric(
        "Rejected",
        rejected
    )

st.divider()

if total_applications > 0:

    st.subheader(
        "Application Status Breakdown"
    )

    status_counts = (
        df["status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    st.bar_chart(
        status_counts.set_index(
            "Status"
        )
    )

st.divider()

st.subheader(
    "CareerPilotAI Insights"
)

if total_applications == 0:

    st.info(
        "Start adding applications to see analytics."
    )

else:

    if average_score < 70:

        st.warning(
            "Average ATS score is below 70%. Consider optimizing resumes further."
        )

    elif average_score < 85:

        st.info(
            "Average ATS score is healthy. Continue tailoring resumes to job descriptions."
        )

    else:

        st.success(
            "Excellent ATS performance. Resume quality is strong."
        )

st.divider()

st.subheader(
    "CareerPilotAI"
)

st.info(
    """
Upload resumes, analyze ATS match,
generate optimized resumes,
track applications,
monitor interviews,
and measure your job search performance.
"""
)
