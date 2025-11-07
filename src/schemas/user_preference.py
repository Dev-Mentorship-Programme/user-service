from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum


# Enums
class ConsentTypeEnum(str, Enum):
    TERMS_OF_SERVICE = "terms_of_service"
    PRIVACY_POLICY = "privacy_policy"
    MARKETING = "marketing"
    DATA_SHARING = "data_sharing"
    THIRD_PARTY_SHARING = "third_party_sharing"


# User Preferences Schemas
class UserPreferenceBase(BaseModel):
    language: Optional[str] = Field(None, max_length=10, example="en")
    currency: Optional[str] = Field(None, max_length=3, example="NGN")
    timezone: Optional[str] = Field(None, max_length=50, example="Africa/Lagos")
    theme: Optional[str] = Field(None, max_length=20, example="light")
    default_transaction_pin_enabled: Optional[bool] = None
    biometric_enabled: Optional[bool] = None


class UserPreferenceUpdate(UserPreferenceBase):
    pass


class UserPreferenceResponse(UserPreferenceBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Notification Settings Schemas
class NotificationSettingBase(BaseModel):
    # Email
    email_enabled: Optional[bool] = None
    email_transaction_alerts: Optional[bool] = None
    email_security_alerts: Optional[bool] = None
    email_marketing: Optional[bool] = None
    email_product_updates: Optional[bool] = None

    # SMS
    sms_enabled: Optional[bool] = None
    sms_transaction_alerts: Optional[bool] = None
    sms_security_alerts: Optional[bool] = None
    sms_marketing: Optional[bool] = None

    # Push
    push_enabled: Optional[bool] = None
    push_transaction_alerts: Optional[bool] = None
    push_security_alerts: Optional[bool] = None
    push_marketing: Optional[bool] = None


class NotificationSettingUpdate(NotificationSettingBase):
    pass


class NotificationSettingResponse(NotificationSettingBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Privacy Settings Schemas
class PrivacySettingBase(BaseModel):
    profile_visible: Optional[bool] = None
    show_email: Optional[bool] = None
    show_phone: Optional[bool] = None
    show_transaction_history: Optional[bool] = None
    allow_data_collection: Optional[bool] = None
    allow_analytics: Optional[bool] = None
    allow_third_party_sharing: Optional[bool] = None


class PrivacySettingUpdate(PrivacySettingBase):
    pass


class PrivacySettingResponse(PrivacySettingBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Consent Schemas
class ConsentCreate(BaseModel):
    consent_type: ConsentTypeEnum
    granted: bool
    version: Optional[str] = Field(None, example="v1.0")


class ConsentResponse(BaseModel):
    id: UUID
    user_id: UUID
    consent_type: ConsentTypeEnum
    granted: bool
    version: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    granted_at: datetime
    revoked_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class ConsentHistoryResponse(BaseModel):
    consents: list[ConsentResponse]
    total: int
