import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
import requests
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import toml as tomllib

WEB_API_KEY = None
secrets = {}

try:
    root_dir = Path(__file__).resolve().parent.parent.parent.parent
    secrets_path = root_dir / ".streamlit" / "secrets.toml"
    
    print(f"Loading secrets from: {secrets_path}")
    if secrets_path.exists():
        if hasattr(tomllib, "load"):
            with open(secrets_path, "rb") as f:
                secrets = tomllib.load(f)
        else:
            with open(secrets_path, "r", encoding="utf-8") as f:
                secrets = tomllib.loads(f.read())
                
        if "firebase_client" in secrets:
            WEB_API_KEY = secrets["firebase_client"].get("apiKey")
                
        if "firebase_admin" in secrets:
            cred = credentials.Certificate(secrets["firebase_admin"])
            # Kiem tra app chua duoc initialize thi moi initialize
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
        else:
            if not firebase_admin._apps:
                firebase_admin.initialize_app()
    else:
        print("secrets_path not found!")
        if not firebase_admin._apps:
            firebase_admin.initialize_app()
        
    db = firestore.client()
except Exception as e:
    print("Lỗi khởi tạo Firebase trong Backend:", e)
    db = None

def get_db():
    return db

def verify_token(token: str):
    try:
        return auth.verify_id_token(token)
    except Exception:
        return None

def sign_in_with_email_password(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={WEB_API_KEY}"
    res = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
    return res

def sign_up_with_email_password(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={WEB_API_KEY}"
    res = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
    return res
