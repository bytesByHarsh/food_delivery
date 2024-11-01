import logging
import asyncio

from sqlalchemy import text
from sqlmodel import select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db.session import async_get_db
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def init(get_db) -> None:
    try:
        async for db in get_db():
            await db.exec(select(1))
    except Exception as e:
        if "does not exist" in e.__str__():
            logger.info("Creating new database")
            await create_database(get_db)
            return
        logger.error(e)
        raise e


# TODO: Fix create database
async def create_database(get_db) -> None:
    try:
        async for db in get_db():
            await db.exec(text(f"CREATE DATABASE {settings.POSTGRES_DB}"))
            await db.commit()
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    asyncio.run(init(async_get_db))
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
