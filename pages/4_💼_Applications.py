import streamlit as st
import pandas as pd

from services.supabase_service import get_supabase

supabase = get_supabase()

st.title("💼 Application Tracker")

st.subheader("Add Application")

company = st.text_input(
    "Company Name"
)

role = st.text_input(
    "Role"
)

job_url = st.text_input(
    "Job URL"
)

match_score = st.number_input(
    "Match Score",
    min_value=0,
    max_value=100,
    value=80
)

status = st.selectbox(
    "Application Status",
    [
        "Saved",
        "Applied",
        "Interviewing",
        "Offer",
        "Rejected"
    ]
)

from datetime import datetime

if st.button("Save Application"):

    if company and role:

        try:

            supabase.table(
                "applications"
            ).insert(
                {
                    "company": company,
                    "role": role,
                    "match_score": match_score,
                    "job_url": job_url,
                    "status": status,
                    "applied_date": datetime.utcnow().isoformat()
                }
            ).execute()

            st.success(
                "Application Saved Successfully"
            )

        except Exception as e:

            st.error(
                str(e)
            )

    else:

        st.warning(
            "Company and Role are required."
        )

st.divider()

st.subheader(
    "Application History"
)

try:

    response = supabase.table(
        "applications"
    ).select(
        "*"
    ).execute()

    data = response.data

    if len(data) > 0:

        df = pd.DataFrame(
            data
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Applications",
                len(df)
            )

        with col2:

            st.metric(
                "Applied",
                len(
                    df[
                        df["status"] == "Applied"
                    ]
                )
            )

        with col3:

            st.metric(
                "Interviewing",
                len(
                    df[
                        df["status"] == "Interviewing"
                    ]
                )
            )

        with col4:

            st.metric(
                "Offers",
                len(
                    df[
                        df["status"] == "Offer"
                    ]
                )
            )

    else:

        st.info(
            "No applications saved yet."
        )

except Exception as e:

    st.error(
        str(e)
    )