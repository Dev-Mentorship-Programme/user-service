from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.config.database import get_db_session
from src.config.deps import get_current_user
from src.repositories.preference_repo import PreferenceRepository
from src.services.preference_service import PreferenceService
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
from src.schemas.response import ResponseModel


router = APIRouter()


def get_preference_service(
    db: AsyncSession = Depends(get_db_session),
) -> PreferenceService:
    preference_repo = PreferenceRepository(db)
    return PreferenceService(preference_repo)


@router.get(
    "/preferences",
    response_model=ResponseModel[UserPreferenceResponse],
    summary="Get User Preferences",
    description="Retrieve the current user's general preferences including language, currency, timezone, and theme",
)
async def get_preferences(
    current_user: dict = Depends(get_current_user),
    service: PreferenceService = Depends(get_preference_service),
):
    """Get user preferences"""
    user_id = UUID(current_user["user_id"])
    preferences = await service.get_preferences(user_id)

    return ResponseModel(
        success=True, message="Preferences retrieved successfully", data=preferences
    )


@router.put(
    "/preferences",
    response_model=ResponseModel[UserPreferenceResponse],
    summary="Update User Preferences",
    description="Update the current user's general preferences",
)
async def update_preferences(
    data: UserPreferenceUpdate,
    current_user: dict = Depends(get_current_user),
    service: PreferenceService = Depends(get_preference_service),
):
    """Update user preferences"""
    user_id = UUID(current_user["user_id"])
    preferences = await service.update_preferences(user_id, data)

    return ResponseModel(
        success=True, message="Preferences updated successfully", data=preferences
    )


# ============= NOTIFICATION SETTINGS =============
@router.get(
    "/notifications",
    response_model=ResponseModel[NotificationSettingResponse],
    summary="Get Notification Settings",
    description="Retrieve the current user's notification preferences for email, SMS, and push notifications",
)
async def get_notification_settings(
    current_user: dict = Depends(get_current_user),
    service: PreferenceService = Depends(get_preference_service),
):
    """Get notification settings"""
    user_id = UUID(current_user["user_id"])
    settings = await service.get_notification_settings(user_id)

    return ResponseModel(
        success=True,
        message="Notification settings retrieved successfully",
        data=settings,
    )


@router.put(
    "/notifications",
    response_model=ResponseModel[NotificationSettingResponse],
    summary="Update Notification Settings",
    description="Update the current user's notification preferences",
)
async def update_notification_settings(
    data: NotificationSettingUpdate,
    current_user: dict = Depends(get_current_user),
    service: PreferenceService = Depends(get_preference_service),
):
    """Update notification settings"""
    user_id = UUID(current_user["user_id"])
    settings = await service.update_notification_settings(user_id, data)

    return ResponseModel(
        success=True,
        message="Notification settings updated successfully",
        data=settings,
    )


# ============= PRIVACY SETTINGS =============
@router.get(
    "/privacy",
    response_model=ResponseModel[PrivacySettingResponse],
    summary="Get Privacy Settings",
    description="Retrieve the current user's privacy settings including profile visibility and data sharing preferences",
)
async def get_privacy_settings(
    current_user: dict = Depends(get_current_user),
    service: PreferenceService = Depends(get_preference_service),
):
    """Get privacy settings"""
    user_id = UUID(current_user["user_id"])
    settings = await service.get_privacy_settings(user_id)

    return ResponseModel(
        success=True, message="Privacy settings retrieved successfully", data=settings
    )


@router.put(
    "/privacy",
    response_model=ResponseModel[PrivacySettingResponse],
    summary="Update Privacy Settings",
    description="Update the current user's privacy settings",
)
async def update_privacy_settings(
    data: PrivacySettingUpdate,
    current_user: dict = Depends(get_current_user),
    service: PreferenceService = Depends(get_preference_service),
):
    """Update privacy settings"""
    user_id = UUID(current_user["user_id"])
    settings = await service.update_privacy_settings(user_id, data)

    return ResponseModel(
        success=True, message="Privacy settings updated successfully", data=settings
    )


# ============= CONSENT MANAGEMENT =============
@router.post(
    "/consent",
    response_model=ResponseModel[ConsentResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Grant or Revoke Consent",
    description="Record user consent for terms of service, privacy policy, marketing, or data sharing",
)
async def grant_or_revoke_consent(
    data: ConsentCreate,
    request: Request,
    current_user: dict = Depends(get_current_user),
    service: PreferenceService = Depends(get_preference_service),
):
    """Grant or revoke consent"""
    user_id = UUID(current_user["user_id"])

    # Capture IP and User-Agent for audit trail
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    consent = await service.grant_or_revoke_consent(
        user_id, data, ip_address, user_agent
    )

    action = "granted" if data.granted else "revoked"
    return ResponseModel(
        success=True, message=f"Consent {action} successfully", data=consent
    )


@router.get(
    "/consent",
    response_model=ResponseModel[ConsentHistoryResponse],
    summary="Get Consent History",
    description="Retrieve the complete consent history for the current user",
)
async def get_consent_history(
    current_user: dict = Depends(get_current_user),
    service: PreferenceService = Depends(get_preference_service),
):
    """Get consent history"""
    user_id = UUID(current_user["user_id"])
    history = await service.get_consent_history(user_id)

    return ResponseModel(
        success=True, message="Consent history retrieved successfully", data=history
    )
