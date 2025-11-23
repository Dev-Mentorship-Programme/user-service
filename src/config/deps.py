from typing import Optional, Dict, Any
from uuid import UUID
from fastapi import Depends, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from src.utils.exceptions import (
    InvalidTokenException,
    InactiveUserException,
    MissingTokenException,
)
from src.config.security import decode_token
from src.models.users import User
from src.config.database import get_db_session
from src.config.cache import get_redis_client

security = HTTPBearer(auto_error=False)


async def get_token_from_header(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    authorization: Optional[str] = Header(None),
) -> str:
    """
    Extract JWT token from Authorization header

    Supports both:
    - Bearer token via HTTPBearer
    - Manual Authorization header parsing
    """
    # Try HTTPBearer first
    if credentials:
        return credentials.credentials

    # Fallback to manual header parsing
    if authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1]

    raise MissingTokenException()


async def verify_token(token: str = Depends(get_token_from_header)) -> Dict[str, Any]:
    """
    Verify and decode JWT token

    Args:
        token: JWT token string

    Returns:
        Decoded token payload
    """
    try:
        payload = decode_token(token)

        # Verify token type
        if payload.get("type") != "access":
            raise InvalidTokenException("Invalid token type")

        # Verify required fields
        user_id = payload.get("user_id")
        if not user_id:
            raise InvalidTokenException("Token missing user_id")

        return payload

    except Exception as e:
        if isinstance(e, (InvalidTokenException, MissingTokenException)):
            raise
        raise InvalidTokenException(f"Token verification failed: {str(e)}")


async def get_current_user_from_db(
    payload: Dict[str, Any] = Depends(verify_token), db:AsyncSession = Depends(get_db_session)
) -> User:
    """
    Get current user from database

    Args:
        payload: Decoded JWT payload
        db: Database session

    Returns:
        User model instance
    """
    user_id = payload.get("user_id")

    user: User = db.query(User).filter(User.id == UUID(user_id)).first()

    if not user:
        raise InvalidTokenException("User not found")

    if not user.is_active:
        raise InactiveUserException("User account is inactive")

    return user


async def get_current_user(
    payload: Dict[str, Any] = Depends(verify_token),
    redis_client: Redis = Depends(get_redis_client),
    db: AsyncSession = Depends(get_db_session),
) -> Dict[str, Any]:
    """
    Get current authenticated user with Redis caching

    This dependency:
    1. Verifies the JWT token
    2. Checks Redis cache for user data
    3. Falls back to database if not in cache
    4. Validates user is active

    Args:
        payload: Decoded JWT token payload
        redis_client: Redis connection
        db: Database session

    Returns:
        Dictionary containing user information
    """
    user_id = payload.get("user_id")

    # Try to get user from Redis cache
    cache_key = f"user:{user_id}"
    cached_user = await redis_client.get(cache_key)

    if cached_user:
        import json

        user_data = json.loads(cached_user)

        # Validate cached user is still active
        if not user_data.get("is_active"):
            raise InactiveUserException()

        return user_data

    # Cache miss - get from database
    user: User = db.query(User).filter(User.id == UUID(user_id)).first()

    if not user:
        raise InvalidTokenException("User not found")

    if not user.is_active:
        raise InactiveUserException()

    # Prepare user data
    user_data = {
        "user_id": str(user.id),
        "email": user.email,
        "phone": user.phone,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "role": getattr(user, "role", "user"),
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }

    # Cache user data in Redis (expire after 1 hour)
    import json

    await redis_client.setex(cache_key, 3600, json.dumps(user_data))  # 1 hour

    return user_data
