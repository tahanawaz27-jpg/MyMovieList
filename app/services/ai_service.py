import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


def recommend_movie(title: str, genre: str, rating: float):

    if client is None:
        return "AI recommendation unavailable"

    prompt = f"""
    The user enjoyed this movie:

    Title: {title}
    Genre: {genre}
    Rating: {rating}/10

    Recommend ONE similar movie.

    Explain why in 2-3 sentences.
    Don't use markdown.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text