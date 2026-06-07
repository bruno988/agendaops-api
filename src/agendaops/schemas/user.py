from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=6)


class UserRead(BaseModel):
    id: int
    username: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"