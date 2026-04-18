from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    uid: str
    email: Optional[str] = None

class AuthRequest(BaseModel):
    email: str
    password: str

class GoogleAuthRequest(BaseModel):
    id_token: str
