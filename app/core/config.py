import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

API_V1_STR = "/api/v1"
PROJECT_NAME = "YOUR_PROJECT_NAME"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.warning("DATABASE_URL not found in environment variables.")
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            logger.info(f"Contents of .env file: {f.read()}")

if DATABASE_URL and DATABASE_URL.startswith("postgresql+psycopg2") and ENVIRONMENT != "testing":
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg2", "postgresql+asyncpg")
    SYNC_DATABASE_URL = DATABASE_URL
else:
    ASYNC_DATABASE_URL = DATABASE_URL
    SYNC_DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2") if DATABASE_URL else None

#add your env variables here
ENV_VARIABLE_NAME = os.getenv("ENV_VARIABLE_NAME")

class Settings:
    API_V1_STR = API_V1_STR
    PROJECT_NAME = PROJECT_NAME
    ENVIRONMENT = ENVIRONMENT
    DATABASE_URL = ASYNC_DATABASE_URL

settings = Settings()

