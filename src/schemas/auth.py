from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
import re


class UserRegistrationRequest(BaseModel):
    email: EmailStr
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    referral_code: Optional[str] = None

    @field_validator("password")
    def validate_password(cls, v):
        """
        Validate password strength:
        - At least 8 characters
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit
        - Contains at least one special character
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")

        return v

    @field_validator("phone")
    def validate_phone(cls, v):
        if v:
            # Remove spaces and dashes
            phone = re.sub(r"[\s\-]", "", v)

            # Check if it's a valid phone number (basic validation)
            if not re.match(r"^\+?[1-9]\d{9,14}$", phone):
                raise ValueError("Invalid phone number format")

            return phone
        return v


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class UserResponse(BaseModel):
    id: UUID
    email: str
    phone: Optional[str]
    first_name: str
    last_name: str
    is_active: bool
    is_verified: bool
    role: str
    created_at: datetime
    last_login: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class AuthResponse(BaseModel):
    user: UserResponse
    tokens: TokenResponse
