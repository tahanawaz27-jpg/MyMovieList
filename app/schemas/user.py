from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=50,
    )


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )


class Token(BaseModel):
    access_token: str
    token_type: str