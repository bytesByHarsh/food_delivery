# Built-in Dependencies
from typing import Annotated, Dict, Any
import os

# Third-Party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, Request, File, UploadFile
import fastapi
from PIL import Image
from sqlalchemy.sql import text

# Local Dependencies
from app.core.dependencies import CurrentUser, CurrentSuperUser
from app.db.crud.crud_user import crud_users, create_new_user, get_full_user_details
from app.db.session import async_get_db
from app.core.http_exceptions import (
    DuplicateValueException,
    NotFoundException,
    ForbiddenException,
    # RateLimitException
)
from app.schemas.v1.schema_user import UserCreate, UserUpdate, UserRead, UserReadFull
from app.db.models.v1.db_user import AccessLevel_Enum

from app.utils.paginated import (
    PaginatedListResponse,
    paginated_response,
    compute_offset,
)
from app.core.security import blacklist_token, oauth2_scheme
from app.core.config import settings

router = fastapi.APIRouter(tags=["Users"])


@router.post("", response_model=UserRead, status_code=201)
async def signup_user(
    request: Request,
    user: UserCreate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> Any:
    # For new user make these default
    user.user_role = AccessLevel_Enum.USER
    return await create_new_user(user, db)


@router.post("/create_user", response_model=UserRead, status_code=201)
async def create_user(
    request: Request,
    user: UserCreate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser,
) -> Any:
    # For new user make these default
    try:
        if current_user.user_role != AccessLevel_Enum.ADMIN.value:
            raise ForbiddenException("Don't have proper access to create user")
        return await create_new_user(user, db)
    except Exception:
        raise ForbiddenException("Wrong Input Details")


@router.get("/search", response_model=PaginatedListResponse[UserRead])
async def search_users(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser,
    search: str,
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    filters = []

    if search:
        filters.append(text(f"username ILIKE '%{search}%'"))

    if current_user.user_role == AccessLevel_Enum.ADMIN.value:
        users_data = await crud_users.get_multi_on_filters(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=UserRead,
            filters=filters,
        )
    else:
        users_data = await crud_users.get_multi_on_filters(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=UserRead,
            filters=filters,
        )

    if not users_data["data"]:
        raise NotFoundException("No User Found")

    return paginated_response(
        crud_data=users_data, page=page, items_per_page=items_per_page
    )


@router.get("/list", response_model=PaginatedListResponse[UserRead])
async def read_users(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser,
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    users_data = None
    if current_user.user_role == AccessLevel_Enum.ADMIN.value:
        users_data = await crud_users.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=UserRead,
            is_deleted=False,
        )
    else:
        users_data = await crud_users.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=UserRead,
            is_deleted=False,
        )

    if users_data is None:
        raise NotFoundException("No User Found")

    return paginated_response(
        crud_data=users_data, page=page, items_per_page=items_per_page
    )


@router.get("/me", response_model=UserRead)
async def read_user_me(
    request: Request,
    current_user: CurrentUser,
) -> UserRead:
    return current_user


@router.get("/me/full", response_model=UserReadFull)
async def read_user_me_full(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser,
) -> UserReadFull:
    return await get_full_user_details(user=current_user, db=db)


@router.get("/{username}", response_model=UserRead)
async def read_user(
    request: Request,
    username: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentUser,
) -> dict:
    if current_user.user_role == AccessLevel_Enum.ADMIN.value:
        db_user = await crud_users.get(
            db=db,
            schema_to_select=UserRead,
            username=username,
            is_deleted=False,
        )
    else:
        db_user = await crud_users.get(
            db=db,
            schema_to_select=UserRead,
            username=username,
            is_deleted=False,
        )
    if db_user is None:
        raise NotFoundException("User not found")

    return db_user


@router.patch("/{username}")
async def patch_user(
    request: Request,
    values: UserUpdate,
    username: str,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> Dict[str, str]:
    db_user = await crud_users.get(db=db, schema_to_select=UserRead, username=username)
    if db_user is None:
        raise NotFoundException("User not found")

    if current_user.username != values.username:
        # Trying to change for some other user
        if current_user.user_role != AccessLevel_Enum.ADMIN.value:
            # Don't have permission
            raise ForbiddenException(
                "Don't have proper access to change other user details"
            )
    else:
        if current_user.user_role != values.user_role:
            # Person cannot change his user role on it's own
            raise ForbiddenException("Cannot change own Role, contact admin")

    # if db_user["username"] != current_user["username"]:
    #     raise ForbiddenException()

    if values.username != db_user["username"]:
        existing_username = await crud_users.exists(db=db, username=values.username)
        if existing_username:
            raise DuplicateValueException("Username not available")

    if values.email != db_user["email"]:
        existing_email = await crud_users.exists(db=db, email=values.email)
        if existing_email:
            raise DuplicateValueException("Email is already registered")

    await crud_users.update(db=db, object=values, username=username)
    return {"message": "User updated"}


@router.post("/update_profile_image")
async def update_profile_image(
    request: Request,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    file: UploadFile = File(...),
):
    db_user = await crud_users.get(
        db=db, schema_to_select=UserRead, username=current_user.username
    )
    if not db_user:
        raise NotFoundException("User not found")

    FILEPATH = settings.IMAGE_FILE_PATH
    filename = file.filename

    if filename is None:
        raise NotFoundException("File Not Found")

    parts: list[str] = filename.split(".")
    if len(parts) < 2:
        raise ForbiddenException()
    extension = parts[-1]

    if extension not in ["png", "jpg"]:
        raise ForbiddenException("Image Type not supported")

    token_name = current_user.username + "." + extension
    generated_name = os.path.join(FILEPATH, token_name)
    file_content = await file.read()

    with open(generated_name, "wb") as f:
        f.write(file_content)
        f.close()

    await file.close()

    # Pillow
    imgFile = Image.open(generated_name)
    img = imgFile.resize(size=(200, 200))
    img.save(generated_name)

    value = UserUpdate(
        username=current_user.username,
        user_role=current_user.user_role,
        email=current_user.email,
        name=current_user.name,
        profile_image_url=os.path.join(settings.SERVER_LINK, generated_name),
    )
    await crud_users.update(db=db, object=value, username=current_user.username)
    return {"message": "User Profile Image Updated"}


@router.post("/reset_profile_image")
async def reset_profile_image(
    request: Request,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(async_get_db)],
):
    db_user = await crud_users.get(
        db=db, schema_to_select=UserRead, username=current_user.username
    )
    if not db_user:
        raise NotFoundException("User not found")

    value = UserUpdate(
        username=current_user.username,
        user_role=current_user.user_role,
        email=current_user.email,
        name=current_user.name,
        profile_image_url=settings.DEFAULT_USER_IMAGE,
    )
    await crud_users.update(db=db, object=value, username=current_user.username)
    return {"message": "User Profile Image Updated"}


@router.delete("/delete_user/{username}")
async def erase_user(
    request: Request,
    username: str,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    token: str = Depends(oauth2_scheme),
) -> Dict[str, str]:
    if current_user.user_role != AccessLevel_Enum.ADMIN.value:
        raise ForbiddenException("Don't have access to delete user")
    db_user = await crud_users.get(db=db, schema_to_select=UserRead, username=username)
    if not db_user:
        raise NotFoundException("User not found")

    await crud_users.delete(db=db, db_row=db_user, username=username)
    await blacklist_token(token=token, db=db)
    return {"message": "User deleted"}


@router.delete("/delete_user/db_user/{username}")
async def erase_db_user(
    request: Request,
    username: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: CurrentSuperUser,
) -> Dict[str, str]:
    db_user = await crud_users.exists(db=db, username=username)
    if not db_user:
        raise NotFoundException("User not found")

    # Delete user from the database
    await crud_users.db_delete(db=db, username=username)
    return {"message": "User deleted from the database"}
