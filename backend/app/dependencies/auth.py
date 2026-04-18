from fastapi import Header, HTTPException
from typing import Optional
from app.core.firebase_config import verify_token
from app.schemas.auth import UserSchema

def get_current_user(authorization: Optional[str] = Header(None)) -> UserSchema:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    token = authorization.split(" ")[1]
    user_data = verify_token(token)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return UserSchema(uid=user_data.get("uid"), email=user_data.get("email"))
