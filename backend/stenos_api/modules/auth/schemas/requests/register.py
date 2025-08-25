from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    plain_password: str
