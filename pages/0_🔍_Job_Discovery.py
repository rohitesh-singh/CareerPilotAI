import streamlit as st

from datetime import datetime, timezone

from services.pdf_services import extract_text_from_pdf
from services.job_recommendation_service import (
    recommend_roles
)
from services.job_search_service import (
    search_jobs
)

st.title("🔍 Job Discovery")

st.info(
    """
### CareerPilotAI Beta

This tool helps job seekers:

• Discover suitable roles

• Find live jobs

• Analyze ATS match scores

• Generate tailored resumes

• Create cover letters

• Track applications

Feedback is welcome.
"""
)

st.write(
    """
Discover career opportunities based on your resume,
explore recommended roles, and find live jobs.
"""
)

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if st.button(
    "Analyze Career Profile"
):

    if uploaded_resume:

        resume_text = extract_text_from_pdf(
            uploaded_resume
        )

        with st.spinner(
            "Analyzing career profile..."
        ):

            result = recommend_roles(
                resume_text
            )

        st.session_state[
            "career_analysis"
        ] = result

        st.session_state[
            "resume_text"
        ] = resume_text

        st.success(
            "Career profile analyzed successfully."
        )

    else:

        st.error(
            "Upload a resume first."
        )

if "career_analysis" in st.session_state:

    result = st.session_state[
        "career_analysis"
    ]

    st.divider()

    st.subheader(
        "Career Level"
    )

    st.info(
        result.get(
            "career_level",
            "Unknown"
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Core Skills"
        )

        for skill in result.get(
            "core_skills",
            []
        ):

            st.write(
                f"✅ {skill}"
            )

    with col2:

        st.subheader(
            "Industries"
        )

        for industry in result.get(
            "industries",
            []
        ):

            st.write(
                f"🏢 {industry}"
            )

    st.divider()

    st.subheader(
        "Recommended Roles"
    )

    recommended_roles = result.get(
        "recommended_roles",
        []
    )

    for role in recommended_roles:

        st.write(
            f"🎯 {role}"
        )

    st.divider()

    st.subheader(
        "Adjacent Opportunities"
    )

    for role in result.get(
        "adjacent_roles",
        []
    ):

        st.write(
            f"🚀 {role}"
        )

    st.divider()

    st.subheader(
        "Find Live Jobs"
    )

    selected_role = st.selectbox(
        "Select Role",
        recommended_roles
        if recommended_roles
        else ["No roles available"]
    )

    location = st.selectbox(
        "Location",
        [
            "India",
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Mumbai",
            "Delhi NCR",
            "Chennai",
            "Remote"
        ]
    )

    job_age = st.selectbox(
        "Posted Within",
        [
            "Any Time",
            "24 Hours",
            "3 Days",
            "7 Days",
            "14 Days"
        ],
        index=3
    )

    if (
        selected_role
        != "No roles available"
    ):

        if st.button(
            "🔎 Search Jobs"
        ):

            with st.spinner(
                "Searching live jobs..."
            ):

                jobs = search_jobs(
                    selected_role,
                    location
                )

            st.session_state[
                "live_jobs"
            ] = jobs

            st.session_state[
                "role"
            ] = selected_role

    if "live_jobs" in st.session_state:

        jobs = st.session_state[
            "live_jobs"
        ]

        filtered_jobs = []

        now = datetime.now(
            timezone.utc
        )

        for job in jobs:

            created = job.get(
                "created",
                ""
            )

            if not created:

                filtered_jobs.append(
                    job
                )

                continue

            try:

                job_date = datetime.fromisoformat(
                    created.replace(
                        "Z",
                        "+00:00"
                    )
                )

                age_days = (
                    now - job_date
                ).days

                if job_age == "Any Time":

                    filtered_jobs.append(
                        job
                    )

                elif (
                    job_age == "24 Hours"
                    and age_days <= 1
                ):

                    filtered_jobs.append(
                        job
                    )

                elif (
                    job_age == "3 Days"
                    and age_days <= 3
                ):

                    filtered_jobs.append(
                        job
                    )

                elif (
                    job_age == "7 Days"
                    and age_days <= 7
                ):

                    filtered_jobs.append(
                        job
                    )

                elif (
                    job_age == "14 Days"
                    and age_days <= 14
                ):

                    filtered_jobs.append(
                        job
                    )

            except Exception:

                filtered_jobs.append(
                    job
                )

        st.divider()

        st.subheader(
            f"Live Jobs Found ({len(filtered_jobs)})"
        )

        if len(filtered_jobs) == 0:

            st.warning(
                "No jobs found for the selected time period."
            )

        for idx, job in enumerate(
            filtered_jobs
        ):

            with st.expander(
                f"{job['title']} | {job['company']}"
            ):

                st.write(
                    f"🏢 Company: {job['company']}"
                )

                st.write(
                    f"📍 Location: {job['location']}"
                )

                created = job.get(
                    "created",
                    ""
                )

                if created:

                    st.write(
                        f"🕒 Posted: {created[:10]}"
                    )

                description = job.get(
                    "description",
                    ""
                )

                if description:

                    st.write(
                        description[:1200]
                    )

                st.link_button(
                    "View Job Posting",
                    job["url"]
                )

                if st.button(
                    "Use For Resume Optimization",
                    key=f"use_job_{idx}"
                ):

                    st.session_state[
                        "company"
                    ] = job[
                        "company"
                    ]

                    st.session_state[
                        "role"
                    ] = job[
                        "title"
                    ]

                    st.session_state[
                        "job_url"
                    ] = job[
                        "url"
                    ]

                    st.session_state[
                        "job_description"
                    ] = description

                    st.success(
                        "Job details saved. Open Resume Optimizer to continue."
                    )

    st.divider()

    st.subheader(
        "Career Summary"
    )

    st.info(
        f"""
Career Level: {result.get('career_level', 'Unknown')}

Core Skills: {len(result.get('core_skills', []))}

Recommended Roles: {len(result.get('recommended_roles', []))}

Adjacent Opportunities: {len(result.get('adjacent_roles', []))}

Industries: {len(result.get('industries', []))}
"""
    )
