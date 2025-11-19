from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
from src.config.database import get_db_session
from src.config.cache import get_redis_client
from src.repositories.auth_repo import AuthRepository
from src.services.auth_service import AuthService
from src.schemas.auth import (
    UserRegistrationRequest,
    UserLoginRequest,
    AuthResponse,
    TokenResponse,
    RefreshTokenRequest,
)
from src.schemas.response import ResponseModel

router = APIRouter()


def get_auth_service(
    db: AsyncSession = Depends(get_db_session),
    redis_client: redis.Redis = Depends(get_redis_client),
) -> AuthService:
    """Dependency to get AuthService instance"""
    auth_repo = AuthRepository(db)
    return AuthService(auth_repo, redis_client)


@router.post(
    "/register",
    response_model=ResponseModel[AuthResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register New User",
    description="Create a new user account with email, password, and personal details",
)
async def register(
    data: UserRegistrationRequest, service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user

    - **email**: Valid email address (must be unique)
    - **password**: Strong password (min 8 chars, uppercase, lowercase, digit, special char)
    - **first_name**: User's first name
    - **last_name**: User's last name
    - **phone**: Optional phone number
    - **referral_code**: Optional referral code
    """
    result = await service.register_user(data)

    return ResponseModel(success=True, message="Registration successful", data=result)


@router.post(
    "/login",
    response_model=ResponseModel[AuthResponse],
    summary="User Login",
    description="Authenticate user with email and password",
)
async def login(
    data: UserLoginRequest, service: AuthService = Depends(get_auth_service)
):
    """
    Login with email and password

    - **email**: Registered email address
    - **password**: User password

    Returns access token and refresh token
    """
    result = await service.login_user(data)

    return ResponseModel(success=True, message="Login successful", data=result)


@router.post(
    "/refresh",
    response_model=ResponseModel[TokenResponse],
    summary="Refresh Access Token",
    description="Generate new access token using refresh token",
)
async def refresh_token(
    data: RefreshTokenRequest, service: AuthService = Depends(get_auth_service)
):
    """
    Refresh access token

    - **refresh_token**: Valid refresh token

    Returns new access token and refresh token
    """
    result = await service.refresh_access_token(data.refresh_token)

    return ResponseModel(
        success=True, message="Token refreshed successfully", data=result
    )
