from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
from uuid import UUID
from src.config.settings import settings
from src.utils.exceptions import InvalidTokenException, TokenExpiredException

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityManager:
    """Handles password hashing and JWT token operations"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plain text password"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(
        data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token

        Args:
            data: Payload data to encode in token
            expires_delta: Token expiration time

        Returns:
            Encoded JWT token string
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "access"})

        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

        return encoded_jwt

    @staticmethod
    def create_refresh_token(
        data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT refresh token

        Args:
            data: Payload data to encode in token
            expires_delta: Token expiration time

        Returns:
            Encoded JWT refresh token string
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )

        to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "refresh"})

        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """
        Decode and verify a JWT token

        Args:
            token: JWT token string

        Returns:
            Decoded token payload

        Raises:
            InvalidTokenException: If token is invalid
            TokenExpiredException: If token has expired
        """
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise TokenExpiredException("Token has expired")
        except jwt.PyJWTError as e:
            raise InvalidTokenException(f"Invalid token: {str(e)}")

    @staticmethod
    def create_tokens_for_user(
        user_id: UUID,
        email: str,
        role: str = "user",
        additional_claims: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, str]:
        """
        Create both access and refresh tokens for a user

        Args:
            user_id: User's unique identifier
            email: User's email address
            role: User's role (default: "user")
            additional_claims: Additional data to include in token

        Returns:
            Dictionary with access_token and refresh_token
        """
        token_data = {"user_id": str(user_id), "email": email, "role": role}

        if additional_claims:
            token_data.update(additional_claims)

        access_token = SecurityManager.create_access_token(token_data)
        refresh_token = SecurityManager.create_refresh_token(
            {"user_id": str(user_id), "email": email}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }


# Convenience functions
def hash_password(password: str) -> str:
    """Hash a password"""
    return SecurityManager.hash_password(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password"""
    return SecurityManager.verify_password(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create an access token"""
    return SecurityManager.create_access_token(data, expires_delta)


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a refresh token"""
    return SecurityManager.create_refresh_token(data, expires_delta)


def decode_token(token: str) -> Dict[str, Any]:
    """Decode a JWT token"""
    return SecurityManager.decode_token(token)
