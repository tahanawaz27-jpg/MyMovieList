import os

from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def recommend_movie(title: str, genre: str, rating: float):
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
    model="gemini-3.6-flash",
    contents=prompt
    )

    return response.text