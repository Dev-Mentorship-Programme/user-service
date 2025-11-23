import uuid
from datetime import datetime
from sqlalchemy import Column,Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.config.database import Base


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
