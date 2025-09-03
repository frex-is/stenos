from pydantic import BaseModel


class LoginSuccessful(BaseModel):
    user_id: str