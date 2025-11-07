import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.config.database import Base


class ConsentType(str, enum.Enum):
    TERMS_OF_SERVICE = "terms_of_service"
    PRIVACY_POLICY = "privacy_policy"
    MARKETING = "marketing"
    DATA_SHARING = "data_sharing"
    THIRD_PARTY_SHARING = "third_party_sharing"


class NotificationChannel(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)

    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String(20), default="user")  # user, admin, super_admin

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    preferences = relationship(
        "UserPreference",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    notification_settings = relationship(
        "UserNotificationSetting",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    privacy_settings = relationship(
        "UserPrivacySetting",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    consents = relationship(
        "UserConsent", back_populates="user", cascade="all, delete-orphan"
    )


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # General Preferences
    language = Column(String(10), default="en")
    currency = Column(String(3), default="NGN")
    timezone = Column(String(50), default="Africa/Lagos")
    theme = Column(String(20), default="light")  # light, dark, auto

    # Transaction Preferences
    default_transaction_pin_enabled = Column(Boolean, default=True)
    biometric_enabled = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="preferences")


class UserNotificationSetting(Base):
    __tablename__ = "user_notification_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # Email Notifications
    email_enabled = Column(Boolean, default=True)
    email_transaction_alerts = Column(Boolean, default=True)
    email_security_alerts = Column(Boolean, default=True)
    email_marketing = Column(Boolean, default=False)
    email_product_updates = Column(Boolean, default=True)

    # SMS Notifications
    sms_enabled = Column(Boolean, default=True)
    sms_transaction_alerts = Column(Boolean, default=True)
    sms_security_alerts = Column(Boolean, default=True)
    sms_marketing = Column(Boolean, default=False)

    # Push Notifications
    push_enabled = Column(Boolean, default=True)
    push_transaction_alerts = Column(Boolean, default=True)
    push_security_alerts = Column(Boolean, default=True)
    push_marketing = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="notification_settings")


class UserPrivacySetting(Base):
    __tablename__ = "user_privacy_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # Profile Visibility
    profile_visible = Column(Boolean, default=False)
    show_email = Column(Boolean, default=False)
    show_phone = Column(Boolean, default=False)
    show_transaction_history = Column(Boolean, default=False)

    # Data Management
    allow_data_collection = Column(Boolean, default=True)
    allow_analytics = Column(Boolean, default=True)
    allow_third_party_sharing = Column(Boolean, default=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="privacy_settings")


class UserConsent(Base):
    __tablename__ = "user_consents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    consent_type = Column(Enum(ConsentType), nullable=False)
    granted = Column(Boolean, nullable=False)
    version = Column(String(20))  # e.g., "v1.0", "v2.3"
    ip_address = Column(String(45))  # IPv4 or IPv6
    user_agent = Column(String(500))

    # Audit trail
    granted_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="consents")

    __table_args__ = (
        # Index for efficient consent lookups
        {"schema": None}
    )
