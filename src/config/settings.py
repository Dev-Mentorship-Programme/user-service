from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Literal, Optional
from src.config.constants import Environment
import os

servive_name = os.getenv("SERVICE_NAME", "User-service")
service_mode = os.getenv("SERVICE_MODE", "development")
postgres_server = os.getenv("POSTGRES_SERVER", "localhost")
postgres_user = os.getenv("POSTGRES_USER", "postgres")
postgres_password = os.getenv("POSTGRES_PASSWORD", "postgres")
postgres_db = os.getenv("POSTGRES_DB", "postgres")
postgres_port = os.getenv("POSTGRES_PORT", 5432)
smtp_server = os.getenv("SMTP_SERVER", "localhost")
smtp_port = os.getenv("SMTP_PORT", 25)
smtp_username = os.getenv("SMTP_USERNAME", "user")
smtp_password = os.getenv("SMTP_PASSWORD", "password")
log_level = os.getenv("LOG_LEVEL", "INFO")
cors_origins = os.getenv("CORS_ORIGINS", ["*"])
cors_headers = os.getenv("CORS_HEADERS", ["*"])
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
redis_db = os.getenv("REDIS_DB", "0")
redis_password = os.getenv("REDIS_PASSWORD", "password")
rabbitmq_exchange = os.getenv("RABBITMQ_EXCHANGE", "user_service")
rabbitmq_default_user = os.getenv("RABBITMQ_DEFAULT_USER", "admin")
rabbitmq_default_password = os.getenv("RABBITMQ_DEFAULT_PASSWORD", "admin")
rabbitmq_default_host = os.getenv("RABBITMQ_DEFAULT_HOST", "localhost")
rabbitmq_default_port = os.getenv("RABBITMQ_DEFAULT_PORT", "5672")
host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", 8000)
grpc_port = os.getenv("GRPC_PORT", 50051)
kyc_service_host = os.getenv("KYC_SERVICE_HOST", "localhost")
kyc_service_port = os.getenv("KYC_SERVICE_PORT", 8001)
service_discovery_url = os.getenv("SERVICE_DISCOVERY_URL", "http://localhost:8000")
access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
refresh_token_expire_days = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7)
algorithm = os.getenv("ALGORITHM", "HS256")
secret_key = os.getenv("JWT_SECRET", "your_jwt_secret")
rate_limit_requests_per_minute = os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", 60)
google_client_id = os.getenv("GOOGLE_CLIENT_ID", "client_id")
google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "client_secret")
facebook_client_id = os.getenv("FACEBOOK_CLIENT_ID", "client_id")
facebook_client_secret = os.getenv("FACEBOOK_CLIENT_SECRET", "client_secret")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", "access_key_id")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", "secret_access_key")
aws_region = os.getenv("AWS_REGION", "us-east-1")
aws_s3_bucket = os.getenv("AWS_S3_BUCKET", "bucket_name")
grpc_client_timeout = os.getenv("GRPC_CLIENT_TIMEOUT", 30)


class Settings(BaseSettings):
    SERVICE_NAME: str = servive_name
    SERVICE_MODE: str = Literal["development", "production"]
    DEBUG: bool = True

    # Database
    POSTGRES_SERVER: str = postgres_server
    POSTGRES_USER: str = postgres_user
    POSTGRES_PASSWORD: str = postgres_password
    POSTGRES_DB: str = postgres_db
    POSTGRES_PORT: str = postgres_port

    @property
    def sqlalchemy_database_uri(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Email
    SMTP_SERVER: str = smtp_server
    SMTP_PORT: int = smtp_port
    SMTP_USERNAME: str = smtp_username
    SMTP_PASSWORD: str = smtp_password

    LOG_LEVEL: str = log_level
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    CORS_ORIGINS: List[str] = cors_origins
    CORS_HEADERS: List[str] = cors_headers

    # Redis
    REDIS_PASSWORD: Optional[str] = redis_password
    REDIS_HOST: str = redis_host
    REDIS_PORT: int = redis_port
    REDIS_DB: str = redis_db

    @property
    def get_redis_url(self) -> str:
        return f"redis://{self.REDIS_DB}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"

    # RabbitMQ
    # RABBITMQ_URL: str = "amqp://admin:password@localhost:5672/"
    RABBITMQ_EXCHANGE: str = rabbitmq_exchange
    RABBITMQ_DEFAULT_USER: str = rabbitmq_default_user
    RABBITMQ_DEFAULT_PASS: str = rabbitmq_default_password
    RABBITMQ_DEFAULT_HOST: str = rabbitmq_default_host
    RABBITMQ_DEFAULT_PORT: int = rabbitmq_default_port

    @property
    def get_amqp_url(self) -> str:
        return f"amqp://{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASS}@{self.RABBITMQ_DEFAULT_HOST}:{self.RABBITMQ_DEFAULT_PORT}/"

    # Server
    HOST: str = host
    PORT: int = port
    GRPC_PORT: int = grpc_port

    # gRPC Client Services
    KYC_SERVICE_HOST: str = kyc_service_host
    KYC_SERVICE_PORT: int = kyc_service_port

    # Service Discovery Consul
    SERVICE_DISCOVERY_URL: Optional[str] = service_discovery_url

    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = access_token_expire_minutes
    REFRESH_TOKEN_EXPIRE_DAYS: int = refresh_token_expire_days
    ALGORITHM: str = algorithm
    SECRET_KEY: str = secret_key

    # gRPC Client Timeouts and Retries
    GRPC_CLIENT_TIMEOUT: int = grpc_client_timeout

    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = rate_limit_requests_per_minute

    # SMS
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None

    # OAuth
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    FACEBOOK_CLIENT_ID: Optional[str] = None
    FACEBOOK_CLIENT_SECRET: Optional[str] = None

    # Storage
    AWS_ACCESS_KEY_ID: Optional[str] = aws_access_key_id
    AWS_SECRET_ACCESS_KEY: Optional[str] = aws_secret_access_key
    AWS_REGION: str = aws_region
    AWS_S3_BUCKET: Optional[str] = aws_s3_bucket

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = []

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
