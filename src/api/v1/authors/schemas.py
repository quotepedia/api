from pydantic import BaseModel, ConfigDict


class AuthorResponse(BaseModel):
    id: int
    name: str
    created_by_user_id: int | None


class AuthorCreateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
