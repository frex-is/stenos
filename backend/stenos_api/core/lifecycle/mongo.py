from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from stenos_api.core.logging.mongo_logger import log_mongo_error
from stenos_api.core.configurations.logging import logger
from stenos_api.core.configurations.settings import settings


async def init_mongo(stenos_application: FastAPI) -> None:
    """
    Initialize MongoDB client and attach it to the FastAPI app state.

    Pings the database to confirm connectivity and selects the configured database.
    Logs key steps and errors, raising exceptions on failure.

    Args:
        stenos_application (FastAPI): FastAPI app instance.
    """

    logger.debug(
        "🐛 Starting database initialization", 
        step="init_mongo", 
        details={
            "uri" : settings.mongo_uri_masked
        }
    )

    logger.info("🔄 Initializing MongoDB connection...")
    
    stenos_application.state.mongodb_client = AsyncIOMotorClient(settings.mongo_uri)

    try:
        await stenos_application.state.mongodb_client.admin.command("ping")
        logger.info("✅ MongoDB connection established.")

        logger.debug(
            "📂 Selecting database", 
            db_name=settings.mongo_database, 
            client=str(stenos_application.state.mongodb_client)
        )

        stenos_application.state.mongodb = stenos_application.state.mongodb_client[settings.mongo_database]

        logger.info(f"✅ MongoDB database `{settings.mongo_database}` successfully selected.")
    except Exception as error:
        log_mongo_error(error)
        raise error


async def close_mongo(stenos_application: FastAPI) -> None:
    """
    Close the MongoDB client connection attached to the FastAPI app state.

    Logs the closing process.

    Args:
        stenos_application (FastAPI): FastAPI app instance.
    """

    stenos_application.state.mongodb_client.close()
    logger.debug("🔒 MongoDB AsyncIOMotorClient has been closed")
    logger.info("🔒 MongoDB connection closed successfully.")
