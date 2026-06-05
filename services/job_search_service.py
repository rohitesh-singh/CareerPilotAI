import os
import requests

from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv(
    "ADZUNA_APP_ID"
)

APP_KEY = os.getenv(
    "ADZUNA_APP_KEY"
)


def search_jobs(
    role,
    location="India",
    results=25
):

    if not APP_ID or not APP_KEY:

        return []

    try:

        url = (
            "https://api.adzuna.com/v1/api/jobs/in/search/1"
        )

        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": role,
            "where": location,
            "results_per_page": results,
            "content-type": "application/json"
        }

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        jobs = []

        for job in data.get(
            "results",
            []
        ):

            jobs.append(
                {
                    "company": (
                        job.get(
                            "company",
                            {}
                        ).get(
                            "display_name",
                            ""
                        )
                    ),

                    "title": job.get(
                        "title",
                        ""
                    ),

                    "location": (
                        job.get(
                            "location",
                            {}
                        ).get(
                            "display_name",
                            ""
                        )
                    ),

                    "url": job.get(
                        "redirect_url",
                        ""
                    ),

                    "description": job.get(
                        "description",
                        ""
                    ),

                    "created": job.get(
                        "created",
                        ""
                    )
                }
            )

        jobs.sort(
            key=lambda x: x.get(
                "created",
                ""
            ),
            reverse=True
        )

        return jobs

    except Exception as e:

        print(
            f"Job Search Error: {e}"
        )

        return []