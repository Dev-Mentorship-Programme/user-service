import pytest
import asyncio
from uuid import uuid4
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from httpx import AsyncClient, ASGITransport

from src.main import app
from src.config.database import Base, get_db_session

# Dockerized test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"



@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()



@pytest.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function", autouse=True)
async def setup_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



@pytest.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    SessionLocal = async_sessionmaker(
        bind=test_engine, expire_on_commit=False, class_=AsyncSession
    )

    async with SessionLocal() as session:
        yield session
        await session.close()



@pytest.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        async with db_session.begin():
            yield db_session

    app.dependency_overrides[get_db_session] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_id():
    return str(uuid4())


@pytest.fixture
def sample_preference_data():
    return {
        "language": "en",
        "currency": "USD",
        "timezone": "America/New_York",
        "theme": "light",
        "date_format": "YYYY-MM-DD",
        "time_format": "24h",
    }


@pytest.fixture
def sample_notification_data():
    return {
        "email_enabled": True,
        "sms_enabled": True,
        "push_enabled": True,
        "marketing_emails": False,
        "transaction_alerts": True,
        "security_alerts": True,
    }


@pytest.fixture
def sample_privacy_data():
    return {
        "profile_visible": True,
        "show_email": False,
        "show_phone": False,
        "show_transaction_history": False,
        "data_sharing_enabled": False,
    }


@pytest.fixture
def sample_consent_data():
    return {
        "consent_type": "terms_of_service",
        "granted": True,
        "version": "v2.0",
    }


@pytest.fixture
def mock_current_user():
    async def _mock():
        return {
            "user_id": "c4e9c473-f1f4-4a8b-9f12-2332e36aea03",
            "email": "test@example.com",
            "phone": "1234567890",
            "first_name": "Test",
            "last_name": "User",
            "is_active": True,
            "is_verified": True,
            "role": "user",
            "created_at": "2025-11-18T15:00:00",
        }

    return _mock
