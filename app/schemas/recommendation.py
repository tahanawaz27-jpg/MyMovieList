from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    title: str
    genre: str
    rating: float


class RecommendationResponse(BaseModel):
    recommendation: str