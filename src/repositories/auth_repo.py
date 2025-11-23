from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Optional
from uuid import UUID
from datetime import datetime
from src.models.users import User
from src.config.security import hash_password, verify_password
from src.utils.exceptions import (
    AlreadyExistsException,
    NotFoundException,
    InvalidCredentialsException,
    DatabaseException,
)


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        phone: Optional[str] = None,
        role: str = "user",
    ) -> User:
        """Create a new user"""
        try:
            # Check if email already exists
            result = await self.db.execute(select(User).filter(User.email == email))
            existing_user = result.scalar_one_or_none()
            if existing_user:
                raise AlreadyExistsException(
                    message="Email already registered", resource="email"
                )

            # Check if phone already exists
            if phone:
                result = await self.db.execute(select(User).filter(User.phone == phone))
                existing_phone = result.scalar_one_or_none()
                if existing_phone:
                    raise AlreadyExistsException(
                        message="Phone number already registered", resource="phone"
                    )

            # Create user
            user = User(
                email=email,
                password_hash=hash_password(password),
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                role=role,
                is_active=True,
                is_verified=False,
            )

            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)

            return user

        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Database error: {str(e)}")

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    async def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate user with email and password"""
        user = await self.get_user_by_email(email)

        if not user:
            raise InvalidCredentialsException()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsException()

        if not user.is_active:
            from src.utils.exceptions import InactiveUserException

            raise InactiveUserException()

        # Update last login
        user.last_login = datetime.utcnow()
        await self.db.commit()

        return user

    async def update_password(self, user_id: UUID, new_password: str) -> User:
        """Update user password"""
        user = await self.get_user_by_id(user_id)

        if not user:
            raise NotFoundException(message="User not found")

        user.password_hash = hash_password(new_password)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def verify_user_email(self, user_id: UUID) -> User:
        """Mark user email as verified"""
        user = await self.get_user_by_id(user_id)

        if not user:
            raise NotFoundException(message="User not found")

        user.is_verified = True
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def deactivate_user(self, user_id: UUID) -> User:
        """Deactivate user account"""
        user = await self.get_user_by_id(user_id)

        if not user:
            raise NotFoundException(message="User not found")

        user.is_active = False
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def activate_user(self, user_id: UUID) -> User:
        """Activate user account"""
        user = await self.get_user_by_id(user_id)

        if not user:
            raise NotFoundException(message="User not found")

        user.is_active = True
        await self.db.commit()
        await self.db.refresh(user)

        return user
