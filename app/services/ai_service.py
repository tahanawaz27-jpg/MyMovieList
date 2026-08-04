import os
from groq import Groq

print("========== GROQ DEBUG ==========")
print("GROQ_API_KEY FOUND:", os.getenv("GROQ_API_KEY") is not None)
print("GROQ_API_KEY VALUE:", os.getenv("GROQ_API_KEY"))
print("================================")

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key) if api_key else None


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
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Groq Error:", str(e))
        return f"AI recommendation failed: {str(e)}"