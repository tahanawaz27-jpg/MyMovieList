# app/schemas/recommendation.py
from pydantic import BaseModel


class RecommendationItem(BaseModel):
    title: str
    genre: str
    reason: str


class RecommendationResponse(BaseModel):
    recommendations: list[RecommendationItem]