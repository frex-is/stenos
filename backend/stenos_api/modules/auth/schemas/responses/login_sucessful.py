from pydantic import BaseModel


class LoginSuccessful(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
