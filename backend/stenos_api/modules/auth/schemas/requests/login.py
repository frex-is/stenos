from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    plain_password: str