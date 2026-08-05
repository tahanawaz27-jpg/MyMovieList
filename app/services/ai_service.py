import os

from groq import Groq

from app.utils.logger import logger


api_key = os.getenv("GROQ_API_KEY")

if api_key:
    logger.info("Groq API key loaded successfully.")
else:
    logger.warning("Groq API key not found.")

client = Groq(api_key=api_key) if api_key else None

def recommend_movie(title: str):
    if client is None:
        logger.error(
            "AI recommendation failed: API key missing."
        )
        return "AI recommendation unavailable. API key missing."

    prompt = f"""
The user enjoyed the movie "{title}".

Recommend ONE similar movie.

In 2-3 sentences explain why it is similar.

If the movie title is unknown or does not exist, reply only:
Movie not found.

Do not use markdown.
"""

    try:
        logger.info(
            f"Sending recommendation request for '{title}'"
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        logger.info(
            f"Recommendation generated successfully for '{title}'"
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.exception(
            f"Groq API error while recommending '{title}': {e}"
        )

        return "Unable to generate recommendation at this time."