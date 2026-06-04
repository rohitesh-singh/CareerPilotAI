import streamlit as st
import pandas as pd

from services.supabase_service import get_supabase

st.title("📊 Dashboard")

supabase = get_supabase()

try:

    response = supabase.table(
        "applications"
    ).select(
        "*"
    ).execute()

    data = response.data

    if len(data) > 0:

        df = pd.DataFrame(data)

        total_applications = len(df)

        interviews = len(
            df[
                df["status"] == "Interviewing"
            ]
        )

        offers = len(
            df[
                df["status"] == "Offer"
            ]
        )

        average_score = round(
            df["match_score"].mean(),
            1
        )

    else:

        total_applications = 0
        interviews = 0
        offers = 0
        average_score = 0

except Exception:

    total_applications = 0
    interviews = 0
    offers = 0
    average_score = 0

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Applications",
        total_applications
    )

with col2:

    st.metric(
        "Interviews",
        interviews
    )

with col3:

    st.metric(
        "Offers",
        offers
    )

with col4:

    st.metric(
        "Average Match Score",
        f"{average_score}%"
    )

st.divider()

st.subheader(
    "CareerPilotAI"
)

st.info(
    """
Upload resumes, optimize them for jobs,
generate ATS-friendly resumes,
track applications and monitor progress.
"""
)