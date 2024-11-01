from typing import Dict, Any, Literal, Union

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession

# Local Dependencies
from app.db.crud.base import CRUDBase
from app.db.models.v1.db_user import User
from app.schemas.v1.schema_user import (
    UserCreateInternal,
    UserUpdate,
    UserUpdateInternal,
    UserDelete,
    UserCreate,
)

from app.core.http_exceptions import (
    DuplicateValueException,
    # RateLimitException
)

from app.core.hashing import Hasher

# CRUD operations for the 'User' model
CRUDUser = CRUDBase[
    User, UserCreateInternal, UserUpdate, UserUpdateInternal, UserDelete
]

# Create an instance of CRUDUser for the 'User' model
crud_users = CRUDUser(User)


async def create_new_user(user: UserCreate, db: AsyncSession) -> User:
    email_row = await crud_users.exists(db=db, email=user.email)
    if email_row:
        raise DuplicateValueException("Email is already registered")
    username_row = await crud_users.exists(db=db, username=user.username)
    if username_row:
        raise DuplicateValueException("Username not available")

    user_internal_dict = user.model_dump()
    user_internal_dict["hashed_password"] = Hasher.get_hash_password(
        plain_password=user_internal_dict["password"]
    )
    del user_internal_dict["password"]

    user_internal = UserCreateInternal(**user_internal_dict)
    return await crud_users.create(db=db, object=user_internal)


async def get_user(
    username_or_email: str, db: AsyncSession
) -> Union[Dict[str, Any], Literal[None]]:
    if "@" in username_or_email:
        db_user: dict = await crud_users.get(
            db=db, email=username_or_email, is_deleted=False
        )
    else:
        db_user = await crud_users.get(
            db=db, username=username_or_email, is_deleted=False
        )

    if not db_user:
        return None

    return db_user
