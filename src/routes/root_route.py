from fastapi import APIRouter
from src.routes.v1 import auth,user_preference_settings

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(user_preference_settings.router, prefix="/settings", tags=["Preference Settings"])
