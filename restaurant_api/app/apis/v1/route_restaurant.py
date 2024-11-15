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
# from app.db.crud.crud_user import crud_users, create_new_user, get_full_user_details
from app.db.session import async_get_db
from app.core.http_exceptions import (
    DuplicateValueException,
    NotFoundException,
    ForbiddenException,
    # RateLimitException
)
# from app.schemas.v1.schema_user import UserCreate, UserUpdate, UserRead, UserReadFull
# from app.db.models.v1.db_user import AccessLevel_Enum

from app.utils.paginated import (
    PaginatedListResponse,
    paginated_response,
    compute_offset,
)
from app.core.security import blacklist_token, oauth2_scheme
from app.core.config import settings

router = fastapi.APIRouter(tags=["Users"])