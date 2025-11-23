import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.config.database import Base
from src.utils.constant import ConsentType


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
