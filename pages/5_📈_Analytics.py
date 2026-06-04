import streamlit as st
import pandas as pd
import plotly.express as px

from services.supabase_service import get_supabase

st.title("📈 Analytics Dashboard")

supabase = get_supabase()

try:

    response = supabase.table(
        "applications"
    ).select(
        "*"
    ).execute()

    data = response.data

    if not data:

        st.info(
            "No application data available."
        )
        st.stop()

    df = pd.DataFrame(data)

    total_applications = len(df)

    average_score = round(
        df["match_score"].mean(),
        1
    )

    interviewing = len(
        df[
            df["status"] == "Interviewing"
        ]
    )

    offers = len(
        df[
            df["status"] == "Offer"
        ]
    )

    interview_rate = round(
        (
            interviewing /
            total_applications
        ) * 100,
        1
    )

    offer_rate = round(
        (
            offers /
            total_applications
        ) * 100,
        1
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Applications",
            total_applications
        )

    with col2:

        st.metric(
            "Average Match Score",
            f"{average_score}%"
        )

    with col3:

        st.metric(
            "Interview Rate",
            f"{interview_rate}%"
        )

    with col4:

        st.metric(
            "Offer Rate",
            f"{offer_rate}%"
        )

    st.divider()

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

    fig = px.pie(
        status_counts,
        names="Status",
        values="Count",
        title="Applications by Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "Match Scores"
    )

    fig2 = px.bar(
        df,
        x="company",
        y="match_score",
        color="status",
        title="Match Score by Company"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "Application Funnel"
    )

    saved = len(
        df[
            df["status"] == "Saved"
        ]
    )

    applied = len(
        df[
            df["status"] == "Applied"
        ]
    )

    interviewing = len(
        df[
            df["status"] == "Interviewing"
        ]
    )

    offers = len(
        df[
            df["status"] == "Offer"
        ]
    )

    funnel_df = pd.DataFrame(
        {
            "Stage": [
                "Saved",
                "Applied",
                "Interviewing",
                "Offer"
            ],
            "Count": [
                saved,
                applied,
                interviewing,
                offers
            ]
        }
    )

    fig3 = px.funnel(
        funnel_df,
        x="Count",
        y="Stage"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

except Exception as e:

    st.error(
        str(e)
    )