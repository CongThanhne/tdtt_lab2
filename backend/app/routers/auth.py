from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
import requests

from app.dependencies.auth import get_current_user
from app.schemas.auth import UserSchema, AuthRequest, GoogleAuthRequest
from app.core.firebase_config import sign_in_with_email_password, sign_up_with_email_password, verify_token, secrets, WEB_API_KEY

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def get_me(user: UserSchema = Depends(get_current_user)):
    return user

@router.post("/login")
def login(req: AuthRequest):
    res = sign_in_with_email_password(req.email, req.password)
    if res.status_code == 200:
        return res.json()
    raise HTTPException(status_code=400, detail=res.json().get("error", {}).get("message", "Login failed"))

@router.post("/signup")
def signup(req: AuthRequest):
    res = sign_up_with_email_password(req.email, req.password)
    if res.status_code == 200:
        return res.json()
    raise HTTPException(status_code=400, detail=res.json().get("error", {}).get("message", "Signup failed"))

@router.post("/google")
def google_verify(req: GoogleAuthRequest):
    user_data = verify_token(req.id_token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    return {"idToken": req.id_token, "email": user_data.get("email"), "uid": user_data.get("uid")}

# === Luong dang nhap Google OAuth2 ===
google_conf = secrets.get("google-login", {})
GOOGLE_CLIENT_ID = google_conf.get("google_client_id")
GOOGLE_CLIENT_SECRET = google_conf.get("google_client_secret")
GOOGLE_REDIRECT_URI = google_conf.get("google_redirect_uri", "http://localhost:8000/auth/google/callback")
FRONTEND_URL = google_conf.get("frontend_url", "http://localhost:8501")

@router.get("/google/start")
def google_start():
    url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        "response_type=code&"
        "scope=openid%20email%20profile&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        "access_type=offline"
    )
    return RedirectResponse(url)

@router.get("/google/callback")
def google_callback(code: str = None, error: str = None):
    if error or not code:
        raise HTTPException(status_code=400, detail="Google authentication failed")
    
    # Doi ma code de lay id_token
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    res = requests.post(token_url, data=payload)
    if res.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to exchange Google code")
    
    data = res.json()
    google_id_token = data.get("id_token")
    
    # Doi Google Token lay Firebase Token
    idp_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={WEB_API_KEY}"
    idp_payload = {
        "postBody": f"id_token={google_id_token}&providerId=google.com",
        "requestUri": "http://localhost",
        "returnIdpCredential": True,
        "returnSecureToken": True
    }
    idp_res = requests.post(idp_url, json=idp_payload)
    if idp_res.status_code != 200:
        print("Firebase IdP Error:", idp_res.text)
        raise HTTPException(status_code=400, detail="Failed to link Google Auth with Firebase")
        
    firebase_token = idp_res.json().get("idToken")
    
    # Danh vong redirect id_token nguoc ve Frontend Streamlit URL params
    return RedirectResponse(f"{FRONTEND_URL}?id_token={firebase_token}")
