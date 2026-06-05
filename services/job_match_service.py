from services.resume_optimizer_service import (
    analyze_resume
)


def score_live_job(
    resume_text,
    job_description
):

    result = analyze_resume(
        resume_text,
        job_description
    )

    return result.get(
        "match_score",
        0
    )