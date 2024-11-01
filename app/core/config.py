import os
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def unset_env():
    all_env = os.environ
    if "POSTGRES_SERVER" in all_env:
        del os.environ["POSTGRES_SERVER"]
    if "POSTGRES_PORT" in all_env:
        del os.environ["POSTGRES_PORT"]
    if "POSTGRES_USER" in all_env:
        del os.environ["POSTGRES_USER"]
    if "POSTGRES_PASSWORD" in all_env:
        del os.environ["POSTGRES_PASSWORD"]
    if "POSTGRES_DB" in all_env:
        del os.environ["POSTGRES_DB"]
    if "POSTGRES_ASYNC_URI" in all_env:
        del os.environ["POSTGRES_ASYNC_URI"]
    if "DATABASE_URL" in all_env:
        del os.environ["DATABASE_URL"]


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "I_AM_BATMAN"
    ALGORITHM: str = "HS256"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    COOKIES_SECURE_SETTINGS: bool = False

    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    PROJECT_NAME: str
    PROJECT_VERSION: str = "v0.0.1"
    CONTACT_NAME: str = "Harsh Mittal"
    CONTACT_EMAIL: str = "harsmittal2210@gmail.com"

    SERVER_IP: str = "0.0.0.0"
    SERVER_PORT: int = 9000

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SERVER_LINK(self) -> str:
        return f"http://{self.SERVER_IP}:{self.SERVER_PORT}/"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "template_app"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def POSTGRES_ASYNC_URI(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    FIRST_SUPERUSER_NAME: str = "admin"
    FIRST_SUPERUSER_EMAIL: str = "harshmittal2210@gmail.com"
    FIRST_SUPERUSER_USERNAME: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str
    DEFAULT_USER_IMAGE: str = "https://www.imageurl.com/profile_image.jpg"

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self

    DATABASE_USER_TABLE: str = "users"

    STATIC_FILE_FOLDER: str = "static"
    PROFILE_IMAGE_FOLDER: str = "profile_images"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def IMAGE_FILE_PATH(self) -> str:
        return f"{self.STATIC_FILE_FOLDER}/{self.PROFILE_IMAGE_FOLDER}"


unset_env()
settings = Settings()  # type: ignore
print(settings.POSTGRES_DB)
