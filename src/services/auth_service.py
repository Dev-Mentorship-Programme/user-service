from typing import Dict, Any
from uuid import UUID
from datetime import timedelta
import redis.asyncio as redis

from src.repositories.auth_repo import AuthRepository
from src.config.security import SecurityManager, decode_token

from src.schemas.auth import (
    UserRegistrationRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
    AuthResponse,
    # ChangePasswordRequest,
)
from src.config.settings import settings
from src.utils.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    NotFoundException,
)


class AuthService:
    def __init__(self, auth_repo: AuthRepository, redis_client: redis.Redis = None):
        self.auth_repo = auth_repo
        self.redis_client = redis_client

    async def register_user(self, data: UserRegistrationRequest) -> AuthResponse:
        """
        Register a new user

        Args:
            data: User registration data

        Returns:
            AuthResponse with user data and tokens
        """
        # Create user
        user = await self.auth_repo.create_user(
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            role="user",
        )

        # Generate tokens
        tokens = SecurityManager.create_tokens_for_user(
            user_id=user.id, email=user.email, role=user.role
        )

        # Store refresh token in Redis
        if self.redis_client:
            await self.redis_client.setex(
                f"refresh_token:{user.id}",
                settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
                tokens["refresh_token"],
            )

        # Cache user data
        if self.redis_client:
            import json

            user_data = {
                "user_id": str(user.id),
                "email": user.email,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "role": user.role,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            }
            await self.redis_client.setex(
                f"user:{user.id}", 3600, json.dumps(user_data)  # 1 hour
            )

        return AuthResponse(
            user=UserResponse.model_validate(user),
            tokens=TokenResponse(
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                token_type="bearer",
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            ),
        )

    async def login_user(self, data: UserLoginRequest) -> AuthResponse:
        """
        Authenticate user and return tokens

        Args:
            data: Login credentials

        Returns:
            AuthResponse with user data and tokens
        """
        # Authenticate user
        user = await self.auth_repo.authenticate_user(data.email, data.password)

        # Generate tokens
        tokens = SecurityManager.create_tokens_for_user(
            user_id=user.id,
            email=user.email,
            role=user.role,
            additional_claims={"is_verified": user.is_verified},
        )

        # Store refresh token in Redis
        if self.redis_client:
            await self.redis_client.setex(
                f"refresh_token:{user.id}",
                settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
                tokens["refresh_token"],
            )

        # Cache user data
        if self.redis_client:
            import json

            user_data = {
                "user_id": str(user.id),
                "email": user.email,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "role": user.role,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            }
            await self.redis_client.setex(
                f"user:{user.id}", 3600, json.dumps(user_data)
            )

        return AuthResponse(
            user=UserResponse.model_validate(user),
            tokens=TokenResponse(
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                token_type="bearer",
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            ),
        )

    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """
        Generate new access token using refresh token

        Args:
            refresh_token: Valid refresh token

        Returns:
            New TokenResponse
        """
        try:
            # Decode refresh token
            payload = decode_token(refresh_token)

            # Verify token type
            if payload.get("type") != "refresh":
                raise InvalidTokenException("Invalid token type")

            user_id = payload.get("user_id")

            # Verify refresh token exists in Redis
            if self.redis_client:
                stored_token = await self.redis_client.get(f"refresh_token:{user_id}")
                if not stored_token or stored_token != refresh_token:
                    raise InvalidTokenException("Invalid refresh token")

            # Get user
            user = await self.auth_repo.get_user_by_id(UUID(user_id))
            if not user:
                raise InvalidCredentialsException("User not found")

            if not user.is_active:
                from src.utils.exceptions import InactiveUserException

                raise InactiveUserException()

            # Generate new tokens
            tokens = SecurityManager.create_tokens_for_user(
                user_id=user.id,
                email=user.email,
                role=user.role,
                additional_claims={"is_verified": user.is_verified},
            )

            # Update refresh token in Redis
            if self.redis_client:
                await self.redis_client.setex(
                    f"refresh_token:{user.id}",
                    settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
                    tokens["refresh_token"],
                )

            return TokenResponse(
                access_token=tokens["access_token"],
                refresh_token=tokens["refresh_token"],
                token_type="bearer",
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            )

        except Exception as e:
            if isinstance(e, InvalidTokenException):
                raise
            raise InvalidTokenException(f"Token refresh failed: {str(e)}")

    async def logout_user(self, user_id: UUID) -> bool:
        """
        Logout user by invalidating tokens

        Args:
            user_id: User ID

        Returns:
            True if successful
        """
        if self.redis_client:
            # Delete refresh token
            await self.redis_client.delete(f"refresh_token:{user_id}")

            # Delete cached user data
            await self.redis_client.delete(f"user:{user_id}")

        return True
