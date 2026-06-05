import streamlit as st
import pandas as pd

from datetime import datetime
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

status_options = [
    "Saved",
    "Applied",
    "Recruiter Screen",
    "Interview Scheduled",
    "Final Round",
    "Offer",
    "No Response"
    "Rejected",
    "Withdrawn"
]

status = st.selectbox(
    "Application Status",
    status_options
)

notes = st.text_area(
    "Notes",
    height=100
)

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
                    "notes": notes,
                    "applied_date": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
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

    response = (
        supabase
        .table("applications")
        .select("*")
        .execute()
    )

    data = response.data

    if len(data) > 0:

        df = pd.DataFrame(data)

        total_apps = len(df)

        avg_score = round(
            df["match_score"].mean(),
            1
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

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Applications",
                total_apps
            )

        with col2:

            st.metric(
                "Avg ATS",
                f"{avg_score}%"
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

        st.subheader(
            "Update Application Status"
        )

        for row in data:

            with st.expander(
                f"{row['company']} | {row['role']}"
            ):

                st.write(
                    f"ATS Score: {row.get('match_score', 0)}%"
                )

                st.write(
                    f"Current Status: {row.get('status', '')}"
                )

                if row.get(
                    "job_url"
                ):

                    st.write(
                        row["job_url"]
                    )

                new_status = st.selectbox(
                    "Update Status",
                    status_options,
                    index=status_options.index(
                        row.get(
                            "status",
                            "Saved"
                        )
                    ),
                    key=row["id"]
                )

                updated_notes = st.text_area(
                    "Notes",
                    value=row.get(
                        "notes",
                        ""
                    ),
                    key=f"notes_{row['id']}"
                )

                if st.button(
                    "Update",
                    key=f"update_{row['id']}"
                ):

                    try:

                        supabase.table(
                            "applications"
                        ).update(
                            {
                                "status": new_status,
                                "notes": updated_notes,
                                "updated_at": datetime.utcnow().isoformat()
                            }
                        ).eq(
                            "id",
                            row["id"]
                        ).execute()

                        st.success(
                            "Updated successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            str(e)
                        )

        st.divider()

        st.subheader(
            "Application Data"
        )

        display_columns = [
            col
            for col in [
                "company",
                "role",
                "match_score",
                "status",
                "applied_date",
                "updated_at"
            ]
            if col in df.columns
        ]

        st.dataframe(
            df[display_columns],
            use_container_width=True
        )

    else:

        st.info(
            "No applications saved yet."
        )

except Exception as e:

    st.error(
        str(e)
    )
