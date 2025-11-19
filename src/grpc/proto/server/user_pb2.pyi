from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPreferenceRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class Preference(_message.Message):
    __slots__ = ("user_id", "language", "currency", "timezone", "theme")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    THEME_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    language: str
    currency: str
    timezone: str
    theme: str
    def __init__(self, user_id: _Optional[str] = ..., language: _Optional[str] = ..., currency: _Optional[str] = ..., timezone: _Optional[str] = ..., theme: _Optional[str] = ...) -> None: ...

class UpdatePreferenceRequest(_message.Message):
    __slots__ = ("user_id", "preference")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    preference: Preference
    def __init__(self, user_id: _Optional[str] = ..., preference: _Optional[_Union[Preference, _Mapping]] = ...) -> None: ...

class PreferenceResponse(_message.Message):
    __slots__ = ("preference",)
    PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    preference: Preference
    def __init__(self, preference: _Optional[_Union[Preference, _Mapping]] = ...) -> None: ...

class NotificationSetting(_message.Message):
    __slots__ = ("user_id", "email_enabled", "sms_enabled", "push_enabled")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SMS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PUSH_ENABLED_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    email_enabled: bool
    sms_enabled: bool
    push_enabled: bool
    def __init__(self, user_id: _Optional[str] = ..., email_enabled: bool = ..., sms_enabled: bool = ..., push_enabled: bool = ...) -> None: ...

class UpdateNotificationRequest(_message.Message):
    __slots__ = ("user_id", "notification")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    notification: NotificationSetting
    def __init__(self, user_id: _Optional[str] = ..., notification: _Optional[_Union[NotificationSetting, _Mapping]] = ...) -> None: ...

class NotificationResponse(_message.Message):
    __slots__ = ("notification",)
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    notification: NotificationSetting
    def __init__(self, notification: _Optional[_Union[NotificationSetting, _Mapping]] = ...) -> None: ...

class PrivacySetting(_message.Message):
    __slots__ = ("user_id", "profile_visible", "show_email", "show_phone")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PROFILE_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    SHOW_EMAIL_FIELD_NUMBER: _ClassVar[int]
    SHOW_PHONE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    profile_visible: bool
    show_email: bool
    show_phone: bool
    def __init__(self, user_id: _Optional[str] = ..., profile_visible: bool = ..., show_email: bool = ..., show_phone: bool = ...) -> None: ...

class UpdatePrivacyRequest(_message.Message):
    __slots__ = ("user_id", "privacy")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVACY_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    privacy: PrivacySetting
    def __init__(self, user_id: _Optional[str] = ..., privacy: _Optional[_Union[PrivacySetting, _Mapping]] = ...) -> None: ...

class PrivacyResponse(_message.Message):
    __slots__ = ("privacy",)
    PRIVACY_FIELD_NUMBER: _ClassVar[int]
    privacy: PrivacySetting
    def __init__(self, privacy: _Optional[_Union[PrivacySetting, _Mapping]] = ...) -> None: ...

class Consent(_message.Message):
    __slots__ = ("id", "user_id", "consent_type", "granted", "version", "ip_address", "user_agent", "granted_at", "revoked_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONSENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    GRANTED_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    GRANTED_AT_FIELD_NUMBER: _ClassVar[int]
    REVOKED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    consent_type: str
    granted: bool
    version: str
    ip_address: str
    user_agent: str
    granted_at: str
    revoked_at: str
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., consent_type: _Optional[str] = ..., granted: bool = ..., version: _Optional[str] = ..., ip_address: _Optional[str] = ..., user_agent: _Optional[str] = ..., granted_at: _Optional[str] = ..., revoked_at: _Optional[str] = ...) -> None: ...

class CreateConsentRequest(_message.Message):
    __slots__ = ("user_id", "consent_type", "granted", "version", "ip_address", "user_agent")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONSENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    GRANTED_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    consent_type: str
    granted: bool
    version: str
    ip_address: str
    user_agent: str
    def __init__(self, user_id: _Optional[str] = ..., consent_type: _Optional[str] = ..., granted: bool = ..., version: _Optional[str] = ..., ip_address: _Optional[str] = ..., user_agent: _Optional[str] = ...) -> None: ...

class CreateConsentResponse(_message.Message):
    __slots__ = ("consent",)
    CONSENT_FIELD_NUMBER: _ClassVar[int]
    consent: Consent
    def __init__(self, consent: _Optional[_Union[Consent, _Mapping]] = ...) -> None: ...

class GetConsentHistoryRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GetConsentHistoryResponse(_message.Message):
    __slots__ = ("consents",)
    CONSENTS_FIELD_NUMBER: _ClassVar[int]
    consents: _containers.RepeatedCompositeFieldContainer[Consent]
    def __init__(self, consents: _Optional[_Iterable[_Union[Consent, _Mapping]]] = ...) -> None: ...

class GetLatestConsentRequest(_message.Message):
    __slots__ = ("user_id", "consent_type")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONSENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    consent_type: str
    def __init__(self, user_id: _Optional[str] = ..., consent_type: _Optional[str] = ...) -> None: ...

class GetLatestConsentResponse(_message.Message):
    __slots__ = ("consent",)
    CONSENT_FIELD_NUMBER: _ClassVar[int]
    consent: Consent
    def __init__(self, consent: _Optional[_Union[Consent, _Mapping]] = ...) -> None: ...
