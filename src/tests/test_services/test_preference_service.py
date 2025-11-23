from datetime import datetime
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

from src.services.preference_service import PreferenceService
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
from src.models import UserPreference, UserNotificationSetting, UserPrivacySetting, UserConsent


@pytest.mark.unit
class TestPreferenceService:
    """Test suite for PreferenceService"""

    @pytest.fixture
    def mock_preference_repo(self):
        """Create a mocked PreferenceRepository"""
        return AsyncMock(spec=PreferenceRepository)

    @pytest.fixture
    def preference_service(self, mock_preference_repo):
        """Create a PreferenceService instance with mocked repository"""
        return PreferenceService(mock_preference_repo)

    @pytest.fixture
    def sample_user_id(self):
        """Generate a sample user ID"""
        return uuid4()

    # =========================================================================
    # USER PREFERENCES TESTS
    # =========================================================================

    @pytest.mark.asyncio
    async def test_get_preferences_existing(
        self, 
        preference_service, 
        mock_preference_repo, 
        sample_user_id
    ):
        """Test getting preferences when they already exist"""

        # Arrange
        existing_preference = UserPreferenceResponse(
            id=uuid4(),
            user_id=sample_user_id,
            language="en",
            currency="USD",
            theme="light",
            timezone="America/New_York",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        mock_preference_repo.get_user_preference.return_value = existing_preference

        # Act
        result = await preference_service.get_preferences(sample_user_id)

        # Assert
        assert result.language == "en"
        assert result.currency == "USD"
        assert result.theme == "light"
        assert result.timezone == "America/New_York"
        mock_preference_repo.get_user_preference.assert_called_once_with(sample_user_id)
        # Should NOT create if already exists
        mock_preference_repo.create_user_preference.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_preferences_nonexistent_creates_default(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test getting preferences creates defaults if none exist"""
        # Arrange
        # First call returns None (preference doesn't exist)
        # Second call returns created preference
        default_preference = UserPreference(
            id=uuid4(),
            user_id=sample_user_id,
            language="en",
            currency="USD",
            theme="light",
            timezone="America/New_York",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        mock_preference_repo.get_user_preference.return_value = None
        mock_preference_repo.create_user_preference.return_value = default_preference

        # Act
        result = await preference_service.get_preferences(sample_user_id)

        # Assert
        assert result.language == "en"
        # Should create default preferences
        mock_preference_repo.create_user_preference.assert_called_once_with(sample_user_id)

    @pytest.mark.asyncio
    async def test_update_preferences_success(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test successfully updating user preferences"""
        # Arrange
        update_data = UserPreferenceUpdate(
            language="fr",
            currency="EUR",
            timezone="Europe/Paris",
            theme="dark",
        )

        updated_response = UserPreference(
            id=uuid4(),
            user_id=sample_user_id,
            language="fr",
            currency="EUR",
            theme="dark",
            timezone="Europe/Paris",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        mock_preference_repo.update_user_preference.return_value = updated_response

        # Act
        result = await preference_service.update_preferences(sample_user_id, update_data)

        # Assert
        assert result.language == "fr"
        assert result.currency == "EUR"
        assert result.theme == "dark"
        assert result.timezone == "Europe/Paris"
        mock_preference_repo.update_user_preference.assert_called_once_with(
            sample_user_id, update_data
        )

    @pytest.mark.asyncio
    async def test_update_preferences_partial_update(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test updating only specific preference fields"""
        # Arrange
        update_data = UserPreferenceUpdate(language="de")  # Only update language

        updated_preference = UserPreference(
            id=uuid4(),
            user_id=sample_user_id,
            language="de",
            currency="USD",  # Unchanged
            theme="light",   # Unchanged
            timezone="America/New_York",  # Unchanged
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        mock_preference_repo.update_user_preference.return_value = updated_preference

        # Act
        result = await preference_service.update_preferences(sample_user_id, update_data)

        # Assert
        assert result.language == "de"
        assert result.currency == "USD"
        assert result.theme == "light"
        assert result.timezone == "America/New_York"
        mock_preference_repo.update_user_preference.assert_called_once_with(
            sample_user_id, update_data
        )

    # =========================================================================
    # NOTIFICATION SETTINGS TESTS
    # =========================================================================

    @pytest.mark.asyncio
    async def test_get_notification_settings_existing(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test getting existing notification settings"""
        # Arrange
        existing_setting = UserNotificationSetting(
            id=uuid4(),
            user_id=sample_user_id,
            email_enabled=True,
            sms_enabled=False,
            sms_transaction_alerts=False,
            sms_security_alerts=True,
            sms_marketing=False,
            push_enabled=True,
            email_transaction_alerts=True,
            push_transaction_alerts=True,
            push_marketing=False,
            push_security_alerts=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        mock_preference_repo.get_notification_setting.return_value = existing_setting

        # Act
        result = await preference_service.get_notification_settings(sample_user_id)

        # Assert
        assert result.email_enabled is True
        assert result.sms_enabled is False
        assert result.sms_transaction_alerts is False
        assert result.sms_security_alerts is True
        assert result.sms_marketing is False
        assert result.push_enabled is True
        assert result.email_transaction_alerts is True
        assert result.push_transaction_alerts is True
        assert result.push_marketing is False
        assert result.push_security_alerts is True

        mock_preference_repo.get_notification_setting.assert_called_once_with(sample_user_id)

    @pytest.mark.asyncio
    async def test_get_notification_settings_nonexistent_creates_default(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test notification settings creates defaults if none exist"""
        # Arrange
        default_setting = UserNotificationSetting(
            id=uuid4(),
            user_id=sample_user_id,
            email_enabled=True,
            sms_enabled=True,
            push_enabled=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        mock_preference_repo.get_notification_setting.return_value = None
        mock_preference_repo.create_notification_setting.return_value = default_setting

        # Act
        result = await preference_service.get_notification_settings(sample_user_id)

        # Assert
        assert result.email_enabled is True
        assert result.sms_enabled is True
        assert result.push_enabled is True
        mock_preference_repo.create_notification_setting.assert_called_once_with(sample_user_id)

    @pytest.mark.asyncio
    async def test_update_notification_settings_success(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test successfully updating notification settings"""
        # Arrange
        update_data = NotificationSettingUpdate(
            email_enabled=False,
            sms_enabled=True,
            push_enabled=False
        )

        updated_setting = UserNotificationSetting(
            id=uuid4(),
            user_id=sample_user_id,
            email_enabled=False,
            sms_enabled=True,
            push_enabled=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        mock_preference_repo.update_notification_setting.return_value = updated_setting

        # Act
        result = await preference_service.update_notification_settings(
            sample_user_id, 
            update_data
        )

        # Assert
        assert result.email_enabled is False
        assert result.sms_enabled is True
        assert result.push_enabled is False
        mock_preference_repo.update_notification_setting.assert_called_once()

    # =========================================================================
    # PRIVACY SETTINGS TESTS
    # =========================================================================

    @pytest.mark.asyncio
    async def test_get_privacy_settings_existing(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test getting existing privacy settings"""
        # Arrange
        existing_setting = UserPrivacySetting(
            id=uuid4(),
            user_id=sample_user_id,
            profile_visible=True,
            show_email=False,
            show_phone=False,
            show_transaction_history=False,
            allow_data_collection=True,
            allow_analytics=True,
            allow_third_party_sharing=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        mock_preference_repo.get_privacy_setting.return_value = existing_setting

        # Act
        result = await preference_service.get_privacy_settings(sample_user_id)

        # Assert
        assert result.profile_visible is True
        assert result.show_email is False
        assert result.show_phone is False
        assert result.show_transaction_history is False
        assert result.allow_data_collection is True
        assert result.allow_analytics is True
        assert result.allow_third_party_sharing is False
        mock_preference_repo.get_privacy_setting.assert_called_once_with(sample_user_id)

    @pytest.mark.asyncio
    async def test_get_privacy_settings_nonexistent_creates_default(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test privacy settings creates defaults if none exist"""
        # Arrange
        default_setting = UserPrivacySetting(
            id=uuid4(),
            user_id=sample_user_id,
            profile_visible=True,
            show_email=False,
            show_phone=False,
            show_transaction_history=False,
            allow_data_collection=True,
            allow_analytics=True,
            allow_third_party_sharing=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        mock_preference_repo.get_privacy_setting.return_value = None
        mock_preference_repo.create_privacy_setting.return_value = default_setting

        # Act
        result = await preference_service.get_privacy_settings(sample_user_id)

        # Assert
        assert result.profile_visible is True
        assert result.show_email is False
        assert result.show_phone is False
        assert result.show_transaction_history is False
        assert result.allow_data_collection is True
        assert result.allow_analytics is True
        assert result.allow_third_party_sharing is False

        mock_preference_repo.create_privacy_setting.assert_called_once_with(sample_user_id)

    @pytest.mark.asyncio
    async def test_update_privacy_settings_success(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test successfully updating privacy settings"""
        # Arrange
        update_data = PrivacySettingUpdate(
            profile_visible=False,
            show_email=False,
            show_phone=False,
            show_transaction_history=False,
            allow_data_collection=False,
            allow_analytics=False,
            allow_third_party_sharing=False,
        )

        updated_setting = UserPrivacySetting(
            id=uuid4(),
            user_id=sample_user_id,
            profile_visible=False,
            show_email=False,
            show_phone=False,
            show_transaction_history=False,
            allow_data_collection=False,
            allow_analytics=False,
            allow_third_party_sharing=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        mock_preference_repo.update_privacy_setting.return_value = updated_setting

        # Act
        result = await preference_service.update_privacy_settings(
            sample_user_id,
            update_data
        )

        # Assert
        assert result.profile_visible is False
        assert result.show_email is False
        assert result.show_phone is False
        assert result.show_transaction_history is False
        assert result.allow_data_collection is False
        assert result.allow_analytics is False
        assert result.allow_third_party_sharing is False

        mock_preference_repo.update_privacy_setting.assert_called_once()

    # =========================================================================
    # CONSENT MANAGEMENT TESTS
    # =========================================================================

    @pytest.mark.asyncio
    async def test_grant_consent_success(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test successfully granting consent"""
        # Arrange
        consent_data = ConsentCreate(
            consent_type="terms_of_service",
            granted=True,
            version="v2.0",
        )

        created_consent = ConsentResponse(
            id=uuid4(),
            user_id=sample_user_id,
            consent_type="terms_of_service",
            granted=True,
            version="v2.0",
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0",
            granted_at=datetime.utcnow(),
            revoked_at=None,
        )

        mock_preference_repo.create_consent.return_value = created_consent

        # Act
        result = await preference_service.grant_or_revoke_consent(
            sample_user_id,
            consent_data
        )

        # Assert
        assert result.consent_type == "terms_of_service"
        assert result.granted is True
        assert result.version == "v2.0"


    @pytest.mark.asyncio
    async def test_revoke_consent_success(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test successfully revoking consent"""
        # Arrange
        consent_data = ConsentCreate(
            consent_type="marketing",
            granted=False,
            version="v1.0",
        )

        revoked_consent = ConsentResponse(
            id=uuid4(),
            user_id=sample_user_id,
            consent_type="marketing",
            granted=False,
            version="v1.0",
            ip_address=None,
            user_agent=None,
            granted_at=datetime.utcnow(),
            revoked_at=datetime.utcnow(),
        )

        mock_preference_repo.create_consent.return_value = revoked_consent

        # Act
        result = await preference_service.grant_or_revoke_consent(
            sample_user_id,
            consent_data
        )

        # Assert
        assert result.granted is False
        assert result.consent_type == "marketing"
        assert result.version == "v1.0"


    @pytest.mark.asyncio
    async def test_get_consent_history_success(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test getting consent history"""
        # Arrange
        consent1 = UserConsent(
            id=uuid4(),
            user_id=sample_user_id,
            consent_type="terms_of_service",
            granted=True,
            version="v2.0",
            granted_at=datetime.utcnow(),
        )
        consent2 = UserConsent(
            id=uuid4(),
            user_id=sample_user_id,
            consent_type="privacy_policy",
            granted=True,
            version="v1.5",
            granted_at=datetime.utcnow(),
        )
        consent3 = UserConsent(
            id=uuid4(),
            user_id=sample_user_id,
            consent_type="marketing",
            granted=False,
            version="v1.0",
            granted_at=datetime.utcnow(),
        )

        mock_preference_repo.get_consent_history.return_value = [
            consent1, consent2, consent3
        ]

        # Act
        result = await preference_service.get_consent_history(sample_user_id)

        # Assert
        assert result.total == 3
        assert len(result.consents) == 3
        assert result.consents[0].consent_type == "terms_of_service"
        assert result.consents[2].granted is False
        mock_preference_repo.get_consent_history.assert_called_once_with(sample_user_id)

    @pytest.mark.asyncio
    async def test_get_consent_history_empty(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test getting consent history when no consents exist"""
        # Arrange
        mock_preference_repo.get_consent_history.return_value = []

        # Act
        result = await preference_service.get_consent_history(sample_user_id)

        # Assert
        assert result.total == 0
        assert len(result.consents) == 0

    # =========================================================================
    # ERROR HANDLING TESTS
    # =========================================================================

    @pytest.mark.asyncio
    async def test_update_preferences_repository_error(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test handling repository errors during preference update"""
        # Arrange
        update_data = UserPreferenceUpdate(language="en")
        mock_preference_repo.update_user_preference.side_effect = Exception("DB Error")

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await preference_service.update_preferences(sample_user_id, update_data)

        assert "DB Error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_notification_settings_repository_error(
        self,
        preference_service,
        mock_preference_repo,
        sample_user_id
    ):
        """Test handling repository errors when getting notification settings"""
        # Arrange
        mock_preference_repo.get_notification_setting.side_effect = Exception("DB Error")

        # Act & Assert
        with pytest.raises(Exception):
            await preference_service.get_notification_settings(sample_user_id)
