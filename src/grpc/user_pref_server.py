import asyncio
import logging
from datetime import datetime
from uuid import UUID

import grpc

from src.grpc.proto.server import user_pb2, user_pb2_grpc
from src.config.database import sessionmanager
from src.repositories.preference_repo import PreferenceRepository
from src.schemas.user_preference import (
    UserPreferenceUpdate,
    NotificationSettingUpdate,
    PrivacySettingUpdate,
    ConsentCreate,
)

logger = logging.getLogger("user_pref_grpc")


class UserPreferenceServiceServicer(user_pb2_grpc.UserPreferenceServiceServicer):
    async def GetPreference(self, request, context):
        """Get user preferences"""
        try:
            user_id = UUID(request.user_id)
        except ValueError:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Invalid user_id format"
            )

        async with sessionmanager.session() as session:
            repo = PreferenceRepository(session)
            pref = await repo.get_user_preference(user_id)

        if not pref:
            return user_pb2.PreferenceResponse()

        return user_pb2.PreferenceResponse(
            preference=user_pb2.Preference(
                user_id=str(pref.user_id),
                language=pref.language or "",
                currency=pref.currency or "",
                timezone=pref.timezone or "",
                theme=pref.theme or "",
            )
        )

    async def UpdatePreference(self, request, context):
        """Update user preferences"""
        try:
            user_id = UUID(request.user_id)
        except ValueError:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Invalid user_id format"
            )

        p = request.preference

        # Convert proto message to Pydantic model
        update_data = UserPreferenceUpdate(
            language=p.language if p.language else None,
            currency=p.currency if p.currency else None,
            timezone=p.timezone if p.timezone else None,
            theme=p.theme if p.theme else None,
        )

        async with sessionmanager.session() as session:
            repo = PreferenceRepository(session)
            pref = await repo.update_user_preference(user_id, update_data)

        return user_pb2.PreferenceResponse(
            preference=user_pb2.Preference(
                user_id=str(pref.user_id),
                language=pref.language or "",
                currency=pref.currency or "",
                timezone=pref.timezone or "",
                theme=pref.theme or "",
            )
        )

    async def GetNotificationSetting(self, request, context):
        """Get notification settings"""
        try:
            user_id = UUID(request.user_id)
        except ValueError:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Invalid user_id format"
            )

        async with sessionmanager.session() as session:
            repo = PreferenceRepository(session)
            setting = await repo.get_notification_setting(user_id)

        if not setting:
            return user_pb2.NotificationResponse()

        return user_pb2.NotificationResponse(
            notification=user_pb2.NotificationSetting(
                user_id=str(setting.user_id),
                email_enabled=setting.email_enabled,
                sms_enabled=setting.sms_enabled,
                push_enabled=setting.push_enabled,
            )
        )

    async def UpdateNotificationSetting(self, request, context):
        """Update notification settings"""
        try:
            user_id = UUID(request.user_id)
        except ValueError:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Invalid user_id format"
            )

        n = request.notification

        # Convert proto to Pydantic
        update_data = NotificationSettingUpdate(
            email_enabled=n.email_enabled if n.HasField("email_enabled") else None,
            sms_enabled=n.sms_enabled if n.HasField("sms_enabled") else None,
            push_enabled=n.push_enabled if n.HasField("push_enabled") else None,
        )

        async with sessionmanager.session() as session:
            repo = PreferenceRepository(session)
            setting = await repo.update_notification_setting(user_id, update_data)

        return user_pb2.NotificationResponse(
            notification=user_pb2.NotificationSetting(
                user_id=str(setting.user_id),
                email_enabled=setting.email_enabled,
                sms_enabled=setting.sms_enabled,
                push_enabled=setting.push_enabled,
            )
        )

    async def GetPrivacySetting(self, request, context):
        """Get privacy settings"""
        try:
            user_id = UUID(request.user_id)
        except ValueError:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Invalid user_id format"
            )

        async with sessionmanager.session() as session:
            repo = PreferenceRepository(session)
            setting = await repo.get_privacy_setting(user_id)

        if not setting:
            return user_pb2.PrivacyResponse()

        return user_pb2.PrivacyResponse(
            privacy=user_pb2.PrivacySetting(
                user_id=str(setting.user_id),
                profile_visible=setting.profile_visible,
                show_email=setting.show_email,
                show_phone=setting.show_phone,
            )
        )

    async def UpdatePrivacySetting(self, request, context):
        """Update privacy settings"""
        try:
            user_id = UUID(request.user_id)
        except ValueError:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Invalid user_id format"
            )

        p = request.privacy

        # Convert proto to Pydantic
        update_data = PrivacySettingUpdate(
            profile_visible=(
                p.profile_visible if p.HasField("profile_visible") else None
            ),
            show_email=p.show_email if p.HasField("show_email") else None,
            show_phone=p.show_phone if p.HasField("show_phone") else None,
        )

        async with sessionmanager.session() as session:
            repo = PreferenceRepository(session)
            setting = await repo.update_privacy_setting(user_id, update_data)

        return user_pb2.PrivacyResponse(
            privacy=user_pb2.PrivacySetting(
                user_id=str(setting.user_id),
                profile_visible=setting.profile_visible,
                show_email=setting.show_email,
                show_phone=setting.show_phone,
            )
        )

    async def CreateConsent(self, request, context):
        """Create a consent record"""
        try:
            user_id = UUID(request.user_id)
        except ValueError:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Invalid user_id format"
            )

        # Convert proto to Pydantic
        consent_data = ConsentCreate(
            consent_type=request.consent_type,
            granted=request.granted,
            version=request.version if request.version else None,
        )

        async with sessionmanager.session() as session:
            repo = PreferenceRepository(session)
            consent = await repo.create_consent(
                user_id,
                consent_data,
                ip_address=request.ip_address if request.ip_address else None,
                user_agent=request.user_agent if request.user_agent else None,
            )

        return user_pb2.CreateConsentResponse(
            consent=user_pb2.Consent(
                id=str(consent.id),
                user_id=str(consent.user_id),
                consent_type=(
                    consent.consent_type.value
                    if hasattr(consent.consent_type, "value")
                    else str(consent.consent_type)
                ),
                granted=consent.granted,
                version=consent.version or "",
                ip_address=consent.ip_address or "",
                user_agent=consent.user_agent or "",
                granted_at=consent.granted_at.isoformat() if consent.granted_at else "",
                revoked_at=consent.revoked_at.isoformat() if consent.revoked_at else "",
            )
        )

    async def GetConsentHistory(self, request, context):
        """Get consent history for a user"""
        try:
            user_id = UUID(request.user_id)
        except ValueError:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Invalid user_id format"
            )

        async with sessionmanager.session() as session:
            repo = PreferenceRepository(session)
            consents = await repo.get_consent_history(user_id)

        pb_consents = []
        for c in consents:
            pb_consents.append(
                user_pb2.Consent(
                    id=str(c.id),
                    user_id=str(c.user_id),
                    consent_type=(
                        c.consent_type.value
                        if hasattr(c.consent_type, "value")
                        else str(c.consent_type)
                    ),
                    granted=c.granted,
                    version=c.version or "",
                    ip_address=c.ip_address or "",
                    user_agent=c.user_agent or "",
                    granted_at=c.granted_at.isoformat() if c.granted_at else "",
                    revoked_at=c.revoked_at.isoformat() if c.revoked_at else "",
                )
            )

        return user_pb2.GetConsentHistoryResponse(consents=pb_consents)

    async def GetLatestConsent(self, request, context):
        """Get latest consent for a specific type"""
        try:
            user_id = UUID(request.user_id)
        except ValueError:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Invalid user_id format"
            )

        async with sessionmanager.session() as session:
            repo = PreferenceRepository(session)
            c = await repo.get_latest_consent(user_id, request.consent_type)

        if not c:
            return user_pb2.GetLatestConsentResponse()

        return user_pb2.GetLatestConsentResponse(
            consent=user_pb2.Consent(
                id=str(c.id),
                user_id=str(c.user_id),
                consent_type=(
                    c.consent_type.value
                    if hasattr(c.consent_type, "value")
                    else str(c.consent_type)
                ),
                granted=c.granted,
                version=c.version or "",
                ip_address=c.ip_address or "",
                user_agent=c.user_agent or "",
                granted_at=c.granted_at.isoformat() if c.granted_at else "",
                revoked_at=c.revoked_at.isoformat() if c.revoked_at else "",
            )
        )


async def serve(host: str = "0.0.0.0", port: int = 50051):
    server = grpc.aio.server()
    user_pb2_grpc.add_UserPreferenceServiceServicer_to_server(
        UserPreferenceServiceServicer(), server
    )
    listen_addr = f"{host}:{port}"
    server.add_insecure_port(listen_addr)
    logger.info(f"gRPC server listening on {listen_addr}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
