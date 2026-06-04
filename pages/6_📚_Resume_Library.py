import streamlit as st
import pandas as pd

from services.supabase_service import get_supabase

supabase = get_supabase()

st.title("📚 Resume Library")

response = supabase.table(
    "generated_resumes"
).select(
    "*"
).order(
    "created_at",
    desc=True
).execute()

data = response.data

if len(data) == 0:

    st.info(
        "No saved resumes found."
    )

else:

    df = pd.DataFrame(
        data
    )

    for _, row in df.iterrows():

        with st.expander(
            f"{row['company']} | {row['role']}"
        ):

            st.text(
                row["created_at"]
            )

            st.markdown(
                row["resume_content"]
            )