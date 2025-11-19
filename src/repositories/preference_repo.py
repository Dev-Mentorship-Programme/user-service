from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from src.models import (
    UserPreference,
    UserNotificationSetting,
    UserPrivacySetting,
    UserConsent,
)
from src.schemas.user_preference import (
    UserPreferenceUpdate,
    NotificationSettingUpdate,
    PrivacySettingUpdate,
    ConsentCreate,
)
from src.utils.exceptions import DatabaseException


class PreferenceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # User Preferences
    async def get_user_preference(self, user_id: UUID) -> Optional[UserPreference]:
        result = await self.db.execute(
            select(UserPreference).filter(UserPreference.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_user_preference(self, user_id: UUID) -> UserPreference:
        """Create default preferences for a new user"""
        try:
            preference = UserPreference(user_id=user_id)
            self.db.add(preference)
            await self.db.commit()
            await self.db.refresh(preference)
            return preference
        except IntegrityError:
            await self.db.rollback()
            raise DatabaseException("Failed to create user preferences")

    async def update_user_preference(
        self, user_id: UUID, data: UserPreferenceUpdate
    ) -> UserPreference:
        preference = await self.get_user_preference(user_id)

        if not preference:
            preference = await self.create_user_preference(user_id)

        # Update only provided fields
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(preference, field, value)

        preference.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(preference)
        return preference

    # Notification Settings
    async def get_notification_setting(
        self, user_id: UUID
    ) -> Optional[UserNotificationSetting]:
        result = await self.db.execute(
            select(UserNotificationSetting).filter(
                UserNotificationSetting.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def create_notification_setting(
        self, user_id: UUID
    ) -> UserNotificationSetting:
        try:
            setting = UserNotificationSetting(user_id=user_id)
            self.db.add(setting)
            await self.db.commit()
            await self.db.refresh(setting)
            return setting
        except IntegrityError:
            await self.db.rollback()
            raise DatabaseException("Failed to create notification settings")

    async def update_notification_setting(
        self, user_id: UUID, data: NotificationSettingUpdate
    ) -> UserNotificationSetting:
        setting = await self.get_notification_setting(user_id)

        if not setting:
            setting = await self.create_notification_setting(user_id)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(setting, field, value)

        setting.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(setting)
        return setting

    # Privacy Settings
    async def get_privacy_setting(self, user_id: UUID) -> Optional[UserPrivacySetting]:
        result = await self.db.execute(
            select(UserPrivacySetting).filter(UserPrivacySetting.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_privacy_setting(self, user_id: UUID) -> UserPrivacySetting:
        try:
            setting = UserPrivacySetting(user_id=user_id)
            self.db.add(setting)
            await self.db.commit()
            await self.db.refresh(setting)
            return setting
        except IntegrityError:
            await self.db.rollback()
            raise DatabaseException("Failed to create privacy settings")

    async def update_privacy_setting(
        self, user_id: UUID, data: PrivacySettingUpdate
    ) -> UserPrivacySetting:
        setting = await self.get_privacy_setting(user_id)

        if not setting:
            setting = await self.create_privacy_setting(user_id)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(setting, field, value)

        setting.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(setting)
        return setting

    # Consent Management
    async def create_consent(
        self,
        user_id: UUID,
        data: ConsentCreate,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> UserConsent:
        consent = UserConsent(
            user_id=user_id,
            consent_type=data.consent_type,
            granted=data.granted,
            version=data.version,
            ip_address=ip_address,
            user_agent=user_agent,
            granted_at=datetime.utcnow(),
            revoked_at=None if data.granted else datetime.utcnow(),
        )

        self.db.add(consent)
        await self.db.commit()
        await self.db.refresh(consent)
        return consent

    async def get_consent_history(self, user_id: UUID) -> List[UserConsent]:
        result = await self.db.execute(
            select(UserConsent)
            .filter(UserConsent.user_id == user_id)
            .order_by(UserConsent.granted_at.desc())
        )
        return result.scalars().all()

    async def get_latest_consent(
        self, user_id: UUID, consent_type: str
    ) -> Optional[UserConsent]:
        result = await self.db.execute(
            select(UserConsent)
            .filter(
                UserConsent.user_id == user_id, UserConsent.consent_type == consent_type
            )
            .order_by(UserConsent.granted_at.desc())
        )
        return result.scalar_one_or_none()
