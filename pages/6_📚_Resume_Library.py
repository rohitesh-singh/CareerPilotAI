import streamlit as st
import pandas as pd

from services.supabase_service import get_supabase

supabase = get_supabase()

st.title("📚 Resume Library")

try:

    response = (
        supabase
        .table("generated_resumes")
        .select("*")
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    data = response.data

    if not data:

        st.info(
            "No resumes found."
        )

    else:

        df = pd.DataFrame(data)

        columns = [
            "resume_filename",
            "company",
            "role",
            "resume_version",
            "created_at"
        ]

        st.dataframe(
            df[columns],
            use_container_width=True
        )

except Exception as e:

    st.error(
        str(e)
    )
