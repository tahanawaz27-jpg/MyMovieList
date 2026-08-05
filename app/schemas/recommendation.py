from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    title: str


class RecommendationResponse(BaseModel):
    recommendation: str