from fastapi import APIRouter, HTTPException
from app.models.user_model import User
from app.auth.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

fake_user_db = {
    "admin": {
        "username": "admin",
        "password": "admin"  # (in production, password should be hashed)
    }
}

@router.post("/login")
async def login(user: User):
    if user.username in fake_user_db and user.password == fake_user_db[user.username]["password"]:
        token = create_access_token({"sub": user.username})
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid username or password")
