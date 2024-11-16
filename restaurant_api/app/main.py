# Built-in Dependencies
import sys
import os

# Third-Party Dependencies
import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Add the project directory to the sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


# Local Dependencies
from app.core.config import settings
from app.db import init_db
from app.core.dependencies import create_folders

from app.apis.base import api_router


description = """
Restaurant Microservice
## API Supported
- User Details
- Basic Functionalities
"""

tags_metadata = [
    {"name": "Login", "description": "This is user login route"},
    {"name": "User", "description": "This is user route"},
]


def include_router(app: fastapi.FastAPI):
    app.include_router(api_router, prefix=settings.API_V1_STR)


async def startup_event():
    print("Executing startup event")
    await init_db.init_db()


def start_application():
    app = fastapi.FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description=description,
        contact={"name": settings.CONTACT_NAME, "email": settings.CONTACT_EMAIL},
    )

    if settings.all_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                str(origin).strip("/") for origin in settings.all_cors_origins
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    create_folders(
        f"./{settings.STATIC_FILE_FOLDER}", [f"{settings.PROFILE_IMAGE_FOLDER}"]
    )
    app.mount(
        f"/{settings.STATIC_FILE_FOLDER}",
        StaticFiles(directory=f"{settings.STATIC_FILE_FOLDER}"),
        name=f"{settings.STATIC_FILE_FOLDER}",
    )

    include_router(app)
    app.add_event_handler("startup", startup_event)
    return app


if __name__ == "__main__":
    try:
        print(
            f"[INFO] Starting Application at: host={settings.SERVER_IP}, port={settings.SERVER_PORT}"
        )
        uvicorn.run(
            "main:start_application",
            host=settings.SERVER_IP,
            port=settings.SERVER_PORT,
            reload=True,
        )
    except Exception as e:
        print(f"[ERROR] Main Error: {e}")
