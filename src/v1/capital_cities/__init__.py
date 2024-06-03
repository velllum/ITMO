import logging

from fastapi import FastAPI

from src.core.configs import settings
from src.core.lifespan import lifespan
from src.core.middelwares import register_middleware

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """- создаем приложение"""
    app = FastAPI(title="HTTP REST API", debug=settings.WEB_DEBUG, lifespan=lifespan)
    register_middleware(app)
    return app


