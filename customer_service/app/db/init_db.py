# Built-in Dependencies

# Third-Party Dependencies
from sqlmodel import select

# Local Dependencies
from app.db.session import AsyncSession, local_session
from app.db.session import async_engine as engine
from app.db.models.v1.common import Base

from app.core.config import settings
from app.core.hashing import Hasher
from app.db.models.v1.db_user import User, AccessLevel_Enum


async def create_first_super_user(session: AsyncSession) -> None:
    name = settings.FIRST_SUPERUSER_NAME
    email = settings.FIRST_SUPERUSER_EMAIL
    username = settings.FIRST_SUPERUSER_USERNAME
    phone = settings.FIRST_SUPERUSER_PHONE
    # userRole = settings.FIRST_SUPERUSER_ROLE
    hashed_pass = Hasher.get_hash_password(settings.FIRST_SUPERUSER_PASSWORD)

    # check if already existing
    query = select(User).filter_by(email=email)
    result = await session.exec(query)
    user = result.one_or_none()

    if user is None:
        session.add(
            User(
                name=name,
                email=email,
                username=username,
                phone=phone,
                hashed_password=hashed_pass,
                is_superuser=True,
                profile_image_url="https://www.imageurl.com/first_user.jpg",
                user_role=AccessLevel_Enum.ADMIN,
            )
        )
        await session.commit()
    pass


async def init_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def init_db() -> None:
    await init_tables()
    async with local_session() as session:
        await create_first_super_user(session=session)
