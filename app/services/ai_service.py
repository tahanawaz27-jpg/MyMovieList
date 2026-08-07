# app/services/ai_service.py
import json
import os
import random
from groq import Groq
from app.utils.logger import logger

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None


def recommend_movie(title: str) -> list[dict]:
    if client is None:
        logger.error("AI recommendation failed: API key missing.")
        return []

    random_seeds = [
        "Focus on hidden gems or lesser-known masterpieces.",
        "Focus on critically acclaimed classics and fan favorites.",
        "Focus on modern and highly-rated contemporary films.",
        "Focus on unique, cult-classic, or stylish cinema choices.",
    ]
    selected_seed = random.choice(random_seeds)

    prompt = f"""
The user enjoyed the movie "{title}".

Suggest EXACTLY 3 distinct movie recommendations similar to "{title}".
{selected_seed}

Return a JSON object containing a "recommendations" array with 3 objects matching this structure:
{{
  "recommendations": [
    {{
      "title": "Movie Title",
      "genre": "Genre(s)",
      "reason": "2-3 sentences explaining why it is similar."
    }}
  ]
}}
"""

    try:
        logger.info(f"Sending 3-movie recommendation request for '{title}'")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.9,
            response_format={"type": "json_object"},  # Guarantees strictly valid JSON
            messages=[
                {
                    "role": "system",
                    "content": "You are a movie recommendation engine that responds strictly in valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        content = response.choices[0].message.content.strip()
        data = json.loads(content)

        return data.get("recommendations", [])

    except Exception as e:
        logger.exception(f"Groq API error while recommending for '{title}': {e}")
        return []