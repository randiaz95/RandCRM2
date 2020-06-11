from pydantic import BaseModel

class AuthLogin(BaseModel):
    email: str
    password: str

class AuthConfirm(BaseModel):
    id: str
    code: str
