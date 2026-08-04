import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

print("API KEY FOUND:", api_key is not None)

client = genai.Client(api_key=api_key) if api_key else None


def recommend_movie(title: str, genre: str, rating: float):

    if client is None:
        return "AI recommendation unavailable. API key missing."

    prompt = f"""
The user enjoyed this movie:

Title: {title}
Genre: {genre}
Rating: {rating}/10

Recommend ONE similar movie.

Explain why in 2-3 sentences.
Don't use markdown.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )

        return response.text if response.text else "No recommendation generated."

    except Exception as e:
        print("Gemini Error:", e)
        return f"AI recommendation failed: {e}"