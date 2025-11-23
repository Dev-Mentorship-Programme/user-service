import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.config.database import Base

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
