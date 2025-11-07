from uuid import UUID
from typing import Optional


from src.repositories.preference_repo import PreferenceRepository
from src.schemas.user_preference import (
    UserPreferenceUpdate,
    UserPreferenceResponse,
    NotificationSettingUpdate,
    NotificationSettingResponse,
    PrivacySettingUpdate,
    PrivacySettingResponse,
    ConsentCreate,
    ConsentResponse,
    ConsentHistoryResponse,
)


class PreferenceService:
    def __init__(self, preference_repo: PreferenceRepository):
        self.preference_repo = preference_repo

    # User Preferences
    async def get_preferences(self, user_id: UUID) -> UserPreferenceResponse:
        preference = await self.preference_repo.get_user_preference(user_id)

        if not preference:
            # Create default preferences if none exist
            preference = await self.preference_repo.create_user_preference(user_id)

        return UserPreferenceResponse.model_validate(preference)

    async def update_preferences(
        self, 
        user_id: UUID, 
        data: UserPreferenceUpdate
    ) -> UserPreferenceResponse:
        preference = await self.preference_repo.update_user_preference(user_id, data)
        return UserPreferenceResponse.model_validate(preference)

    # Notification Settings
    async def get_notification_settings(
        self, user_id: UUID
    ) -> NotificationSettingResponse:
        setting = await self.preference_repo.get_notification_setting(user_id)

        if not setting:
            setting = await self.preference_repo.create_notification_setting(user_id)

        return NotificationSettingResponse.model_validate(setting)

    async def update_notification_settings(
        self, user_id: UUID, data: NotificationSettingUpdate
    ) -> NotificationSettingResponse:
        setting = await self.preference_repo.update_notification_setting(user_id, data)
        return NotificationSettingResponse.model_validate(setting)

    # Privacy Settings
    async def get_privacy_settings(self, user_id: UUID) -> PrivacySettingResponse:
        setting = await self.preference_repo.get_privacy_setting(user_id)

        if not setting:
            setting = await self.preference_repo.create_privacy_setting(user_id)

        return PrivacySettingResponse.model_validate(setting)

    async def update_privacy_settings(
        self, user_id: UUID, data: PrivacySettingUpdate
    ) -> PrivacySettingResponse:
        setting = await self.preference_repo.update_privacy_setting(user_id, data)
        return PrivacySettingResponse.model_validate(setting)

    # Consent Management
    async def grant_or_revoke_consent(
        self,
        user_id: UUID,
        data: ConsentCreate,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> ConsentResponse:
        consent = await self.preference_repo.create_consent(
            user_id, data, ip_address, user_agent
        )
        return ConsentResponse.model_validate(consent)

    async def get_consent_history(self, user_id: UUID) -> ConsentHistoryResponse:
        consents = await self.preference_repo.get_consent_history(user_id)
        return ConsentHistoryResponse(
            consents=[ConsentResponse.model_validate(c) for c in consents],
            total=len(consents),
        )
