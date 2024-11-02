# Built-in Dependencies

# Built-in Dependencies
from typing import Annotated, Dict
from datetime import timedelta

# Third-party Dependencies
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from fastapi import Response, Request, Depends, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession


# Local Dependencies
from app.core.http_exceptions import UnauthorizedException
from app.core.config import settings
from app.schemas.v1.schema_auth import Token
from app.db.session import async_get_db
from app.core.security import (
    create_access_token,
    authenticate_user,
    create_refresh_token,
    verify_token,
    oauth2_scheme,
    blacklist_token,
)

router = APIRouter(tags=["Login"])


@router.post("/login", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> Dict[str, str]:
    user = await authenticate_user(
        username_or_email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise UnauthorizedException("Wrong username, email or password.")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )

    refresh_token = await create_refresh_token(data={"sub": user["username"]})
    max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 24 * 60 * 60

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        # httponly=True,
        secure=settings.COOKIES_SECURE_SETTINGS,
        samesite="lax",
        max_age=max_age,
    )
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        # httponly=True,
        secure=settings.COOKIES_SECURE_SETTINGS,
        samesite="lax",
        max_age=max_age,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh")
async def refresh_access_token(
    request: Request, db: AsyncSession = Depends(async_get_db)
) -> Dict[str, str]:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise UnauthorizedException("Refresh token missing.")

    user_data = await verify_token(refresh_token, db)
    if not user_data:
        raise UnauthorizedException("Invalid refresh token.")

    new_access_token = await create_access_token(
        data={"sub": user_data.username_or_email}
    )
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(
    response: Response,
    access_token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(async_get_db),
) -> Dict[str, str]:
    try:
        await blacklist_token(token=access_token, db=db)
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")

        return {"message": "Logged out successfully"}

    except JWTError:
        raise UnauthorizedException("Invalid token.")
